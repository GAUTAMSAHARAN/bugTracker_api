from channels.generic.websocket import WebsocketConsumer
import asyncio
import json
import io
from asgiref.sync import async_to_sync
from .models import Comment, Issue, User
from .serializers import CommentSerializers
from rest_framework.authtoken.models import Token
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

class CommentConsumer(WebsocketConsumer):

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['issue_id']
        self.issue_id = int(self.room_name)
        self.room_group_name = 'issue_'+self.room_name

        async_to_sync(self.channel_layer.group_add)(
           self.room_group_name,
           self.channel_name
        )

        self.accept()

    def disconnect(self, close_code=None):
        self.send(json.dumps({"end_message":close_code}))
        async_to_sync (self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
        self.close()

    def new_message(self, data, user):
        print('new')
        comment = ''
        try:
           comment = data['body']
        except KeyError:
            self.disconnect('comment body in not avaliable')
        issue = Issue.objects.get(pk=self.issue_id)
        new_comment = Comment.objects.create(body=comment,creater=user, issues=issue)
        serialized_comment = CommentSerializers(new_comment).data
        content = {
            'command': 'new_message',
            'comment': serialized_comment
        }
        data = json.dumps(content)
        print(data)
        async_to_sync(self.channel_layer.group_send)(
           self.room_group_name,
           {
             'type': 'comment_message',
             'text': data
           }
        )

    def fetch_messages(self, data, user):
        issue = None
        try:
          issue = Issue.objects.get(pk = self.issue_id)
        except Issue.DoesNotExist:
          self.disconnect('Issue does not exist')

        comments = issue.comments.all().order_by("-upload_time")
        serialzed_comments = CommentSerializers(comments, many=True).data
        info = JSONRenderer().render(serialzed_comments)
        stream = io.BytesIO(info)
        data = JSONParser().parse(stream)
        content = {
           "command": 'messages',
           "data": data
        }
        print(content)
        self.send(text_data=json.dumps(content))

    commands = {
        'fetch_messages' : fetch_messages,
        'new_message' : new_message
    }





    def check_token(self, json_data):
        try:
            token = json_data["token"]
        except KeyError:
            self.disconnect("token key not present")
            return "undefined"
        try:
            token_object = Token.objects.get(key=token)
        except Token.DoesNotExist:
            self.disconnect("invalid token. Token does not exists")
            return "undefined"
        user = token_object.user
        return user

    def receive(self, text_data):
        print('hello')
        print(text_data)
        json_data = json.loads(text_data)
        user = self.check_token(json_data)
        if user != 'undefined':
            try:
                command = json_data['command']
                if command not in self.commands.keys():
                    self.disconnect("command property not valid")
            except KeyError:
                    self.disconnect("command property is not persent")
            self.commands[command](self,json_data,user)
        
    def comment_message(self,event):
          self.send(text_data=event["text"])

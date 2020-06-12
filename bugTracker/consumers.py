from channels.generic.websocket import AsyncWebsocketConsumer
import asyncio
import json
import io
from .models import Comment, Issue, User
from .serializers import CommentSerializers
from rest_framework.authtoken.models import Token
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

class CommentConsumer(AsyncWebsocketConsumer):

    async def new_message(self, data, user):
        comment = ''
        try:
           comment = data.body
        except KeyError:
            self.disconnect('comment body in not avaliable')
        new_comment = Comment.create(body=data.body, issue=issue, creater=user)
        serialized_comment = CommentSerializers(new_comment).data
        content = {
            'command': 'new_message',
            'comment': serialized_comment
        }
        data = json.dumps(content)
        await self.channel_layer.group_send(
           self.room_group_name,
           {
             'type': 'comment_message',
             'text': data
           }
        )

    async def fetch_messages(self, data):
        issue = ''
        try:
          issue = Issue.objects.get(pk = self.issue_id)
        except Issue.DoesNotExist:
          self.disconnect('Issue does not exist')

        comments = issue.comments.all().order_by("-created_at")
        serialzed_comments = CommentSerializers(comments, many=True).data
        info = JSONRenderer().render(serialzed_comments)
        stream = io.BytesIO(info)
        data = JSONParser().parse(stream)
        content = {
           "command": 'fetch_messages',
           "data": data
        }
        self.send(text_data=json.dumps(data))

    commands = {
        'fetch_messages' : fetch_messages,
        'new_message' : new_message
    }

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['issue_id']
        self.room_group_name = 'issue_'+self.room_name

        await self.channel_layer.group_add(
           self.room_group_name,
           self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
           self.room_group_name,
           self.channel_name
        )

    async def check_token(self, json_data):
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

    async def receive(self, data):
        json_data = json.loads(data)
        user = self.check_token(json_data)
        if user != 'undefined':
            try:
                command = json_data['command']
                if commonds not in self.commands.keys():
                    self.disconnect("command property not valid")
            except KeyError:
                self.disconnect("command property is not persent")
            self.commands[command](self,json_data,user)

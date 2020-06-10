from rest_framework import serializers
from bugTracker import models

#basic serializers
class ImageSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.Image
        fields = ['image']

class IssueSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.Issue
        fields = ['id','title', 'wiki', 'important', 'type', 'status', 'upload_time', 'creater', 'project']

class ProjectSerializers(serializers.ModelSerializer):  #also works for projectDetail view
    class Meta:
        model = models.Project
        fields = ['id','title', 'desc', 'gitLink', 'upload_time', 'creater', 'memebers']

class UserSerializers(serializers.ModelSerializer): #work for profile view also
    class Meta:
        model = models.User
        fields = ['id','username', 'email', 'disable','mobile', 'enroll' ,'boss', 'gitProfile', 'facebookProfile', 'instaProfile', 'twitterProfile', 'password']

class CommentSerializers(serializers.ModelSerializer):

    username = serializers.SerializerMethodField('get_username')
    member = serializers.SerializerMethodField('get_member_boolean')

    class Meta:
        model = models.Comment
        fields = ['body', 'upload_time', 'creater', 'issues', 'username', 'member']

    def get_username(self, comment):
        username = comment.creater.username
        return username

    def get_member_boolean(self, comment):
        issue = comment.issues
        project = issue.project.memebers.all()
        member = comment.creater
        if(member in project):
            return True
        else:
            return False

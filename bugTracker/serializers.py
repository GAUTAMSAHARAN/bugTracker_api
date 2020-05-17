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
        fields = ['title', 'wiki', 'important', 'type', 'status', 'upload_time', 'creater']

class ProjectSerializers(serializers.ModelSerializer):  #also works for projectDetail view
    class Meta: 
        model = models.Project
        fields = ['title', 'desc', 'gitLink', 'upload_time', 'creater', 'memebers']
 
class UserSerializers(serializers.ModelSerializer): #work for profile view also 
    class Meta:
        model = models.User
        fields = ['username', 'email', 'mobile', 'boss', 'gitProfile', 'facebookProfile', 'instaProfile', 'twitterProfile', 'password']


class CommentSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        fields = ['body', 'upload_time', 'creater']
  


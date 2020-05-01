from rest_framework import serializers
from bugTracker import models

#basic serializers
class ImageSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.Image
        fields = ['image']

class CommentSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        fields = ['body', 'upload_time']

class IssueSerializers(serializers.ModelSerializer):
    comments = CommentSerializers(many=True, read_only=True)
    class Meta:
        model = models.Issue
        fields = ['title', 'wiki', 'status', 'upload_time', 'comments']






#serizlizers based on routes
class HomeSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.Issue
        fields = ['title', 'wiki', 'important', 'type', 'status', 'upload_time', 'project']

class ProjectCategorySerializers(serizlizers.ModelSerializer):
    class Meta:
        model = models.Project
        fields = ['title', 'desc', 'gitLink', 'memebers']

class ProjectShowSerializers(serializers.ModelSerializer):
    issues = IssueSerializers(many=True, read_only=True)
    class Meta:
        model = models.Project
        fields = ['title', 'desc', 'gitLink', 'issues']

class ProfileSerializers(serializers.ModelSerializer):
    projects = ProjectSerializers(serializers.ModelSerializer)
    issues = IssueSerializers(serializers.ModelSerializer)
    comments = CommentSerializers(serializers.ModelSerializer)
    class Meta:
        model = models.User
        fields = ['username', 'gmail', 'mobile', 'fullname', 'gitProfile', 'facebookProfile', 'instaProfile', 'twitterProfile', 'projects', 'issues', 'comments']

class IssueShowSerializers(serializers.ModelSerializer):
    comments = CommentSerializers(many=True, read_only=True)
    class Meta:
        model = models.Issue
        fields = ['title', 'wiki', 'status', 'upload_time', 'comments', 'project']

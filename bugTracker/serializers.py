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

class ProjectSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.Project
        fields = ['title', 'desc', 'gitLink','upload_time', 'creater']

class UserSerializers(serializers.ModelSerializer):
    profileImage = ImageSerializers(read_only=True)
    class Meta:
        model = models.User
        fields = ['username','profileImage','username', 'fullname','mobile', 'boss', 'gitProfile', 'facebookProfile', 'instaProfile', 'twitterProfile']


#serizlizers based on routes
class HomeSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.Issue
        fields = ['title', 'wiki', 'important', 'type', 'status', 'upload_time', 'project', 'creater']

class ProjectCategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = models.Project
        fields = ['title', 'desc', 'gitLink', 'memebers', 'creater']

class ProjectShowSerializers(serializers.ModelSerializer):
    issues = IssueSerializers(many=True, read_only=True)
    memebers = UserSerializers(many=True, read_only=True)
    class Meta:
        model = models.Project
        fields = ['title', 'desc', 'gitLink', 'issues', 'memebers']

class ProfileSerializers(serializers.ModelSerializer):
    projects = ProjectSerializers(many=True, read_only=True)
    issues = IssueSerializers(many=True, read_only=True)
    comments = CommentSerializers(many=True, read_only=True)
    class Meta:
        model = models.User
        fields = ['username', 'mobile', 'fullname', 'gitProfile', 'facebookProfile', 'instaProfile', 'twitterProfile', 'projects', 'issues', 'comments']

class IssueShowSerializers(serializers.ModelSerializer):
    comments = CommentSerializers(many=True, read_only=True)
    class Meta:
        model = models.Issue
        fields = ['title', 'wiki', 'status', 'upload_time', 'comments', 'project']

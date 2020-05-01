from django.shortcuts import render
from bugTracker import models
from bugTracker import serializers
from rest_framework import generics
# Create your views here.

class Home(generics.ListCreateAPIView):
    queryset = models.Issue.objects.all()
    serializer_class = serializers.HomeSerializers

class ProjectList(generics.ListCreateAPIView):
    queryset = models.Project.objects.all()
    serializer_class = serializers.ProjectCategorySerializers

class ProjectDetail(generics.RetrieveAPIView):
    queryset = models.Project.objects.all()
    serializer_class = serializers.ProjectShowSerializers

class Profile(generics.RetrieveUpdateAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.ProfileSerializers

class IssueDetail(generics.RetrieveUpdateAPIView):
    queryset = models.Issue.objects.all()
    serializer_class = serializers.IssueShowSerializers

class UserList(generics.ListCreateAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializers

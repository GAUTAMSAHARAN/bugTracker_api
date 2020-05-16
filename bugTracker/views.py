from django.shortcuts import render
from bugTracker import models
from bugTracker import serializers
from rest_framework import generics
from bugTracker.permissions import ProjectOwner, CommentOwner, IssueOwner
from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter, OrderingFilter
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.authentication import TokenAuthentication, SessionAuthentication

# Create your views here.

class Home(generics.ListCreateAPIView):
    queryset = models.Issue.objects.all()
    serializer_class = serializers.HomeSerializers
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('important', 'creater', 'type', 'status')


class ProjectList(generics.ListCreateAPIView):
    queryset = models.Project.objects.all()
    serializer_class = serializers.ProjectCategorySerializers
    filter_backends = (filters.DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_fields = ('creater', 'memebers','upload_time')
    __base_fields = ('creater__id','memebers__id')
    search_fields = __base_fields


class ProjectDetail(generics.RetrieveUpdateAPIView):
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

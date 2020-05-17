import requests
from bugTracker import models
from rest_framework import viewsets
from bugTracker import serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter, OrderingFilter
from django.http import HttpResponse, JsonResponse,Http404
from rest_framework.permissions import IsAuthenticated, AllowAny  # <-- Here
from bugTracker.permissions import IsOwner, IsTeamMember
# from rest_framework.authentication import TokenAuthentication, SessionAuthentication  

# Create your views here.
class IssueViewSet(viewsets.ModelViewSet):
    queryset = models.Issue.objects.all()
    serializer_class = serializers.IssueSerializers
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('important', 'creater', 'type', 'status')

    permission_classes_by_action = {'create': [AllowAny],
                                    'list': [AllowAny],
                                    'update': [IsOwner],
                                    'destroy': [IsOwner],
                                    'retrieve': [AllowAny],
                                    'default': [IsOwner]}
                        
    def get_permissions(self):
        try: 
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError as e: 
            return [permission() for permission in self.permission_classes_by_action['default']]
    
    @action(methods=['get', ], detail=True, url_path='comments', url_name='comments')
    def get_comments(self, request, pk):
     try: 
         comment_list = models.Comment.objects.filter(issues=pk)
     except models.Comment.DoesNotExist:
         return Response({'empty': 'No Comment have been yet made'}, status=status.HTTP_204_NO_CONTENT)
     
     serializer = serializers.CommentSerializers(comment_list, many=True)
     return Response(serializer.data)


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = models.Project.objects.all()
    serializer_class = serializers.ProjectSerializers
    filter_backends = (filters.DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_fields = ('creater', 'memebers','upload_time')
    __base_fields = ('creater__id','memebers__id')
    search_fields = __base_fields
  
    permission_classes_by_action = {'create': [AllowAny],
                                    'list': [AllowAny],
                                    'update': [IsTeamMember],
                                    'destroy': [IsTeamMember],
                                    'retrieve': [IsTeamMember]}
    def get_permissions(self):
        try: 
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError as e: 
            return [permission() for permission in self.permission_classes_by_action['default']]

    @action(methods=['get', ], detail=True, url_path='issues', url_name='issues')   
    def get_issues(self, request, pk):
      user = request.user
      try: 
         issue_list = models.Issue.objects.filter(project=pk)
      except models.Issue.DoesNotExist:
          return Response({'empty': 'No Bugs for this project yet'}, status=status.HTTP_204_NO_CONTENT)
      
      serializer = serializers.IssueSerializers(issue_list, many=True)
      return Response(serializer.data)
    

    @action(methods=['get',], detail=True, url_path='members', url_name='members')
    def get_team_members(self, request, pk):
        project = models.Project.objects.get(pk=pk)
        member_list = project.memebers
        serializer = serializers.UserSerializers(member_list, many=True)
        return Response(serializer.data)


class UserViewSet(viewsets.ModelViewSet):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializers
    
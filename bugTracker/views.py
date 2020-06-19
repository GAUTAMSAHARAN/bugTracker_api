import requests
from bugTracker import models
from rest_framework import viewsets
from bugTracker import serializers
from rest_framework import generics, request ,mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters import rest_framework as filters
from rest_framework.authtoken.models import Token
from rest_framework.filters import SearchFilter, OrderingFilter
from django.http import HttpResponse, JsonResponse,Http404
from rest_framework.permissions import IsAuthenticated, AllowAny  # <-- Here
from bugTracker.permissions import IsOwner, IsTeamMember, CustomPermission
# from rest_framework.authentication import TokenAuthentication, SessionAuthentication

# Create your views here.

class CommentViewSet(viewsets.ModelViewSet):
    queryset = models.Comment.objects.all()
    serializer_class = serializers.CommentSerializers
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter,)
    filterset_fields = ['creater',]

class IssueViewSet(viewsets.ModelViewSet):
    queryset = models.Issue.objects.all()
    serializer_class = serializers.IssueSerializers
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter,)
    filterset_fields = ('important', 'creater', 'type', 'status', 'project')

    permission_classes_by_action = {'create': [AllowAny],
                                    'list': [AllowAny],
                                    'update': [IsOwner],
                                    'destroy': [AllowAny],
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

     @action(methods=['get', ], detail=False, url_path='my_issues', url_name='my_issues')
     def my_issues(self, request, pk):
        user = request.user
        issues = models.Issue.objects.get(user = user)
        serializer = serializers.IssueSerializers(issues, many=True)
        return Response(serializer.data)


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = models.Project.objects.all()
    serializer_class = serializers.ProjectSerializers
    filter_backends = (filters.DjangoFilterBackend, SearchFilter, OrderingFilter,)
    filterset_fields = ('creater', 'memebers','upload_time',)
    __base_fields = ('creater__id','memebers__id',)
    search_fields = __base_fields

    permission_classes_by_action = {'create': [AllowAny],
                                    'list': [AllowAny],
                                    'update': [AllowAny],
                                    'destroy': [AllowAny],
                                    'retrieve': [AllowAny],
                                    'default': [IsTeamMember]}
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


class UserViewSet(mixins.ListModelMixin,mixins.RetrieveModelMixin,mixins.UpdateModelMixin,viewsets.GenericViewSet):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializers
    filter_backends = (filters.DjangoFilterBackend, SearchFilter, OrderingFilter,)
    filterset_fields = ('boss', 'enroll', 'username', 'email',)
    __base_fields = ('enroll','username' ,'enroll', 'email',)
    search_fields = __base_fields

    @action(methods=['POST','OPTIONS', ], detail=False, url_path='login', url_name='login')
    def token(self, request):
        try:
              code = request.data['code']
        except KeyError:
            return Response('"error" Key is missing')

        #makeing post request to get the acces token and other authentication data
        token_data = {
              "client_id": "l1Wb17BXy5ZoQeJ1fzOtZutOObUrzSi9fW1xxLGR",
              "client_sercret": "lSHHesPe3SgiYsiB0PH2Bobpmsr0LZtnEtS1K3fa4m2HJwUrmIFSnrWNSSLkEbh5Sgzs0KOx4QIV9aq0wgtvy7Jlzf5SXjOrjgbqA8UWwZiXY67OPT6AO2oB8i7xVvnQ",
              "grant_type": "authorization_code",
              "redirect_url": "http://127.0.0.1:8000/users/",
              "code": code
        }

        response = requests.post('https://internet.channeli.in/open_auth/token/', data=token_data).json()

        try:
            access_token = response["access_token"]
        except KeyError:
            return Response('Your Code is Invalid')

        headers = {
            'Authorization': 'Bearer '+ access_token,
        }
        user_data = requests.get('https://internet.channeli.in/open_auth/get_user_data/', headers=headers).json()

        try:
           user = models.User.objects.get(
               email = user_data['contactInformation']['instituteWebmailAddress']
           )
           response = self.login(user, response, user_data)
        except models.User.DoesNotExist:
            user = models.User(
                username =  user_data['person']['fullName'],
                enroll = user_data['student']['enrolmentNumber'],
                email = user_data['contactInformation']['instituteWebmailAddress'],
                first_name = user_data['person']['fullName']
            )
            user.save()
            response = self.login(user, response, user_data)

        return HttpResponse(response)
 
    @action(methods=["POST"], detail=False, url_name="cookielogin", url_path="cookielogin")   
    def cookieLogIn(self, request):
        try:
            token = request.data["code"]
        except KeyError:
            return Response('error, token is missing')

        try: 
            accessToken = Token.objects.get(key=token)
        except Token.DoesNotExist:
            return Response('your token is not valid')
        
        user_data = accessToken.user
        res = {
            "token": token,
            "user_data": serializers.UserSerializers(user_data).data
        }
        return Response(res)

        

    def login(self, user, response, user_data):
        try:
            auth_token = models.AuthToken.objects.get(user = user)
            auth_token.access_token = response["access_token"]
            auth_token.revoke_token = response["refresh_token"]
            auth_token.expires_in = response["expires_in"]

        except models.AuthToken.DoesNotExist:
            auth_token = models.AuthToken(
                access_token = response["access_token"],
                revoke_token = response["refresh_token"],
                expires_in = response["expires_in"],
                user = user
            )

        try:
            token = Token.objects.get(user = user)
            token.delete()
            token = Token.objects.create(user = user)
        except Token.DoesNotExist:
            token = Token.objects.create(user = user)

        auth_token.pusedo_token = token
        auth_token.save()
        response = {
            'token': token.key,
            'user_data': user_data
        }
        return JsonResponse(response)

    def logout(self, request):
        user = request.user
        auth_token = models.AuthToken.objects.get(user = user)
        token = Token.objects.get(user = user)
        auth_token.delete()
        token.delete()
        return Response('logged out successful', status = status.HTTP_200_OK)

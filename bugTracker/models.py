from django.db import models
from django.core.validators import MinLengthValidator
from djrichtextfield.models import RichTextField
import datetime
from rest_framework.authtoken.models import Token
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
# Create your models here.


#user model
class User(AbstractUser):
    mobile = models.CharField(max_length=12, validators=[MinLengthValidator(12)])
    boss = models.BooleanField(default=False)#admin at the site level
    enroll = models.IntegerField()
    gitProfile = models.URLField(
        max_length=300,
        blank=True
    )
    facebookProfile = models.URLField(
        max_length=300,
        blank=True
    )
    instaProfile = models.URLField(
        max_length=300,
        blank=True
    )
    twitterProfile = models.URLField(
        max_length=300,
        blank=True
    )

#project models
class Project(models.Model):
    title = models.CharField(max_length=30)
    desc = models.CharField(max_length=100)
    gitLink = models.URLField(
        max_length=300,
        blank=True
    )
    upload_time = models.DateTimeField(auto_now_add = True)
    creater = models.ForeignKey(User, related_name='myprojects', on_delete=models.CASCADE)

    memebers = models.ManyToManyField("User", related_name="projects")

#issue model
class Issue(models.Model):
    TYPE_CHOICES=[
       ('FRONT','FRONTEND'),
       ('BACK', 'BACKEND')
    ]
    STATUS_CHOICES=[
        ("P","Pending"),
        ("R","Resolved"),
        ("T","To be Discussed")
    ]
    title = models.CharField(max_length=30)
    wiki = RichTextField()
    important = models.BooleanField(default=False)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES, default='BACK')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='P')
    upload_time = datetime.datetime.now()

    project = models.ForeignKey(Project, related_name = 'issues', on_delete=models.CASCADE)
    creater = models.ForeignKey(User, related_name = 'issues', on_delete=models.CASCADE)

#comment models
class Comment(models.Model):
    body = RichTextField()
    upload_time = datetime.datetime.now()

    issues = models.ForeignKey(Issue, related_name = 'comments', on_delete=models.CASCADE)
    creater = models.ForeignKey(User, related_name = 'Comments', on_delete=models.CASCADE)

#image models
class Image(models.Model):
    image = models.ImageField('Uploaded image', blank=True, null=True)

    issue = models.ForeignKey(Issue,related_name = 'image', on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, related_name = 'image', on_delete=models.CASCADE)
    user = models.OneToOneField(User, related_name = 'profileImage', on_delete=models.CASCADE)


class AuthToken(models.Model):
    access_token = models.CharField(max_length=40)
    revoke_token = models.CharField(max_length=40)
    expires_in = models.IntegerField()
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    pusedo_token = models.OneToOneField(Token, on_delete=models.SET_NULL, blank=True, null=True)
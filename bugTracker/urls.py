from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from bugTracker import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
  path('home/', views.Home.as_view()),
  path('projects/', views.ProjectList.as_view()),
  path('projects/<int:pk>/', views.ProjectDetail.as_view()),
  path('users/<int:pk>/', views.Profile.as_view()),
  path('issues/<int:pk>/', views.IssueDetail.as_view()),
  path('users/',views.UserList.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

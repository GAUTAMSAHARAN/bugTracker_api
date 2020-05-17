from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from bugTracker import views
from django.conf.urls.static import static
from django.conf import settings
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'issues', views.IssueViewSet)
router.register(r'projects', views.ProjectViewSet)
router.register(r'users', views.UserViewSet)


urlpatterns = [
    path('', include(router.urls)),
]

# urlpatterns = format_suffix_patterns(urlpatterns)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path
from bugTracker.consumers import CommentConsumer

websocket_urlpatterns = [
    re_path(r"ws/comments/(?P<issue_id>[^/]+)$",CommentConsumer),
]

application = ProtocolTypeRouter({
    # http is channels.http.AsgiHandler by default
    'websocket': AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})

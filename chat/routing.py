from django.urls import re_path
from .consumers import ChatConsumer
from django.urls import path


websocket_urlpatterns = [
    path(
        "ws/chat/<str:room_name>/<str:user_name>/",
        ChatConsumer.as_asgi()
    ),
]

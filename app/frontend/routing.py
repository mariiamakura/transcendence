from django.urls import re_path
from . import consumers
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pong.settings')


websocket_urlpatterns = [
    # re_path(r'wss/socket-server/', consumers.GameConsumer.as_asgi()),
    re_path(r'wss/socket-server/(?P<room_name>\w+)/$', consumers.GameConsumer.as_asgi()),
    re_path(r'wss/keep-alive/(?P<room_name>\w+)/$', consumers.KeepAliveConsumer.as_asgi()),
]

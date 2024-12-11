from django.urls import re_path  # This is like path() but with regex support
from . import consumers  # Import your WebSocket consumer class

# WebSocket URL patterns
websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
]

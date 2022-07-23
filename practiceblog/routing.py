from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/rooms/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
    re_path(r'ws/webrtc/(?P<room_name>\w+)/$', consumers.WebRTCConsumer.as_asgi()),
    re_path(r'ws/room_list/(?P<room_name>\w+)/$', consumers.RoomListConsumer.as_asgi()),
]
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/webcam/(?P<session_id>\w+)/$', consumers.WebcamConsumer.as_asgi()),
]
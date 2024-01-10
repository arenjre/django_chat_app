from .consumers import ChatConsumer
from django.urls import path, re_path

ws_patterns = [
    # path("ws/sync/<user_id>", mySyncConsumer.as_asgi()),
    # path("ws/async/<user_id>", myAsyncConsumer.as_asgi()),
    # re_path(r'ws/chat/(?P<group_name>\d+)/$', ChatConsumer.as_asgi()),
    path('ws/chat/<group_name>/', ChatConsumer.as_asgi()),


]

from django.urls import re_path
from .import consumers


websocket_urlpatterns =[
    re_path(r'ws/complaint/(?P<ticket_id>\d+)/$', consumers.CompliantConsumer.as_asgi())
]
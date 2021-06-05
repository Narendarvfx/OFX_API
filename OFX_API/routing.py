from django.urls import path, re_path
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from production import consumers
from channels.security.websocket import AllowedHostsOriginValidator, OriginValidator

websocket_urlPattern=[
    re_path(r'ws/projects/(?P<room_name>\w+)/$', consumers.ProductionConsumer),
    re_path(r'ws/emp/(?P<room_name>\w+)/$', consumers.ProductionConsumer),
]

application = ProtocolTypeRouter({
    'websocket':AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(websocket_urlPattern)
        )
    )
})
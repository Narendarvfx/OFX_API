from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from production import consumers
from channels.security.websocket import AllowedHostsOriginValidator, OriginValidator

websocket_urlPattern=[
    path('ws/projects/', consumers.ProductionConsumer)
]

application = ProtocolTypeRouter({
    'websocket':AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(websocket_urlPattern)
        )
    )
})
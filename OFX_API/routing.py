import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OFX_API.settings')
django_asgi_app = get_asgi_application()

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
    # Django's ASGI application to handle traditional HTTP requests
    # "http": django_asgi_app,

    # WebSocket chat handler
    'websocket':AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(websocket_urlPattern)
        )
    )
})
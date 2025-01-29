"""
ASGI config for OFX_API project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""
#  Copyright (c) 2023.
#  Designed & Developed by Narendar Reddy G, OscarFX Private Limited
#  All rights reserved.

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.urls import path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OFX_API.settings')

asgi_app = get_asgi_application()

from websockets.consumers import OfxConsumers

application = ProtocolTypeRouter({
    'http': asgi_app,
    'websocket': AuthMiddlewareStack(
        URLRouter([
            path(r'ws/data/<str:apiKey>/<str:wsToken>/', OfxConsumers.as_asgi())
        ]
        )
    )
    # 'websocket': URLRouter(
    #     websockets.routing.websockets_urlpatterns
    #     )
})

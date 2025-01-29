#  Copyright (c) 2023.
#  Designed & Developed by Narendar Reddy G, OscarFX Private Limited
#  All rights reserved.

from django.urls import path
from websockets.consumers import OfxConsumers
# from channels.auth import AuthMiddlewareStack
# from channels.routing import ProtocolTypeRouter, URLRouter
websockets_urlpatterns = [
    # path(r'ws/wsnotifications/<str:apiKey>/<str:wsToken>/',consumers_sync.ws.as_asgi()),
    path(r'ws/data/<str:apiKey>/<str:wsToken>/',OfxConsumers.as_asgi())
]
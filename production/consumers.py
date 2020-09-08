import asyncio
import json
from threading import Thread

from django.contrib.auth import get_user_model
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.consumer import  AsyncConsumer
from channels.db import database_sync_to_async
from .models import *

class ProductionConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        await self.send({
            "type":"websocket.accept"
        })

    async def websocket_receive(self, event):
        data = event.get('text', None)
        await self.send({
            "type": "websocket.send",
            "text": data
        })

    async def websocket_disconnect(self, event):
        print("disconnected", event)

    @database_sync_to_async
    def get_thread(self, user, other_username):
        return Thread.objects.get_or_new(user, other_username)[0]
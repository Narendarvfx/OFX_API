#  Copyright (c) 2023.
#  Designed & Developed by Narendar Reddy G, OscarFX Private Limited
#  All rights reserved.

import asyncio
import json
from django.contrib.auth import get_user_model
from channels.consumer import  AsyncConsumer
from channels.db import database_sync_to_async
from .models import *

class HrmConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print("connected", event)
        await self.send({
            "type": "websocket.accept"
        })
        other_user = 'dharan'
        me = self.scope['user']
        print(other_user, me)
        thread_obj = await self.get_thread(me, other_user)
        print(thread_obj)
        await asyncio.sleep(3)
        await self.send({
            "type": "websocket.send",
            "text": "Hello Narendar"
        })
        await asyncio.sleep(3)
        await self.send({
            "type": "websocket.send",
            "text": "Hey Hai"
        })
        await asyncio.sleep(3)
        await self.send({
            "type": "websocket.send",
            "text": "What are you looking for"
        })

    async def websocket_recieve(self, event):
        print("recieve", event)

    async def websocket_disconnect(self, event):
        print("disconnected", event)

    @database_sync_to_async
    def get_thread(self, user, other_username):
        return Thread.objects.get_or_new(user, other_username)[0]
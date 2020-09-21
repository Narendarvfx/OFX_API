# import asyncio
# import json
# from threading import Thread
#
# from django.contrib.auth import get_user_model
# from channels.generic.websocket import AsyncWebsocketConsumer
# from channels.consumer import  AsyncConsumer
# from channels.db import database_sync_to_async
# from .models import *
#
# class ProductionConsumer(AsyncConsumer):
#     async def websocket_connect(self, event):
#         await self.send({
#             "type":"websocket.accept"
#         })
#
#     async def websocket_receive(self, event):
#         data = event.get('text', None)
#         await self.send({
#             "type": "websocket.send",
#             "text": data
#         })
#
#     async def websocket_disconnect(self, event):
#         print("disconnected", event)
#
#     @database_sync_to_async
#     def get_thread(self, user, other_username):
#         return Thread.objects.get_or_new(user, other_username)[0]

import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ProductionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        pass

    # Receive message from WebSocket
    async def receive(self, text_data):
        print("Recieved")
        print(text_data)
        text_data_json = json.loads(text_data)
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': text_data_json
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'Name': message['Name'],
            'message': message['message']
        }))
#  Copyright (c) 2023.
#  Designed & Developed by Narendar Reddy G, OscarFX Private Limited
#  All rights reserved.

# from http import client
# from time import sleep
# import asyncio
# from typing import Tuple
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
# from channels.layers import get_channel_layer
import json

from websockets.wsManage import wsManage

wsManageX = wsManage()
users = {}
groups = {}
# print("groups",wsManageX.getGroupData('x26rwdmqcy73kcriajb5zef1g2p9vnrn'))
class OfxConsumers(AsyncJsonWebsocketConsumer):
    async def connect(self):
        apiKey = self.scope["url_route"]["kwargs"].get('apiKey','')
        wsToken = self.scope["url_route"]["kwargs"].get('wsToken','')
        oath = await sync_to_async(wsManageX.oathUser, thread_sensitive=True)(apiKey,wsToken)
        if oath.get('status',False):
            for x in oath.get('groups',{}):
                if x not in groups:
                    groups[x] = []
                if apiKey not in groups[x]:
                    groups[x].append(apiKey)
            if apiKey not in users:
                users[apiKey] = {}
            users[apiKey][wsToken] = self.channel_name
            await self.channel_layer.group_add(
                apiKey,
                self.channel_name
                )
            await self.accept()
            # await self.send(text_data=json.dumps({
            #     "status": 'conncetd',
            #     'message': 'Conncetd Successfully',
            #     'connectedWith': {
            #         "apiKey": apiKey,
            #         "wsToken": wsToken,
            #         "users": users,
            #         # "oath": oath,
            #         "groups": groups
            #     }
            # }))
            await self.send(text_data=json.dumps({
                "status":'conncetd',
                'message':'Conncetd Successfully',
                "userData": oath.get('user', {}),
                "groups": oath.get('groups', {}),
                # 'connectedWith':{
                #     "apiKey":apiKey,
                #     "wsToken":wsToken,
                #     "users":users,
                #     "oath": oath,
                #     "groups":groups
                #     }
                }))
            await self.sendClientStatus(apiKey,isOnline=True)
        else:
            await self.close()

    async def disconnect(self, code):
        apiKey = self.scope["url_route"]["kwargs"].get('apiKey','')
        wsToken = self.scope["url_route"]["kwargs"].get('wsToken','')
        await self.channel_layer.group_discard(apiKey, self.channel_name)
        del users[apiKey][wsToken]
        if len(users[apiKey])==0:
            del users[apiKey]
            for x in groups:
                if apiKey in groups[x]:
                    groups[x].remove(apiKey)
        await self.sendClientStatus(apiKey,isOnline=False)
        # for gname in users:
        #     await self.channel_layer.group_send(gname,{
        #         'type': 'sendMessage',
        #         'message': {
        #             "status":'info',
        #             "code":code,
        #             'message':'Device Disconnected',
        #             "users": users,
        #             "groups": groups
        #             }
        #         })

    async def receive(self, text_data=None, bytes_data=None):
        apiKey = self.scope["url_route"]["kwargs"].get('apiKey','')
        # wsToken = self.scope["url_route"]["kwargs"].get('wsToken','')
        data = json.loads(text_data)
        # print('data',data)
        # print("users",users)
        # print("groups",groups)
        dataId = data.get('dataId',wsManageX.getRandomStrings(32))
        saveData = data.get('__SAVE__',None)
        if saveData is not None:
            dxrds = data.get('data',{})
            await sync_to_async(wsManageX.saveData, thread_sensitive=True)(apiKey,dxrds.get('fromGroup',''),data.get('targetUsers',[]),data.get('targetGroups',[]),saveData)
        userInfo = await sync_to_async(wsManageX.getUserData, thread_sensitive=True)(apiKey,False)
        message = {
            "from": apiKey,
            "fromUser": userInfo,
            "type": data.get('type',"data"),
            "dataId": dataId,
            "target":"user",
            "data": data.get('data',{})
            }
        for userId in data.get('targetUsers',[]):
            msg = message
            msg['toUser'] = await sync_to_async(wsManageX.getUserData, thread_sensitive=True)(userId, False)
            await self.sendToClient(userId,msg,True)
        message["target"] = "group"
        for gropuId in data.get('targetGroups',[]):
            msg = message
            # msg['fromGroup'] = await sync_to_async(wsManageX.getGroupData, thread_sensitive=True)(msg.data.get('fromGroup',''), False)
            # msg['toGroup'] = await sync_to_async(wsManageX.getGroupData, thread_sensitive=True)(gropuId, False)
            msg["targetGroup"] = gropuId
            await self.sendToGroup(gropuId,msg)

    async def sendClientStatus(self,apiKey,isOnline=True):
        dataId = wsManageX.getRandomStrings(10)
        for us in users:
            await self.channel_layer.group_send(us,{
                'type': 'sendMessage',
                'message': {
                    "status":'clientonline' if isOnline is True else 'clientoffline',
                    'clientId': apiKey,
                    "dataId": dataId,
                    }
                })

    async def sendToClient(self,to='apiKey',message={},feedback=False):
        # print('Tas',to)
        if to in users:
            # print(to)
            await self.channel_layer.group_send(to,{
                'type': 'sendMessage',
                'message': message
                })
        else:
            if feedback:
                await self.send(text_data=json.dumps({
                    "status":'clientoffline',
                    'clientId': to,
                    "dataId": message["dataId"],
                    }))

    async def sendToGroup(self,to='gropuId',message={}):
        if to in groups:
            for x in groups[to]:
                await self.sendToClient(x,message,False)
    
    async def sendMessage(self,event):
        await self.send(text_data=json.dumps(event['message']))
#  Copyright (c) 2023.
#  Designed & Developed by Narendar Reddy G, OscarFX Private Limited
#  All rights reserved.

from django.shortcuts import render
from django.http import HttpResponse
from websockets.wsManage import wsManage
wsManage = wsManage()
def homePage(request):
    return render(request,'index.html',{
        "name":'Human',
        'users': wsManage.users,
        'groups': wsManage.groups
        })
#  Copyright (c) 2023.
#  Designed & Developed by Narendar Reddy G, OscarFX Private Limited
#  All rights reserved.

import json
from django.http import HttpResponse
from websockets.wsManage import wsManage
wsManage = wsManage()
# Create your views here.
def getwstoken(request):
    apiKey = request.GET.get('apiKey', '')
    if apiKey in wsManage.users:
        return HttpResponse(json.dumps({'status':'success', 'wsToken':wsManage.genarateWSToken(10)}))
    else:
        return HttpResponse(json.dumps({'status':'failed', 'message':'Unknown Client'}))
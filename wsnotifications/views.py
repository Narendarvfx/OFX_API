#  Copyright (c) 2023.
#  Designed & Developed by Narendar Reddy G, OscarFX Private Limited
#  All rights reserved.

import json
import os
from io import BytesIO

from django.http import FileResponse
from django.shortcuts import render

from wsnotifications.models import Attachments
from wsnotifications.serializers import AttachmentCompactSerializer


# Create your views here.
def notifications(request):
    return render(request, 'notifications/notifications.html')

# Create your views here.
def notifications_view(request):
    return render(request, 'notifications/notificationsview.html')

def notes_download_attachment(request, file_id):
    attachments = Attachments.objects.get(pk=file_id)
    ser = AttachmentCompactSerializer(attachments)

    _data = ser.data
    buf = ""
    with open('.'+_data['files'], "rb") as fh:
        buf = BytesIO(fh.read())

    return FileResponse(buf, as_attachment=True, filename=_data['file_name'])

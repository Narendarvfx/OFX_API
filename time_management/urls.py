#  Copyright (c) 2023.
#  Designed & Developed by Narendar Reddy G, OscarFX Private Limited
#  All rights reserved.
from django.conf.urls import url

from time_management import api, views

urlpatterns = [
    url(r'^api/backend/time_management/$', api.TimingData.as_view(), name='Time Management API'),
]
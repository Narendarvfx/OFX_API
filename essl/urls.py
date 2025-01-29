#  Copyright (c) 2023.
#  Designed & Developed by Narendar Reddy G, OscarFX Private Limited
#  All rights reserved.

from django.conf.urls import url

from . import api

urlpatterns = [
    url(r'^api/essl/attendance/$', api.EsslDetail.as_view(), name='ESSL API')
]
#  Copyright (c) 2023.
#  Designed & Developed by Narendar Reddy G, OscarFX Private Limited
#  All rights reserved.

from django.conf.urls import url

from . import api

urlpatterns = [
    url(r'^api/EmployeeDailyStatistics/$', api.Ofxstatistics.as_view(), name='OFX Employee Daily Statistics'),
    url(r'^api/TeamLeadDailyStatistics/$', api.teamLeaadstatistics.as_view(), name='Team Lead Daily Statistics'),
    url(r'^api/ClientStatistics/$', api.ClientStatisticsAPI.as_view(), name="Client Statistics"),
    url(r'^api/LeadDailyStatistics/$', api.leadstatistics.as_view(), name='Lead Daily Statistics')
    ]


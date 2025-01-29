#  Copyright (c) 2022-2023.
#  Designed & Developed by Narendar Reddy G, OscarFX Private Limited
#  All rights reserved.
from django.conf.urls import url

from ofx_dashboards import api, views

urlpatterns = [
    url(r'^api/production/mandayavailabilty/$', api.MandayAvailabilityView.as_view(), name='Manday Availability'),
    url(r'^api/production/waitingforbids/$', api.WaitingforBidView.as_view(), name='Waiting For Bid'),
]

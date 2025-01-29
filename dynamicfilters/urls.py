from django.conf.urls import url
from . import api

urlpatterns = [
    ########## API Dynamic Filters URLS #################
    url(r'^api/dynamicfilters/status/$', api.Dynamicfilters.as_view(), name='Status API'), 
]
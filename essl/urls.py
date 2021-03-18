from django.conf.urls import url

from . import api

urlpatterns = [
    url(r'^api/essl/attendance/$', api.EsslDetail.as_view(), name='ESSL API')
]
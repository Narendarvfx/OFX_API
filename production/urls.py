from django.conf.urls import url
from . import api

urlpatterns = [
    url(r'^api/production/clients/$', api.ClientDetail.as_view(), name='Client API'),
]
from django.conf.urls import url
from . import api, views

urlpatterns = [
    # Shot History  urls
    url(r'^api/history/shot/$', api.ShotHistoryAPI.as_view(), name="Shots History"),
    ]
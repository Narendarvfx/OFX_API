from django.conf.urls import url
from . import api, views

urlpatterns = [
    url(r'^shotassignments/$', views.shotAssignmentsUI, name='Shot Assignments UI'),
    url(r'^api/shotassignments/$', api.shotAssignmentsOrders.as_view(), name='Shot Assignments Orders'),
    url(r'^api/setshotassignmentorder/$', api.setshotAssignmentsOrders.as_view(), name='Shot Assignments Orders'),
    ]
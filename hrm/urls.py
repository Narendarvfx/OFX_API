from django.conf.urls import url
from . import api

urlpatterns = [
    url(r'^api/hrm/employee/(?P<profile_id>\d+)/$', api.EmployeeDetail.as_view(), name='Employee details'),
]
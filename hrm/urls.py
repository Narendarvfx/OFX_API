from django.conf.urls import url
from . import api

urlpatterns = [
    url(r'^api/hrm/employee/(?P<profile_id>\d+)/$', api.EmployeeDetail.as_view(), name='Employee details'),
    url(r'^api/hrm/employee/$', api.AllEmployeeDetail.as_view(), name='All Employee details'),
    url(r'api/hrm/teams/$', api.AllTeams.as_view(), name='All Team Details')
]
from django.conf.urls import url
from . import api

urlpatterns = [
    url(r'^api/hrm/employee/(?P<profile_id>\d+)/$', api.EmployeeDetail.as_view(), name='Employee details'),
    url(r'^api/hrm/employee/$', api.AllEmployeeDetail.as_view(), name='All Employee details'),
    url(r'api/hrm/teams/$', api.AllTeams.as_view(), name='All Team Details'),
    url(r'api/hrm/permissions', api.AllPermissions.as_view(), name= 'Role Permissions'),
    url(r'api/hrm/role/permissions/(?P<role_id>\d+)/$', api.RolePermissions.as_view(), name=" Role Permissions by ID" )
]
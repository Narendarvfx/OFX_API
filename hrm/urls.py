#  Copyright (c) 2023.
#  Designed & Developed by Narendar Reddy G, OscarFX Private Limited
#  All rights reserved.

from django.conf.urls import url

from . import api, views

urlpatterns = [

    ### Profile urls
    url(r'^login', views.login_view, name='login'),
    url(r'^logout', views.logout_view, name='logout'),
    url(r'^api/users/$', api.UserList.as_view(), name='user_list_api'),
    url(r'^api/users/(?P<user_id>\d+)$', api.UserEdit.as_view()),
    url(r'^api/profile/(?P<profile_id>\d+)$', api.UserProfileAPIView.as_view()),
    url(r'^api/auth/$', api.UserAuthentication.as_view(), name='User Authentication API'),
    url(r'^api/user/password_change/(?P<user_id>\d+)$', api.UpdatePassword.as_view(), name='User Update Password API'),
    url(r'^profile/password_change/$', views.change_password, name='User Update Password View'),
    url(r'^profile/', views.profile_view, name='profile'),
    url(r'^api/token/user/', api.TokenUser.as_view(), name='Token User'),
    #####
    url(r'^api/myaccount/$', api.MyAccount.as_view(), name='my_account_api'),
    url(r'^api/hrm/employee/(?P<profile_id>\d+)/$', api.EmployeeDetail.as_view(), name='Employee details'),
    url(r'^api/hrm/myprofile/(?P<id>\d+)/$', api.MyProfileDetail.as_view(), name='MyProfile details'),
    url(r'^api/hrm/employee/$', api.AllEmployeeDetail.as_view(), name='All Employee details'),
    url(r'^api/hrm/employeerolebinding/$',api.employee_role_binding.as_view(), name="Artist Role Binding"),
    url(r'^api/hrm/employeerolebinding/(?P<id>\d+)/$',api.employee_role_binding.as_view(), name="Artist Role Binding"),
    url(r'^api/hrm/grades/', api.AllGrades.as_view(), name="All Grades"),
    url(r'^api/hrm/locations/', api.AllLocation.as_view(), name="All Locations"),
    url(r'^api/hrm/departments/', api.AllDepartments.as_view(), name="All Grades"),
    url(r'^api/hrm/role/', api.AllRole.as_view(), name="Role"),
    url(r'api/hrm/teams/$', api.AllTeams.as_view(), name='All Team Details'),
    url(r'api/hrm/leads/$', api.DeptLeads.as_view(), name='Get Dept Lead Details'),
    url(r'api/hrm/teams/(?P<id>\d+)/$', api.TeamById.as_view(), name='All Team Details'),
    url(r'api/hrm/permissions', api.AllPermissions.as_view(), name='Role Permissions'),
    url(r'api/hrm/role/role_permissions/(?P<role_id>\d+)/$', api.RolePermissions.as_view(), name=" Role Permissions by ID"),
    url(r'^hrm/employeelist/', views.employee_view, name='employeelist'),
    url(r'^hrm/leaves/', views.leaves_view, name='employeelist'),
    url(r'^hrm/my_record/', views.my_record_view, name='employeelist'),


    ##Leaves
    url(r'api/hrm/leaves/$', api.LeavesData.as_view(), name="Get Leaves"),

    ## Attendance
    url(r'api/hrm/attendance/$', api.AttendanceData.as_view(), name="Get Attendance"),

    ## For Backend Scripts
    ## Leaves
    url(r'api/backend/hrm/leaves/$', api.LeavesData.as_view(), name="Get Leaves"),
    url(r'api/backend/hrm/attendance/$', api.AttendanceData.as_view(), name="Get Attendance"),

    ##Organization Calendars
    url(r'api/calendar/holidays/$', api.HolidaysDataApi.as_view(), name="Get Holidays"),
    url(r'api/calendar/workingdayTypes/$', api.WorkingDayTypesApi.as_view(), name="Get Working Day Types"),
    url(r'api/calendar/deptworkingdays/$', api.DepartmentWorkingDaysApi.as_view(), name="Get Dept Working Days"),
    url(r'api/calendar/empworkingdays/$', api.EmpWorkingDaysApi.as_view(), name="Get Employee Working Days"),
    url(r'api/calender/orgworkingdays/$', api.OrgWorkingdays.as_view(), name="Get Organization Working Days"),
]




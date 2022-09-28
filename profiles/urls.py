from django.conf.urls import url
from . import api, views
from django.urls import path
urlpatterns = [
    url(r'^login', views.login_view, name='login'),
    url(r'^logout', views.logout_view, name='logout'),
    url(r'^api/users/$', api.UserList.as_view(), name='user_list_api'),
    url(r'^api/users/(?P<user_id>\d+)$', api.UserEdit.as_view()),
    url(r'^api/profile/(?P<profile_id>\d+)$', api.UserProfileAPIView.as_view()),
    url(r'^api/auth/$', api.UserAuthentication.as_view(), name='User Authentication API'),
    url(r'^api/user/password_change/(?P<user_id>\d+)$', api.UpdatePassword.as_view(), name='User Update Password API'),
    url(r'^profile/password_change/$', views.change_password, name='User Update Password View'),
    url(r'^profile/', views.profile_view, name='profile'),
]
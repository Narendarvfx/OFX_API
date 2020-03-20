from django.conf.urls import url
from . import api

urlpatterns = [
    url(r'^api/users/$', api.UserList.as_view(), name='user_list_api'),
    url(r'^api/users/(?P<user_id>\d+)$', api.UserEdit.as_view()),
    url(r'^api/profile/(?P<profile_id>\d+)$', api.UserProfileAPIView.as_view()),
    url(r'^api/auth/$', api.UserAuthentication.as_view(), name='User Authentication API'),
]
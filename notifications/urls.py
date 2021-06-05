from django.conf.urls import url

from notifications import api

urlpatterns = [
    url(r'^api/notifications/$', api.NotificationsDetail.as_view(), name='Notifications API'),
    url(r'^api/notifications/unread/(?P<userId>\d+)/$', api.NotificationsUnread.as_view(), name='Notifications API'),
    ]
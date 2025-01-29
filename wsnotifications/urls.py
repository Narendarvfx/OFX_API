#  Copyright (c) 2023.
#  Designed & Developed by Narendar Reddy G, OscarFX Private Limited
#  All rights reserved.

from django.conf.urls import url

from wsnotifications import api, views

urlpatterns = [
    url(r'^notifications/$', views.notifications, name='Notifications'),
    url(r'^notifications/view/$', views.notifications_view, name='Notifications View'),
    url(r'^api/wsnotifications/notes/$', api.WsNotificationNotes.as_view(), name='Notes Logs API'),
    url(r'^api/wsnotifications/notes/details/$', api.WsNotificationNotesDetails.as_view(), name='Notes Details API'),
    url(r'^api/wsnotifications/notificationlogs/$', api.WsNotificationLogsAPI.as_view(), name='Notifications Logs API'),
    url(r'^attachments/notes/download/(?P<file_id>\d+)/$', views.notes_download_attachment, name='Notes Attachments Download'),
    url(r'^api/notify/shot_targets/$', api.ShotsTargetsListAPI.as_view(), name='Notify API'),

    url(r'^api/notifications/$', api.UserNotificationTagsAPI.as_view(), name='User Notifications API'),

    # url(r'^api/wsnotifications/$', api.NotificationsDetail.as_view(), name='Notifications API'),
    # url(r'^api/wsnotifications/unread/(?P<userId>\d+)/$', api.NotificationsUnread.as_view(), name='Notifications API'),
]

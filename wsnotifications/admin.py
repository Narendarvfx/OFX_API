#  Copyright (c) 2023.
#  Designed & Developed by Narendar Reddy G, OscarFX Private Limited
#  All rights reserved.

from django.contrib import admin

# Register your models here.
from wsnotifications.models import Notifications, NotificationLogs, NotifyTypes, Attachments, UserNotificationLogs, \
    UserNotificationTags


class NotificationFields(admin.ModelAdmin):
    list_display = [f.name for f in Notifications._meta.fields]

class NotifyTypesFields(admin.ModelAdmin):
    list_display = [f.name for f in NotifyTypes._meta.fields]

class UserNotificationTagFields(admin.ModelAdmin):
    list_display = [f.name for f in UserNotificationTags._meta.fields]

class NotificationLogsFields(admin.ModelAdmin):
    list_display = [f.name for f in NotificationLogs._meta.fields]
class AttachmentsFields(admin.ModelAdmin):
    list_display = [f.name for f in Attachments._meta.fields]

admin.site.register(Notifications, NotificationFields)
admin.site.register(NotifyTypes, NotifyTypesFields)
admin.site.register(Attachments, AttachmentsFields)
admin.site.register(NotificationLogs, NotificationLogsFields)
admin.site.register(UserNotificationLogs)
admin.site.register(UserNotificationTags, UserNotificationTagFields)
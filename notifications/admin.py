from django.contrib import admin

# Register your models here.
from notifications.models import Shot_Notifications

class NotificationFields(admin.ModelAdmin):
    list_display = [f.name for f in Shot_Notifications._meta.fields]

admin.site.register(Shot_Notifications, NotificationFields)
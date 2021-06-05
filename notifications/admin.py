from django.contrib import admin

# Register your models here.
from notifications.models import Notifications

class NotificationFields(admin.ModelAdmin):
    list_display = [f.name for f in Notifications._meta.fields]

admin.site.register(Notifications, NotificationFields)
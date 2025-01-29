#  Copyright (c) 2023.
#  Designed & Developed by Narendar Reddy G, OscarFX Private Limited
#  All rights reserved.

import os
import random
import string

import model_utils
from django.db import models, transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from OFX_API import getRandomStrings
from hrm.models import Employee, EmployeeGroups
from production.models import Shots

# Create your models here.
class Notifications(models.Model):
    message = models.CharField(max_length=1000, null=True, blank=True)
    status = models.CharField(max_length=100, null=True, blank=True)
    read = models.BooleanField(default=False)
    by = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='+', null=True, blank=True)
    to = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='+', null=True, blank=True)
    sent_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Notifications"

class NotifyTypes(models.Model):
    name = models.CharField(max_length=10, null=True)

    class Meta:
        verbose_name_plural = "NotifyTypes"

class Attachments(models.Model):
    def _upload_to(instance, filename):
        type = filename.split('.')
        type = "" if len(type) == 1 else type[-1]
        name = "{name}.{format}".format(
            name=''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=20)),
            format=type)
        return os.path.join('attachments/', name)

    files = models.FileField(upload_to=_upload_to, blank = True, null = True)
    file_name = models.CharField(max_length=1024, null=True, blank=True)
    file_size = models.IntegerField(default=0)
    file_type = models.CharField(max_length=50, null=True, blank=True)
    content_type = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.file_name

    class Meta:
        verbose_name_plural = "Attachments"

class NotificationLogs(models.Model):
    dataId = models.CharField(max_length=32, default=getRandomStrings, primary_key=True)
    referenceId = models.IntegerField(null=True, blank=True) ## ShotId/TASKID/etc..
    reference_type = models.ForeignKey(NotifyTypes, on_delete=models.CASCADE, null=True, blank=True)
    from_group_key = models.ForeignKey(EmployeeGroups, on_delete=models.CASCADE, related_name='+', null=True, blank=True)
    from_user_apikey = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='+', null=True, blank=True)
    from_user = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='+', null=True, blank=True)
    to_users = models.ManyToManyField(Employee, blank=True, related_name='+')
    to_groups = models.ManyToManyField(EmployeeGroups, blank=True)
    message_title = models.CharField(max_length=2048, null=True, blank=True)
    message = models.CharField(max_length=2048, null=True, blank=True)
    attachments = models.ManyToManyField(Attachments, blank=True)
    read_recipients = models.ManyToManyField(Employee,blank=True, related_name='+')
    creation_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "NotificationLogs"

class UserNotificationLogs(models.Model):
    NotificationStatus = (
        (0, "UnDelivered"),
        (1, "Delivered"),
        (2, "Read")
    )
    user = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, blank=True)
    notify_id = models.ForeignKey(NotificationLogs, on_delete=models.CASCADE, null=True, blank=True)
    read_status = models.CharField(max_length=300, null=True, blank=True, choices=NotificationStatus, default=NotificationStatus[0][0])

    class Meta:
        verbose_name_plural = "UserNotificationLogs"


class UserNotificationTags(models.Model):
    user_id = models.ForeignKey(Employee, on_delete=models.CASCADE,null=True, blank=True)
    notify_id = models.ForeignKey(NotificationLogs, on_delete=models.CASCADE, null=True, blank=True)
    read = models.BooleanField(default=False)
    creation_date = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name_plural = "UserNotificationTags"








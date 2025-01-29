#  Copyright (c) 2023.
#  Designed & Developed by Narendar Reddy G, OscarFX Private Limited
#  All rights reserved.

import uuid

from django.db import models

from hrm.models import Employee


# Create your models here.
class TimeLogType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=30, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Time Log Type"

class TimeManagement(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, blank=True, related_name='+', null=True)
    logType = models.ForeignKey(TimeLogType, on_delete=models.CASCADE, blank=True, related_name='+', null=True)
    logDate = models.DateField(auto_now_add=True, null=True, blank=True)
    logTime = models.TimeField(auto_now_add=True, null=True, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Time Management"
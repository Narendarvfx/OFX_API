#  Copyright (c) 2023.
#  Designed & Developed by Narendar Reddy G, OscarFX Private Limited
#  All rights reserved.

from django.db import models

# Create your models here.
from hrm.models import Employee


class Attendance(models.Model):
    # user =models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='+', null=True, blank=True)
    employee_id = models.CharField(max_length=10, null=True, blank=True)
    punch_type = models.CharField(max_length=10, null=True, blank=True)
    punch_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.employee_id

    class Meta:
        verbose_name_plural = "Attendance"


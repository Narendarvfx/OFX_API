from django.db import models

from hrm.models import Employee
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

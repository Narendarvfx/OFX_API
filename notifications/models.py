from django.db import models

from hrm.models import Employee
from production.models import Shots

# Create your models here.
class Shot_Notifications(models.Model):
    shot = models.ForeignKey(Shots, on_delete=models.CASCADE, related_name='+', null=True, blank=True)
    message = models.CharField(max_length=1000, null=True, blank=True)
    sent_by = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='+', null=True, blank=True)
    sent_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.shot.name

    class Meta:
        verbose_name_plural = "Shot Notifications"

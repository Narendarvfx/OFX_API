#  Copyright (c) 2023.
#  Designed & Developed by Narendar Reddy G, OscarFX Private Limited
#  All rights reserved.

from django.db import models

from hrm.models import Employee, Department

# Create your models here.
class MandayAvailability(models.Model):
    teamlead = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, blank=True)
    dep = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    mtd_target = models.FloatField(default=0, null=True, blank=True)
    mtd_actuals = models.FloatField(default=0, null=True, blank=True)
    w1_target = models.FloatField(default=0, null=True, blank=True)
    w2_target = models.FloatField(default=0, null=True, blank=True)
    w3_target = models.FloatField(default=0, null=True, blank=True)
    w4_target = models.FloatField(default=0, null=True, blank=True)
    w5_target = models.FloatField(default=0, null=True, blank=True)
    w1_achieved_mandays = models.FloatField(default=0, null=True, blank=True)
    w2_achieved_mandays = models.FloatField(default=0, null=True, blank=True)
    w3_achieved_mandays = models.FloatField(default=0, null=True, blank=True)
    w4_achieved_mandays = models.FloatField(default=0, null=True, blank=True)
    w5_achieved_mandays = models.FloatField(default=0, null=True, blank=True)
    w1_pending_mandays = models.FloatField(default=0, null=True, blank=True)
    w2_pending_mandays = models.FloatField(default=0, null=True, blank=True)
    w3_pending_mandays = models.FloatField(default=0, null=True, blank=True)
    w4_pending_mandays = models.FloatField(default=0, null=True, blank=True)
    w5_pending_mandays = models.FloatField(default=0, null=True, blank=True)
    date = models.DateField(auto_now=True)

    class Meta:
        verbose_name_plural = "MandayAvailability"

class WaitingForBids(models.Model):
    dep = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    w1 = models.FloatField(default=0, null=True, blank=True)
    w2 = models.FloatField(default=0, null=True, blank=True)
    w3 = models.FloatField(default=0, null=True, blank=True)
    w4 = models.FloatField(default=0, null=True, blank=True)
    w5 = models.FloatField(default=0, null=True, blank=True)
    updated_by = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField(auto_now=True)

    class Meta:
        verbose_name_plural = "WaitingForBids"
#  Copyright (c) 2023.
#  Designed & Developed by Narendar Reddy G, OscarFX Private Limited
#  All rights reserved.

import uuid

from django.db import models

from hrm.models import Employee, Role
from production.models import Clients, Task_Type, Projects


# Create your models here.

class EmployeeDailyStatistics(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, blank=True)
    tmd = models.FloatField(default=0) #Target Mandays
    amd = models.FloatField(default=0) #Achieved Mandays
    rwh = models.FloatField(default=0) #Required Working Hours
    aeh = models.FloatField(default=0) #Available ESSL Hours
    ash = models.FloatField(default=0) #Active System Hours
    leaves = models.FloatField(default=0) #It can be 0.5days
    logDate = models.DateField(blank=True, null=True)
    creation_date = models.DateField(auto_now_add=True, blank=True, null=True)
    modified_date = models.DateField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.employee.fullName
    class Meta:
        verbose_name_plural = "EmployeeDailyStatistics"
class TLDailyStatistics(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    tl = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, blank=True)
    artists = models.ManyToManyField(Employee, blank=True, related_name='+')
    artists_count = models.IntegerField(default=0)
    total_workdays = models.FloatField(default=0)
    team_ability = models.FloatField(default=0)
    tmd = models.FloatField(default=0) #Target Mandays
    amd = models.FloatField(default=0) #Achieved Mandays will be sum of consumed_mandays from Artist Statistic Day Logs
    shot_amd = models.FloatField(default=0) #Achieved Mandays will be sum of consumed_mandays from Shot Day Logs
    rwh = models.FloatField(default=0) #Required Working Hours
    aeh = models.FloatField(default=0) #Available ESSL Hours
    ash = models.FloatField(default=0) #Active System Hours
    leaves = models.FloatField(default=0) #It can be 0.5days
    logDate = models.DateField(blank=True, null=True)
    creation_date = models.DateField(auto_now_add=True, blank=True, null=True)
    modified_date = models.DateField(auto_now=True, blank=True, null=True)

    class Meta:
        verbose_name_plural = "TLDailyStatistics"

class LeadDailyStatistics(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    lead = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, blank=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='+', null=True)
    artists = models.ManyToManyField(Employee, blank=True, related_name='+')
    artists_count = models.IntegerField(default=0)
    total_workdays = models.FloatField(default=0)
    team_ability = models.FloatField(default=0)
    tmd = models.FloatField(default=0) #Target Mandays
    amd = models.FloatField(default=0) #Achieved Mandays will be sum of consumed_mandays from Artist Statistic Day Logs
    shot_amd = models.FloatField(default=0) #Achieved Mandays will be sum of consumed_mandays from Shot Day Logs
    rwh = models.FloatField(default=0) #Required Working Hours
    aeh = models.FloatField(default=0) #Available ESSL Hours
    ash = models.FloatField(default=0) #Active System Hours
    leaves = models.FloatField(default=0) #It can be 0.5days
    logDate = models.DateField(blank=True, null=True)
    creation_date = models.DateField(auto_now_add=True, blank=True, null=True)
    modified_date = models.DateField(auto_now=True, blank=True, null=True)

    class Meta:
        verbose_name_plural = "LeadDailyStatistics"

class ClientStatistics(models.Model):
    client = models.ForeignKey(Clients, on_delete=models.CASCADE, related_name='+')
    project = models.ForeignKey(Projects, on_delete=models.CASCADE, related_name='+')
    dep = models.ForeignKey(Task_Type, on_delete=models.CASCADE, related_name='+')
    tmd = models.FloatField(default=0)
    amd = models.FloatField(default=0)
    highest_ver = models.IntegerField(default=0)
    highest_ver_shotCount = models.IntegerField(default=0)
    retake_per = models.FloatField(default=0)
    artistcount = models.IntegerField(default=0)
    artistTMD = models.FloatField(default=0)  ##PerDay
    missedEta = models.IntegerField(default=0)
    totalshots = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = "Client Statistics"

class ClientArtistStatistics(models.Model):
    client = models.ForeignKey(Clients, on_delete=models.CASCADE, related_name='+')
    project = models.ForeignKey(Projects, on_delete=models.CASCADE, related_name='+')
    dep = models.ForeignKey(Task_Type, on_delete=models.CASCADE, related_name='+')
    artist = models.ForeignKey(Employee, on_delete=models.CASCADE,related_name='+')
    tl = models.ForeignKey(Employee, on_delete=models.CASCADE,related_name='+')
    supervisor = models.ForeignKey(Employee, on_delete=models.CASCADE,related_name='+')
    hod = models.ForeignKey(Employee, on_delete=models.CASCADE,related_name='+')
    tmd = models.FloatField(default=0)
    amd = models.FloatField(default=0)
    shotsCount = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = "Client Artist Statistics"

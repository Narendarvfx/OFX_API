import uuid

from django.db import models

from hrm.models import Role, Location, Department, Employee
from production.models import Task_Type, ShotStatus

# Create your models here.
class AssignmentsRoles(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='+', blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='+', blank=True, null=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='+', blank=True, null=True)
    shotStatus = models.ForeignKey(ShotStatus, on_delete=models.CASCADE, related_name='+', blank=True, null=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='+', blank=True, null=True)
    roleIndex = models.PositiveSmallIntegerField(blank=True, null=True, default=0) #indexing for front end assignments form Ex: Supervisor after TL
    created_by = models.ForeignKey(Employee, on_delete=models.CASCADE, blank=True, related_name='+', null=True)
    updated_by = models.ForeignKey(Employee, on_delete=models.CASCADE, blank=True, related_name='+', null=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.location.name+'_'+self.department.name+'_'+self.role.name if self.employee is None else self.employee.fullName
    
    class Meta:
        verbose_name_plural = "AssignmentsRoles"

class ShotAssignmentsOrder(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='+', null=True, blank=True)
    department = models.ForeignKey(Task_Type, on_delete=models.CASCADE, related_name='+')
    shotStatus = models.ForeignKey(ShotStatus, on_delete=models.CASCADE, related_name='+')
    acceptCase = models.ForeignKey(ShotStatus, on_delete=models.CASCADE, blank=True, related_name='+', null=True)
    rejectCase = models.ForeignKey(ShotStatus, on_delete=models.CASCADE, blank=True, related_name='+', null=True)
    authorizedRoles = models.ManyToManyField(AssignmentsRoles, blank=True, related_name='+')
    allowedSteps = models.ManyToManyField(AssignmentsRoles, blank=True, related_name='+')
    statusIndex = models.PositiveSmallIntegerField(blank=True, null=True, default=0) #indexing based on status pipeline process
    isBeforeArtist = models.BooleanField(default=False)
    isSubShot = models.BooleanField(default=False)
    created_by = models.ForeignKey(Employee, on_delete=models.CASCADE, blank=True, related_name='+', null=True)
    updated_by = models.ForeignKey(Employee, on_delete=models.CASCADE, blank=True, related_name='+', null=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "ShotAssignmentsOrder"
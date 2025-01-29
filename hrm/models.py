#  Copyright (c) 2023.
#  Designed & Developed by Narendar Reddy G, OscarFX Private Limited
#  All rights reserved.

import os
import shutil
import random
import string
import uuid

from PIL import Image, ImageDraw, ImageFont
from colorfield.fields import ColorField
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.safestring import mark_safe
from imagekit.models import ProcessedImageField

from OFX_API import getRandomStrings


# Create your models here.
class EmployementStatus(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "EmployementStatus"

# Create your models here.
class Location(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __unicode__(self):
        return u'%s' % self.sigla
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Location"

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    color = ColorField(default='#FF0000')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Department"

class Permissions(models.Model):
    identifier = models.CharField(max_length=50, unique=True, default=getRandomStrings, primary_key=True)
    permission_key = models.CharField(max_length=50, unique=True, blank=False)
    name = models.CharField(max_length=50, null=True, blank=True)

    # add_client = models.BooleanField(default=False)
    # view_client= models.BooleanField(default=False)
    # add_project = models.BooleanField(default=False)
    # view_project = models.BooleanField(default=False)
    # add_sequence = models.BooleanField(default=False)
    # view_sequence = models.BooleanField(default=False)
    # add_shots = models.BooleanField(default=False)
    # can_view_all_shots = models.BooleanField(default=False)
    # can_view_team_shots = models.BooleanField(default=False)
    # can_view_my_task = models.BooleanField(default=False)
    # can_request_task_help = models.BooleanField(default=False)
    # can_view_task_help = models.BooleanField(default=False)
    # can_assign_shot = models.BooleanField(default=False)
    # can_assign_lead = models.BooleanField(default=False)
    # can_change_bid = models.BooleanField(default=False)
    # can_view_client_bid = models.BooleanField(default=False)
    # can_view_bid = models.BooleanField(default=False)
    # can_change_eta = models.BooleanField(default=False)
    # can_view_eta = models.BooleanField(default=False)
    # can_view_client_eta = models.BooleanField(default=False)
    # can_send_to_qc = models.BooleanField(default=False)
    # can_approve = models.BooleanField(default=False)
    # can_reject = models.BooleanField(default=False)
    # can_view_reports = models.BooleanField(default=False)
    # can_create_folder_permissions = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Role Permissions"

class Role(models.Model):
    name = models.CharField(max_length=100, unique=True)
    permissions = models.ManyToManyField(Permissions)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Role"

class Grade(models.Model):
    name = models.CharField(max_length=100, unique=True)
    a_man_day = models.FloatField(max_length=100, unique=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Grade"

class ProductionTeam(models.Model):
    lead = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='+', null=True)

    def __str__(self):
        return self.lead

    class Meta:
        verbose_name_plural = "Teams"

def getRandomStrings():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=32))

class EmployeeGroups(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    groupkey = models.CharField(max_length=32, default=getRandomStrings)
    department = models.ManyToManyField(Department)

    class Meta:
        verbose_name_plural = "EmployeeGroups"

    def __str__(self):
        return self.name



class Employee(models.Model):
    """
    Employee Data
    """

    profile = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    employee_id = models.CharField(max_length=100, null=True, unique=True, blank=True)
    first_name = models.CharField(max_length=200, null=True, blank=True)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    fullName = models.CharField(max_length=200, null=True, blank=True)
    def upload_photo_dir(self, filename):
        return ""
        # return create_random_img(self.profile, self.first_name, self.last_name)

    photo = ProcessedImageField(upload_to=upload_photo_dir,
                                format='PNG',
                                options={'quality': 100},
                                null=True, blank=True
                                )
    email = models.CharField(max_length=100, null=True, blank=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    contact = models.CharField(validators=[phone_regex], max_length=10, blank=True, null=True)  # Validators should be a list
    address = models.CharField(max_length=200, null=True, blank=True)
    employement_status = models.ForeignKey(EmployementStatus, on_delete=models.CASCADE, related_name='+', null=True,
                                           blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='+', null=True, blank=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='+', null=True, blank=True)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name='+', null=True, blank=True)
    permissions = models.ManyToManyField(Permissions, blank=True, null=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='+', null=True, blank=True)
    skills = models.TextField(null=True, blank=True)
    experience = models.CharField(max_length=200, null=True, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    team_lead = models.ForeignKey('self', on_delete=models.CASCADE, related_name='+', null=True, blank=True)
    supervisor = models.ForeignKey('self', on_delete=models.CASCADE, related_name='+', null=True, blank=True)
    force_password_change = models.BooleanField(default=True)
    apikey = models.CharField(max_length=32, default=getRandomStrings)
    pan_number = models.CharField(max_length=20, null=True, blank=True)
    doe = models.DateField(blank=True, null=True)  ##Date of Exit
    employee_groups = models.ManyToManyField(EmployeeGroups,blank=True)
    target_md = models.FloatField(default=0)
    # role_permissions = models.ForeignKey(Role_Permissions, on_delete=models.CASCADE, related_name='+', null=True,
    #                                      blank=True)

    def profile_photo(self):
        if self.photo:
            return mark_safe('<img src="%s" style="width: 45px; height:45px;" />' % self.photo.url)
        else:
            return 'No Image Found'

    profile_photo.short_description = 'Image'

    def __str__(self):
        if self.fullName:
            return self.fullName
        else:
            return ""

    class Meta:
        verbose_name_plural = "Employee"
        ordering = ('fullName',)

class WorkingDayTypes(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    sessionType = models.CharField(max_length=50, blank=True, null=True)
    sessionHours = models.FloatField(default=0)
    class Meta:
        verbose_name_plural = "Working Day Types"

class Leaves(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    kekaReferenceId = models.CharField(max_length=50, blank=True, null=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='+',null=True, blank=True)
    targetDate = models.DateTimeField(blank=True, null=True)
    dateFrom = models.DateTimeField(blank=True, null=True)
    dateTo = models.DateTimeField(blank=True, null=True)
    leaveType = models.CharField(max_length=50, blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    requestedOn = models.DateTimeField(blank=True, null=True)
    sessionFrom = models.ForeignKey(WorkingDayTypes, on_delete=models.CASCADE, related_name='+', null=True, blank=True)
    sessionTo = models.ForeignKey(WorkingDayTypes, on_delete=models.CASCADE, related_name='+', null=True, blank=True)
    status = models.CharField(max_length=20, blank=True, null=True)
    isWorking = models.BooleanField(default=False)
    creationDate = models.DateTimeField(auto_now_add=True)
    modifiedDate = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Leaves"

class Attendance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    attendanceDate = models.DateTimeField(blank=True, null=True)
    dayType = models.CharField(max_length=50, blank=True, null=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, blank=True, null=True)
    firstInOfTheDay = models.DateTimeField(blank=True, null=True)
    kekaReferenceId = models.CharField(max_length=50, blank=True, null=True)
    lastOutOfTheDay = models.DateTimeField(blank=True, null=True)
    leaveDayStatus = models.CharField(max_length=32, blank=True, null=True)
    shiftBreakDuration = models.FloatField(default=0)
    shiftDuration = models.FloatField(default=0)
    shiftEffectiveDuration = models.FloatField(default=0)
    shiftEndTime = models.DateTimeField(blank=True, null=True)
    shiftStartTime = models.DateTimeField(blank=True, null=True)
    totalBreakDuration = models.FloatField(default=0)
    totalEffectiveHours = models.FloatField(default=0)
    totalGrossHours = models.FloatField(default=0)
    creationDate = models.DateTimeField(auto_now_add=True)
    modifiedDate = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Attendance"

class OrganizationWorkingDays(models.Model):
    '''
    This working days will be the default week calendar for entire organization
    '''
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=20, null=True)
    code = models.CharField(max_length=20, null=True)
    isWorkingDay = models.BooleanField(default=True)
    workingHours =models.FloatField(default=8)
    updatedBy = models.ForeignKey(Employee, on_delete=models.CASCADE, blank=True, null=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='+', null=True, blank=True)
    creationDate = models.DateTimeField(auto_now_add=True)
    modifiedDate = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Organization Working Days"

class OrganizationHolidayTypes(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=20, null=True)


    class Meta:
        verbose_name_plural = "Organization Holiday Types"

class OrganizationHolidays(models.Model):
    '''
        This holidays days will be the default year calendar for entire organization
        '''
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100, null=True)
    targetDate = models.DateField(null=True, blank=True)
    type = models.ForeignKey(OrganizationHolidayTypes, on_delete=models.CASCADE, blank=True, null=True)
    sessionType = models.ForeignKey(WorkingDayTypes, on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField(max_length=1024, null=True, blank=True)
    createdBy = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='+', blank=True, null=True,)
    updatedBy = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='+',blank=True, null=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='+', null=True, blank=True)
    creationDate = models.DateTimeField(auto_now_add=True)
    modifiedDate = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Organization Holiday Days"

class DepartmentWorkingDays(models.Model):
    '''
    This will be forced working day by department wise
    '''
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100, null=True)
    description = models.TextField(max_length=1024, null=True, blank=True)
    department = models.ManyToManyField(Department)
    targetDate = models.DateField(blank=True, null=True)
    assignedBy = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='+', blank=True, null=True)
    updatedBy = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='+', blank=True, null=True)
    sessionType = models.ForeignKey(WorkingDayTypes, on_delete=models.CASCADE, null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='+', null=True, blank=True)
    creationDate = models.DateTimeField(auto_now_add=True)
    modifiedDate = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Department Working Days"

class EmployeeWorkingDays(models.Model):
    '''
    This will be forced working day by department wise
    '''
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100, null=True)
    description = models.TextField(max_length=1024, null=True, blank=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='+')
    assignedBy = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='+', null=True, blank=True)
    sessionType = models.ForeignKey(WorkingDayTypes, on_delete=models.CASCADE, null=True, blank=True)
    isSystem = models.BooleanField(default=False) # If the user not completed working hours from mon - fri, then sat might be considered as working day/n If the extra working generated by cron job will be added in calendar list and this value will be true
    targetDate = models.DateField(blank=True, null=True)
    updatedBy = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='+', blank=True, null=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='+', null=True, blank=True)
    creationDate = models.DateTimeField(auto_now_add=True)
    modifiedDate = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Employee Working Days"


class EmployeeRoleBinding(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, blank=True, related_name='+', null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='+', null=True, blank=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, blank=True, related_name='+', null=True)
    bindWith = models.ForeignKey(Employee, on_delete=models.CASCADE, blank=True, related_name='+', null=True)
    created_by = models.ForeignKey(Employee, on_delete=models.CASCADE, blank=True, related_name='+', null=True)
    updated_by = models.ForeignKey(Employee,on_delete=models.CASCADE, blank=True, related_name='+', null=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name_plural = "EmployeeRoleBinding"

class RoleRelationshipBinding(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, blank=True, related_name='+', null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='+', null=True, blank=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, blank=True, related_name='+', null=True)
    bindWithEmployee = models.ForeignKey(Employee, on_delete=models.CASCADE, blank=True, related_name='+', null=True)
    bindWithDepartment = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='+', null=True, blank=True)
    bindWithRole = models.ForeignKey(Role, on_delete=models.CASCADE, blank=True, related_name='+', null=True) 
    permissions = models.ManyToManyField(Permissions, blank=True)
    created_by = models.ForeignKey(Employee, on_delete=models.CASCADE, blank=True, related_name='+', null=True)
    updated_by = models.ForeignKey(Employee,on_delete=models.CASCADE, blank=True, related_name='+', null=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name_plural = "RoleRelationshipBinding"


# class Role_Permissions(models.Model):
#     role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='+', null=True)
#     add_client = models.BooleanField(default=False)
#     view_client = models.BooleanField(default=False)
#     add_project = models.BooleanField(default=False)
#     view_project = models.BooleanField(default=False)
#     add_sequence = models.BooleanField(default=False)
#     view_sequence = models.BooleanField(default=False)
#     add_shots = models.BooleanField(default=False)
#     can_view_all_shots = models.BooleanField(default=False)
#     can_view_team_shots = models.BooleanField(default=False)
#     can_view_my_task = models.BooleanField(default=False)
#     can_request_task_help = models.BooleanField(default=False)
#     can_view_task_help = models.BooleanField(default=False)
#     can_assign_shot = models.BooleanField(default=False)
#     can_assign_lead = models.BooleanField(default=False)
#     can_change_bid = models.BooleanField(default=False)
#     can_view_client_bid = models.BooleanField(default=False)
#     can_view_bid = models.BooleanField(default=False)
#     can_change_eta = models.BooleanField(default=False)
#     can_view_eta = models.BooleanField(default=False)
#     can_view_client_eta = models.BooleanField(default=False)
#     can_send_to_qc = models.BooleanField(default=False)
#     can_approve = models.BooleanField(default=False)
#     can_reject = models.BooleanField(default=False)
#     can_view_reports = models.BooleanField(default=False)
#     can_create_folder_permissions = models.BooleanField(default=False)
#
#     def __str__(self):
#         return self.role.name
#
#     class Meta:
#         verbose_name_plural = "Role Permissions"

def create_random_img(profile, first_name, last_name):
    def random_color():
        return (random.randrange(0, 180), random.randrange(0, 180), random.randrange(0, 100))

    W, H = (200, 200)
    first_l = ""
    last_l = ""
    if len(first_name) > 0:
        first_l = first_name[0]
    if len(last_name)>0:
        last_l = last_name[0]
    msg = first_l+last_l
    img = Image.new('RGB', (W, H), random_color())
    # font = ImageFont.truetype("/usr/share/fonts/truetype/DejaVuSans.ttf",25)
    draw = ImageDraw.Draw(img)
    myFont = ImageFont.truetype("./static/google-fonts/Inter-SemiBold.ttf", 100)
    w, h = draw.textsize(msg, font=myFont)
    h += int(h * 0.21)
    draw.text(((W - w) / 2, (H - h) / 2), msg, font=myFont, fill="white")
    # draw = ImageDraw.Draw(img)

    # Display edited image
    path = 'profiles/photo/{}.png'.format(profile)
    img.save('media/'+path)
    return path
@receiver(post_save, sender=Employee)
def create_user_profile(sender, instance, created, **kwargs):
    Employee.objects.filter(pk=instance.id).update(photo=create_random_img(instance.profile,instance.first_name, instance.last_name))

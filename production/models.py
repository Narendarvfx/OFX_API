#  Copyright (c) 2023.
#  Designed & Developed by Narendar Reddy G, OscarFX Private Limited
#  All rights reserved.

import datetime
import uuid

from colorfield.fields import ColorField
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from imagekit.models import ProcessedImageField
import logging

from OFX_API import getRandomStrings
from hrm.models import Employee, ProductionTeam, Department, Location, Role

logger = logging.getLogger('LoggerName')

class StatusSegregation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    code = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.code

    class Meta:
        verbose_name_plural = "StatusSegregation"

class ShotStatus(models.Model):
    code = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100, unique=True)
    color = ColorField(default='#e38330')
    isApproved = models.BooleanField(default=False)
    status_segregation = models.ForeignKey(StatusSegregation, on_delete=models.CASCADE, related_name='+', blank=True, null=True)


    def __str__(self):
        return self.code

    class Meta:
        verbose_name_plural = "ShotStatus"

class Complexity(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Complexity"

class Locality(models.Model):
    name = models.CharField(max_length=100, unique=True)
    color = ColorField(default='#e38330')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Locality"

class Clients(models.Model):
    Status = (
        ("IN PROGRESS", "IN PROGRESS"),
        ("ARCHIVED", "ARCHIVED")
    )
    Trigger = (
        ("DTC","DTC"),
        ("CAP","CAP")
    )
    name = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=70, null=True, blank=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    locality = models.ForeignKey(Locality, on_delete=models.CASCADE, blank=True, null=True)
    status = models.CharField(max_length=300, null=True, blank=True, choices=Status, default=Status[0][0])
    trigger = models.CharField(max_length=100,null=True, blank=True, choices=Trigger, default=Trigger[0][0])
    producer_email = models.CharField(max_length=300, blank=True, null=True)

    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Clients"

class Projects(models.Model):
    Status = (
        ("IN PROGRESS", "IN PROGRESS"),
        ("ARCHIVED", "ARCHIVED")
    )
    client = models.ForeignKey(Clients, on_delete=models.CASCADE, related_name='+')
    name = models.CharField(max_length=100, unique=False)
    org_status = models.ForeignKey(ShotStatus, on_delete=models.CASCADE, related_name='+',blank=True, null=True)
    start_date = models.DateTimeField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=300, null=True, blank=True, choices=Status, default=Status[0][1])

    def upload_photo_dir(self, filename):
        ext = filename.split('.')[-1]
        path = 'projects/photo/{}.{}'.format(self.name, ext)
        return path

    imageSrc = ProcessedImageField(upload_to=upload_photo_dir,
                                format='JPEG',
                                options={'quality': 80},
                                null=True,
                                blank=True
                                )

    creation_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    # def validate_unique(self, exclude=None):
    #     qs = Projects.objects.filter(name=self.name)
    #     if qs.filter(client=self.client).exists():
    #         logger.error('Project Name must be unique per Client')
    #         raise ValidationError('Project Name must be unique per Client')

    def save(self, *args, **kwargs):
        # self.validate_unique()

        super(Projects, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Projects"

class Episode(models.Model):
    name = models.CharField(max_length=100, unique=False)
    project = models.ForeignKey(Projects, on_delete=models.CASCADE, related_name='+')
    path = models.TextField(blank=True, null=True)
    type = models.CharField(default="Episode", max_length=50)
    creation_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

class Sequence(models.Model):
    name = models.CharField(max_length=100, unique=False)
    project = models.ForeignKey(Projects, on_delete=models.CASCADE, related_name='+')
    path = models.TextField(blank=True, null=True)
    type = models.CharField(default="Sequence", max_length=50)
    creation_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)


    def validate_unique(self, exclude=None):
        qs = Sequence.objects.filter(name=self.name)
        if qs.filter(project=self.project).exists():
            raise ValidationError('Sequence Name must be unique per Project')

    def save(self, *args, **kwargs):
        self.validate_unique()

        super(Sequence, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Sequence"

class Task_Type(models.Model):
    name = models.CharField(max_length=100, unique=True)
    color= ColorField(default='#e38330')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Task_Type"

class ShotVersion(models.Model):
    version = models.CharField(max_length=10)
    creation_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

class Shots(models.Model):
    Types = (
        ("NEW", "NEW"),
        ("RETAKE", "RETAKE"),
        ("ADDITIONAL", "ADDITIONAL")
    )
    name = models.CharField(max_length=100)
    sequence = models.ForeignKey(Sequence, on_delete=models.CASCADE, related_name='+', blank=True, null=True)
    episode = models.ForeignKey(Episode, on_delete=models.CASCADE, related_name='+', blank=True, null=True)
    status = models.ForeignKey(ShotStatus, on_delete=models.CASCADE, related_name='+')
    type = models.CharField(max_length=300, null=True, choices=Types, default=Types[0][0])
    task_type = models.ForeignKey(Task_Type, on_delete=models.CASCADE, related_name='+')
    actual_start_frame = models.IntegerField(default=0)
    actual_end_frame = models.IntegerField(default=0)
    work_start_frame = models.IntegerField(default=0)
    work_end_frame = models.IntegerField(default=0)
    eta = models.DateTimeField(null=True, blank=True)
    internal_eta = models.DateTimeField(null=True, blank=True)
    wip_eta = models.DateTimeField(null=True, blank=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    actual_bid_days = models.FloatField(default=0)
    bid_days = models.FloatField(default=0)
    internal_bid_days = models.FloatField(default=0)
    progress = models.FloatField(default=0)
    description = models.TextField(null=True, blank=True)
    complexity = models.ForeignKey(Complexity, on_delete=models.CASCADE, related_name='+', null=True, blank=True)
    duplicate = models.BooleanField(default=False)
    parentShot = models.ForeignKey('self', on_delete=models.CASCADE, related_name='+', null=True, blank=True)
    isSubShot = models.BooleanField(default=False)
    isSplitShot = models.BooleanField(default=False)
    supervisor = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='+', null=True, blank=True)
    team_lead = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='+', null=True, blank=True)
    hod = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='+', null=True, blank=True)
    artist = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='+', null=True, blank=True)
    artists = models.ManyToManyField(Employee, blank=True, related_name='+')
    scope_of_work = models.CharField(null=True, blank=True,max_length=1024)
    qc_name = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='+', null=True, blank=True)
    pending_mandays = models.FloatField(default=0)
    achieved_mandays = models.FloatField(default=0)
    package_id = models.CharField(max_length=30, blank=True, null=True)
    estimate_id = models.CharField(max_length=30, blank=True, null=True)
    estimate_date = models.DateTimeField(null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, default=1, related_name='+', null=True, blank=True)
    input_path = models.CharField(max_length=100, blank=True, null=True)
    retake_path = models.CharField(max_length=100, blank=True, null=True)
    output_path = models.TextField(blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    version = models.CharField(max_length=10, blank=True, null=True)
    submitted_date = models.DateTimeField(blank=True, null=True)
    naming_check = models.BooleanField(default=False)

    def upload_photo_dir(self, filename):
        ext = filename.split('.')[-1]
        path = 'shots/photo/{}.{}'.format(self.name, ext)
        return path

    imageSrc = ProcessedImageField(upload_to=upload_photo_dir,
                                format='JPEG',
                                options={'quality': 80},
                                null=True,blank=True
                                )

    creation_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_project(self, obj):
        return obj.sequence.project.name

    get_project.admin_order_field = 'project'
    get_project.short_description = 'Project'
    search_fields = ['name']

    class Meta:
        verbose_name_plural = "Shots"
        # get_project()

class ClientVersions(models.Model):
    version = models.CharField(max_length=30)
    shot = models.ForeignKey(Shots, on_delete=models.CASCADE, related_name='+')
    sent_date = models.DateTimeField(auto_now_add=True)
    sent_by = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='+')
    status = models.ForeignKey(ShotStatus, on_delete=models.CASCADE, related_name='+')
    output_path = models.TextField(blank=True, null=True)
    submission_notes = models.TextField(blank=True, null=True)
    verified_by =models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='+', blank=True, null=True)
    verified_date = models.DateTimeField(blank=True, null=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.version

    class Meta:
        verbose_name_plural = "ClientVersions"

class ShotVersions(models.Model):
    version = models.CharField(max_length=30)
    shot = models.ForeignKey(Shots, on_delete=models.CASCADE, related_name='+')
    sent_date = models.DateTimeField(auto_now_add=True)
    sent_by = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='+')
    status = models.ForeignKey(ShotStatus, on_delete=models.CASCADE, related_name='+')
    verified_by =models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='+', blank=True, null=True)
    verified_date = models.DateTimeField(blank=True, null=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.version

    class Meta:
        verbose_name_plural = "ShotVersions"

class AssignmentStepsOrder(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='+', null=True )
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='+', null=True)
    shotStatus = models.ForeignKey(ShotStatus, on_delete=models.CASCADE, related_name='+', null=True)
    authorised_roles = models.ManyToManyField(Role, blank=True, related_name='+')
    allowed_steps = models.ManyToManyField(Role, blank=True, related_name='+')
    acceptCase = models.ForeignKey(ShotStatus, on_delete=models.CASCADE, blank=True, related_name='+', null=True)
    rejectCase = models.ForeignKey(ShotStatus, on_delete=models.CASCADE, blank=True, related_name='+', null=True)
    onRejectSendTo = models.ForeignKey(Role, on_delete=models.CASCADE, blank=True, related_name='+', null=True)
    roleIndex = models.PositiveSmallIntegerField(blank=True, null=True, default=0)
    isBeforeArtist = models.BooleanField(default=False)
    # showInUI = models.BooleanField(default=True)
    created_by = models.ForeignKey(Employee, on_delete=models.CASCADE, blank=True, related_name='+', null=True)
    updated_by = models.ForeignKey(Employee,on_delete=models.CASCADE, blank=True, related_name='+', null=True)
    
    # status = models.ForeignKey(ShotStatus, on_delete=models.CASCADE, related_name='+', blank=True, null=True)
    # allowed_steps = models.ManyToManyField(ShotStatus, blank=True, related_name='+', null=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name_plural = "AssignmentStepsOrder"

class QCVersions(models.Model):
    version = models.CharField(max_length=30)
    shot = models.ForeignKey(Shots, on_delete=models.CASCADE, related_name='+')
    sent_date = models.DateTimeField(auto_now_add=True)
    sent_by = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='+')
    status = models.ForeignKey(ShotStatus, on_delete=models.CASCADE, related_name='+')
    verified_by =models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='+', blank=True, null=True)
    verified_date = models.DateTimeField(blank=True, null=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.version

    class Meta:
        verbose_name_plural = "QCVersions"

class MyTask(models.Model):
    Types = (
        ("NEW", "NEW"),
        ("RETAKE", "RETAKE"),
        ("ADDITIONAL", "ADDITIONAL")
    )
    artist = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='+')
    assigned_by = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='+', blank=True, null=True)
    shot = models.ForeignKey(Shots, on_delete=models.CASCADE, related_name='+')
    art_percentage = models.FloatField(default=0)
    assigned_bids = models.FloatField(default=0)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True , blank=True)
    eta = models.DateTimeField(null=True,blank=True)
    type = models.CharField(max_length=300, null=True, choices=Types, default=Types[0][0])
    task_status = models.ForeignKey(ShotStatus, on_delete=models.CASCADE, related_name='+')
    compiler = models.IntegerField(default=0)
    version = models.CharField(max_length=20, null=True, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.artist.fullName

    class Meta:
        verbose_name_plural = "MyTask"

class Elements(models.Model):
    identifier = models.CharField(unique=True, primary_key=True, max_length=50, default=getRandomStrings, editable=False)
    name = models.CharField(max_length=100, null=True, blank=True)
    project_id = models.ForeignKey(Projects, on_delete=models.CASCADE, blank=True, null=True)
    seq_id = models.ForeignKey(Sequence, on_delete=models.CASCADE, blank=True, null=True)
    shot_id = models.ForeignKey(Shots, on_delete=models.CASCADE, blank=True, null=True)
    # _tasks = models.ForeignKey(MyTask, on_delete=models.CASCADE, blank=True, null=True)
    status = models.ForeignKey(ShotStatus, on_delete=models.CASCADE, blank=True, null=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, blank=True, null=True)
    vendor = models.CharField(max_length=20, null=True, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    frame_range = models.IntegerField(default=0, null=True, blank=True)
    first_frame = models.IntegerField(default=0, null=True, blank=True)
    last_frame = models.IntegerField(default=0, null=True, blank=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    created_by = models.ForeignKey(Employee, on_delete=models.CASCADE, blank=True, null=True)
    layer = models.CharField(max_length=200, null=True, blank=True)
    type = models.CharField(max_length=20, null=True, blank=True)
    _pass = models.CharField(max_length=200, null=True, blank=True)
    version = models.IntegerField(default=0, null=True, blank=True)
    filepath = models.CharField(max_length=200, null=True, blank=True)
    src_path = models.CharField(max_length=200, null=True, blank=True)
    tag = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Elements"

class Assignments(models.Model):
    lead = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='+')
    shot = models.ForeignKey(Shots, on_delete=models.CASCADE, related_name='+')
    # status = models.ForeignKey(ShotStatus, on_delete=models.CASCADE, related_name='+')
    assigned_by = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='+')
    assigned_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.lead.fullName

    class Meta:
        verbose_name_plural = "Assignments"

class Qc_Assignment(models.Model):
    task = models.ForeignKey(MyTask, on_delete=models.CASCADE, related_name='+')
    team = models.ForeignKey(ProductionTeam, on_delete=models.CASCADE, related_name='+')
    qc_status = models.ForeignKey(ShotStatus, on_delete=models.CASCADE, related_name='+')

    def __str__(self):
        return self.team.lead.user.first_name

class Groups(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Groups"

class Channels(models.Model):
    sender = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='author_messages')
    shot = models.ForeignKey(Shots, on_delete=models.CASCADE, related_name='+')
    # group_name = models.ForeignKey(Groups, on_delete=models.CASCADE, related_name='+')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sender.fullName

    def last_10_messages(self):
        return Channels.objects.order_by('-timestamp').all()[:10]

    class Meta:
        verbose_name_plural = "Channels"

class Folder_Permissions(models.Model):
    permissions = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return self.permissions

    class Meta:
        verbose_name_plural = "Folder_Permissions"

class Permission_Groups(models.Model):
    permitted_users = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='+')
    permissions = models.ManyToManyField(Folder_Permissions, related_name='+')

    def __str__(self):
        return self.permitted_users.first_name

    class Meta:
        verbose_name_plural = "Permission_Groups"

class TaskHelp_Main(models.Model):
    shot = models.ForeignKey(Shots, on_delete=models.CASCADE, related_name='+')
    task_type = models.ForeignKey(Task_Type, on_delete=models.CASCADE, related_name='+')
    bid_days = models.FloatField(default=0)
    eta = models.DateTimeField(null=True,blank=True)
    status = models.ForeignKey(ShotStatus,on_delete=models.CASCADE, related_name='+')
    requested_by = models.ForeignKey(Employee, models.CASCADE, related_name='+')
    requested_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.shot.name

    class Meta:
        verbose_name_plural = "TaskHelp_Main"

class TaskHelp_Lead(models.Model):
    shot = models.ForeignKey(Shots, on_delete=models.CASCADE, related_name='+')
    task_type = models.ForeignKey(Task_Type, on_delete=models.CASCADE, related_name='+')
    assigned_to = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='+')
    assigned_by = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='+')
    assigned_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.shot.name

    class Meta:
        verbose_name_plural = "TaskHelp_Lead"

class TaskHelp_Artist(models.Model):
    shot = models.ForeignKey(Shots, on_delete=models.CASCADE, related_name='+')
    parent = models.ForeignKey(TaskHelp_Main, on_delete=models.CASCADE, related_name='+')
    bid_days = models.FloatField(default=0)
    eta = models.DateTimeField(null=True,blank=True)
    status = models.ForeignKey(ShotStatus, on_delete=models.CASCADE, related_name='+')
    assigned_to = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='+')
    assigned_by = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='+')
    assigned_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.shot.name

    class Meta:
        verbose_name_plural = "TaskHelp_Artist"

class ShotLogs(models.Model):
    shot = models.ForeignKey(Shots, on_delete=models.CASCADE, related_name='+')
    original_value = models.CharField(max_length=100, null=True, blank=True)
    updated_value = models.CharField(max_length=100, null=True, blank=True)
    message = models.CharField(max_length=500, null=True, blank=True)
    updated_by = models.ForeignKey(Employee,on_delete=models.CASCADE, null=True)
    update_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.shot.name

    class Meta:
        verbose_name_plural = "ShotLogs"

class DayLogs(models.Model):
    shot = models.ForeignKey(Shots, on_delete=models.CASCADE, related_name='+')
    shot_biddays = models.FloatField(blank=True, null=True)
    updated_shot_biddays = models.FloatField(blank=True, null=True)
    percentage = models.FloatField(default=0, blank=True, null=True)
    day_percentage = models.FloatField(default=0, blank=True, null=True)
    consumed_man_day = models.FloatField(default=0, blank=True, null=True)
    artist = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='+')
    updated_by = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True)
    updated_date = models.DateTimeField(auto_now_add=True) #Created Date
    last_updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.shot.name

    class Meta:
        verbose_name_plural = "DayLogs"

class TaskDayLogs(models.Model):
    task = models.ForeignKey(MyTask, on_delete=models.CASCADE, related_name='+')
    task_biddays = models.FloatField(blank=True, null=True)
    updated_task_biddays = models.FloatField(blank=True, null=True)
    percentage = models.FloatField(default=0, blank= True, null= True)
    day_percentage = models.FloatField(default=0, blank=True, null=True)
    consumed_man_day = models.FloatField(default=0, blank=True, null=True)
    artist = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='+')
    updated_by = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True)
    updated_date = models.DateTimeField(auto_now_add=True) #Created Date
    last_updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.task.shot.name

    class Meta:
        verbose_name_plural = "TaskDayLogs"

class TeamLead_Week_Reports(models.Model):
    team_lead = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='+')
    week = models.IntegerField(blank=True, null=True)
    from_date = models.DateField(null=True, blank=True)
    to_date = models.DateField(null=True, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    backlog_mandays = models.FloatField(null=True, blank=True)
    assigned_mandays = models.FloatField(null=True, blank=True)
    achieved_mandays = models.FloatField(null=True, blank=True)
    forwarded_mandays = models.FloatField(null=True, blank=True)
    percentage = models.FloatField(default=0)

    def __str__(self):
        return self.team_lead.fullName

    class Meta:
        verbose_name_plural = "TeamLead Week Reports"

class RolePipelineSteps(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='+', blank=True, null=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, blank=True, related_name='+', null=True)
    status = models.ForeignKey(ShotStatus, on_delete=models.CASCADE, related_name='+', blank=True, null=True)
    allowed_steps = models.ManyToManyField(ShotStatus, blank=True, related_name='+')
    creation_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Role Pipeline Steps"

class EstimationId(models.Model):
    Status = (
        ("SENT", "SENT"),
        ("NOT SENT", "NOT SENT")
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    client = models.ForeignKey(Clients, on_delete=models.CASCADE, related_name='+', null=True, blank=True)
    estimationId = models.CharField(max_length=100, unique=True)
    zohoId = models.CharField(max_length=100)
    status = models.CharField(max_length=300, null=True, blank=True, choices=Status, default=Status[1][0])

    def __str__(self):
        return self.estimationId

    class Meta:
        verbose_name_plural = "Estimation Id"


# @receiver(post_save, sender=Shots)
# def on_updating_progress(sender,instance,**kwargs):
#     print("Shots:",instance)
#     pm = instance.bid_days / 100 * instance.progress
#     pending_mandays = instance.bid_days - pm
#     instance.pending_mandays = pending_mandays
#     post_save.disconnect(on_updating_progress, sender=Shots)
#     instance.save()
#     post_save.connect(on_updating_progress, sender=Shots)

@receiver(post_save, sender=Shots)
def on_updating_internal_eta(sender,instance,**kwargs):
    MyTask.objects.filter(shot__id=instance.id,eta=None).update(eta=instance.internal_eta)

class TimeLogs(models.Model):
    shot = models.ForeignKey(Shots, on_delete=models.CASCADE, related_name='timelogs', blank=True, null=True)
    spent_hours = models.FloatField(default=0)
    others_hours = models.FloatField(default=0)
    total_hours = models.FloatField(default=0)
    comments = models.CharField(max_length=150, blank=True, null=True)
    approved = models.BooleanField(default=False)
    updated_by = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='+', blank=True, null=True)
    approved_by = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='+', blank=True, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.shot.name

    class Meta:
        verbose_name_plural = "Time Logs"

# @receiver(post_save, sender=Assignments)
# def on_assigning_to_tl(sender,instance,**kwargs):
#     if instance.shot.status.code == "YTA":
#         shot_instance = Shots.objects.select_related('sequence__project__client', 'sequence__project', 'sequence',
#                                                      'status', 'task_type', 'location', 'artist__department',
#                                                      'team_lead__department').get(pk=instance.shot.id)
#         shot_instance.team_lead = instance.lead
#         statusInstance = ShotStatus.objects.get(pk=3)
#         shot_instance.status = statusInstance
#         shot_instance.save()

# @receiver(post_save, sender=MyTask)
# def on_assigning_to_artist(sender,instance,**kwargs):
#     shot_instance = Shots.objects.get(pk=instance.shot.id)
#     if shot_instance.status.code != "DTC":
#         shot_instance.artist = instance.artist
#         shot_instance.save()

@receiver(post_save, sender=ClientVersions)
def on_internal_approve(sender,instance,**kwargs):
    shot_instance = Shots.objects.get(pk=instance.shot.id)
    shot_instance.version = instance.version
    shot_instance.submitted_date = instance.sent_date
    shot_instance.qc_name = instance.verified_by
    shot_instance.save()

# @receiver(post_save, sender=Assignments)
# def on_assignment(sender,instance,created,**kwargs):
#     shot_instance = Shots.objects.select_related('sequence__project__client','sequence__project','sequence','status','task_type','location','artist__department','team_lead__department').get(pk=instance.shot.id)
#
#
#     statusInstance = ShotStatus.objects.get(pk=3)
#     shot_instance.status = statusInstance
#     shot_instance.save()

# @receiver(post_save, sender=Shots)
# def on_dtc_change(sender,instance,created,**kwargs):
#     if instance.status.code == "DTC":
#         task_instance = MyTask.objects.select_related('shot','shot__sequence__project__client','shot__sequence__project','shot__sequence','shot__status','shot__task_type','shot__location','shot__artist__department','shot__team_lead__department').filter(shot=instance.id)
#         for ints in task_instance:
#             if ints.art_percentage < 100:
#                 day_per = 100 - ints.art_percentage
#                 cons_mandays = ints.assigned_bids / 100 * day_per
#                 _start_date = str(datetime.datetime.now().date())+'T00:00:00.000000'
#                 _end_date = str(datetime.datetime.now().date())+'T23:59:59.999999'
#                 daylog_inst = TaskDayLogs.objects.filter(updated_date__range=[_start_date,_end_date], task=ints.id)
#                 if len(daylog_inst)>0:
#                     daylog_inst[0].percentage = 100
#                     daylog_inst[0].day_percentage = day_per
#                     daylog_inst[0].consumed_man_day = cons_mandays
#                     daylog_inst[0].save()
#                 else:
#                     TaskDayLogs.objects.create(task=ints,percentage=100, day_percentage=day_per,consumed_man_day=round(cons_mandays, 2),artist=Employee.objects.get(pk=ints.artist.id),updated_by=Employee.objects.get(pk=ints.artist.id))
#                 ints.art_percentage = 100
#                 stat = ShotStatus.objects.get(code="DTC")
#                 ints.task_status = stat
#                 ints.save()

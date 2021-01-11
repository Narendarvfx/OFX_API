from colorfield.fields import ColorField
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from imagekit.models import ProcessedImageField
import logging
from hrm.models import Employee, ProductionTeam, Department

logger = logging.getLogger('LoggerName')

class ShotStatus(models.Model):
    code = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100, unique=True)
    color = ColorField(default='#e38330')

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

class Clients(models.Model):
    name = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=70, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    # status = models.ForeignKey(ShotStatus, default=1, on_delete=models.CASCADE,null=True,blank=True, related_name='+')

    def upload_photo_dir(self, filename):
        ext = filename.split('.')[-1]
        path = 'clients/photo/{}.{}'.format(self.name, ext)
        return path

    imageSrc = ProcessedImageField(upload_to=upload_photo_dir,
                                format='JPEG',
                                options={'quality': 80},
                                null=True,blank=True
                                )
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Clients"

class Projects(models.Model):
    client = models.ForeignKey(Clients, on_delete=models.CASCADE, related_name='+')
    name = models.CharField(max_length=100, unique=False)
    status = models.ForeignKey(ShotStatus, on_delete=models.CASCADE, related_name='+')
    start_date = models.DateTimeField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

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

    def validate_unique(self, exclude=None):
        qs = Projects.objects.filter(name=self.name)
        if qs.filter(client=self.client).exists():
            logger.error('Project Name must be unique per Client')
            raise ValidationError('Project Name must be unique per Client')

    def save(self, *args, **kwargs):
        self.validate_unique()

        super(Projects, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Projects"

class Sequence(models.Model):
    name = models.CharField(max_length=100, unique=False)
    project = models.ForeignKey(Projects, on_delete=models.CASCADE, related_name='+')
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

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Task_Type"

class ShotVersion(models.Model):
    version = models.CharField(max_length=10)
    creation_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    
class Shots(models.Model):
    name = models.CharField(max_length=100)
    sequence = models.ForeignKey(Sequence, on_delete=models.CASCADE, related_name='+')
    status = models.ForeignKey(ShotStatus, on_delete=models.CASCADE, related_name='+')
    task_type = models.ForeignKey(Task_Type, on_delete=models.CASCADE, related_name='+')
    actual_start_frame = models.IntegerField(default=0)
    actual_end_frame = models.IntegerField(default=0)
    work_start_frame = models.IntegerField(default=0)
    work_end_frame = models.IntegerField(default=0)
    eta = models.DateTimeField(null=True, blank=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    bid_days = models.FloatField(default=0)
    percentage = models.FloatField(default=0)
    description = models.TextField(null=True, blank=True)
    complexity = models.ForeignKey(Complexity, on_delete=models.CASCADE, related_name='+', null=True, blank=True)

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

    class Meta:
        verbose_name_plural = "Shots"

class HQCVersions(models.Model):
    version = models.CharField(max_length=30)
    shot = models.ForeignKey(Shots, on_delete=models.CASCADE, related_name='+')
    sent_date = models.DateTimeField(auto_now_add=True)
    sent_by = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='+')
    status = models.ForeignKey(ShotStatus, on_delete=models.CASCADE, related_name='+')
    verified_by = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='+', blank=True, null=True)
    verified_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.version

    class Meta:
        verbose_name_plural = "HQCVersions"

class ClientVersions(models.Model):
    version = models.CharField(max_length=30)
    shot = models.ForeignKey(Shots, on_delete=models.CASCADE, related_name='+')
    sent_date = models.DateTimeField(auto_now_add=True)
    sent_by = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='+')
    status = models.ForeignKey(ShotStatus, on_delete=models.CASCADE, related_name='+')
    verified_by =models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='+', blank=True, null=True)
    verified_date = models.DateTimeField(blank=True, null=True)

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

    def __str__(self):
        return self.version

    class Meta:
        verbose_name_plural = "ShotVersions"

class MyTask(models.Model):
    artist = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='+')
    assigned_by = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='+', blank=True, null=True)
    shot = models.ForeignKey(Shots, on_delete=models.CASCADE, related_name='+')
    art_percentage = models.FloatField(default=0)
    assigned_bids = models.FloatField(default=0)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True , blank=True)
    eta = models.DateTimeField(null=True,blank=True)
    task_status = models.ForeignKey(ShotStatus, on_delete=models.CASCADE, related_name='+')
    compiler = models.IntegerField(default=0)
    version = models.CharField(max_length=10, null=True, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.artist.fullName

    class Meta:
        verbose_name_plural = "MyTask"

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

class HeadQCTeam(models.Model):
    hqc = models.ForeignKey(Employee, on_delete=models.CASCADE,related_name='+', null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='+')

    def __str__(self):
        return self.hqc.fullName

    class Meta:
        verbose_name_plural = "HeadQCTeam"

class HeadQc_Assignment(models.Model):
    qc_task = models.ForeignKey(Qc_Assignment, on_delete=models.CASCADE, related_name='+')
    hqc = models.ForeignKey(HeadQCTeam, on_delete=models.CASCADE, related_name='+')
    hqc_status = models.ForeignKey(ShotStatus, on_delete=models.CASCADE, related_name='+')

    def __str__(self):
        return self.hqc.hqc.fullName

    class Meta:
        verbose_name_plural = "Head Qc Assignments"

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
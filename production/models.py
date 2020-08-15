from django.db import models
from imagekit.models import ProcessedImageField

from hrm.models import Employee


class Status(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Status"

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
    status = models.ForeignKey(Status, default=1, on_delete=models.CASCADE,null=True,blank=True, related_name='+')

    def upload_photo_dir(self, filename):
        ext = filename.split('.')[-1]
        path = 'clients/photo/{}.{}'.format(self.name, ext)
        return path

    imageSrc = ProcessedImageField(upload_to=upload_photo_dir,
                                format='JPEG',
                                options={'quality': 80},
                                null=True
                                )
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Clients"

class Projects(models.Model):
    name = models.CharField(max_length=100, unique=True)
    client = models.ForeignKey(Clients, on_delete=models.CASCADE, related_name='+')
    status = models.ForeignKey(Status, on_delete=models.CASCADE, related_name='+')
    start_date = models.DateTimeField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def upload_photo_dir(self, filename):
        ext = filename.split('.')[-1]
        path = 'projects/photo/{}.{}'.format(self.name, ext)
        return path

    imageSrc = ProcessedImageField(upload_to=upload_photo_dir,
                                format='JPEG',
                                options={'quality': 80},
                                null=True
                                )

    creation_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Projects"

class Sequence(models.Model):
    name = models.CharField(max_length=100, unique=False)
    project = models.ForeignKey(Projects, on_delete=models.CASCADE, related_name='+')
    status = models.ForeignKey(Status, on_delete=models.CASCADE, related_name='+')
    creation_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

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

class Shots(models.Model):
    name = models.CharField(max_length=100)
    sequence = models.ForeignKey(Sequence, on_delete=models.CASCADE, related_name='+')
    status = models.ForeignKey(Status, on_delete=models.CASCADE, related_name='+')
    task_type = models.ForeignKey(Task_Type, on_delete=models.CASCADE, related_name='+')
    actual_start_frame = models.IntegerField(null=True, blank=True)
    actual_end_frame = models.IntegerField(null=True, blank=True)
    work_start_frame = models.IntegerField(null=True, blank=True)
    work_end_frame = models.IntegerField(null=True, blank=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    bid_days = models.FloatField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    complexity = models.ForeignKey(Complexity, on_delete=models.CASCADE, related_name='+', null=True, blank=True)
    def upload_photo_dir(self, filename):
        ext = filename.split('.')[-1]
        path = 'shots/photo/{}.{}'.format(self.name, ext)
        return path

    imageSrc = ProcessedImageField(upload_to=upload_photo_dir,
                                format='JPEG',
                                options={'quality': 80},
                                null=True
                                )

    creation_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Shots"

class MyTask(models.Model):
    artist = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='+')
    assigned_by = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='+', blank=True, null=True)
    shot = models.ForeignKey(Shots, on_delete=models.CASCADE, related_name='+')
    assigned_bids = models.FloatField(null=True,blank=True)
    eta = models.DateTimeField(null=True,blank=True)
    status = models.ForeignKey(Status, on_delete=models.CASCADE, related_name='+')
    version = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return self.artist.fullName

    class Meta:
        verbose_name_plural = "MyTask"

class Assignments(models.Model):
    lead = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='+')
    shot = models.ForeignKey(Shots, on_delete=models.CASCADE, related_name='+')
    status = models.ForeignKey(Status, on_delete=models.CASCADE, related_name='+')
    assigned_by = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='+')
    assigned_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.lead.fullName

    class Meta:
        verbose_name_plural = "Assignments"
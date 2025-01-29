import uuid

from colorfield.fields import ColorField
from django.db import models

from production.models import Shots, Task_Type, Projects


# Create your models here.
class AssetTypes(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    color = ColorField(default='#e38330')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "AssetTypes"

class Dependencies(models.Model):
    Types = (
        ("References", "References"),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    shot = models.ForeignKey(Shots, on_delete=models.CASCADE, related_name='+', blank=True, null=True)
    department = models.ForeignKey(Task_Type, on_delete=models.CASCADE, related_name='+')
    depend_type = models.CharField(max_length=300, null=True, choices=Types, default=Types[0][0])
    asset_type = models.ForeignKey(AssetTypes, on_delete=models.CASCADE, related_name='+')
    asset_name = models.CharField(max_length=100, blank=True, null=True)
    asset_path = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.shot.name

    class Meta:
        verbose_name_plural = "Dependencies"

class ShotConfig(models.Model):
    Types = (
        ("SHOT", "SHOT"),
        ("ASSET", "ASSET")
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    shot = models.ForeignKey(Shots, on_delete=models.CASCADE, related_name='+')
    type = models.CharField(max_length=300, null=True, choices=Types, default=Types[0][0])
    render_width = models.IntegerField(default=0)  # render width specified by client.
    render_height = models.IntegerField(default=0) # render height specified by client.
    pb_width = models.IntegerField(default=0)   # playblast width specified by client
    pb_height = models.IntegerField(default=0)  # playblast height specified by client
    path = models.TextField(blank=True, null=True)
    dependencies = models.ForeignKey(Dependencies, on_delete=models.SET_NULL, related_name='+', blank=True, null=True)

    def __str__(self):
        return self.shot.name

    class Meta:
        verbose_name_plural = "ShotConfig"

class WinNukeVersions(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    path = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        verbose_name_plural = "WinNukeVersions"
class LinuxNukeVersions(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    path = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        verbose_name_plural = "LinuxNukeVersions"
class WinProjectConfig(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    nuke_config_path = models.TextField(blank=True, null=True)
    mnt_drive = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nuke_config_path
    class Meta:
        verbose_name_plural = "WinProjectConfig"
class LinuxProjectConfig(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    nuke_config_path = models.TextField(blank=True, null=True)
    mnt_drive = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nuke_config_path
    class Meta:
        verbose_name_plural = "LinuxProjectConfig"
class ProjectConfig(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    project = models.ForeignKey(Projects, on_delete=models.CASCADE, related_name='+')
    win_config = models.ForeignKey(WinProjectConfig, on_delete=models.CASCADE, related_name='+')
    linux_config = models.ForeignKey(LinuxProjectConfig, on_delete=models.CASCADE, related_name='+')

    def __str__(self):
        return self.project.name

    class Meta:
        verbose_name_plural = "ProjectConfig"

class PipelineConfig(models.Model):
    id= models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    project = models.ForeignKey(Projects, on_delete=models.CASCADE, related_name='+')
    drive = models.CharField(max_length=100, null=True, blank=True)
    nuke_path = models.CharField(max_length=100, null=True, blank=True)

class SBDesktopVersion(models.Model):
    id= models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    version = models.CharField(max_length=100, null=True, blank=True)
    download_path = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.version

    class Meta:
        verbose_name_plural = "SBDesktopVersion"


from colorfield.fields import ColorField
from django.contrib.auth.models import User
from django.db import models, transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.safestring import mark_safe
from imagekit.models import ProcessedImageField



from profiles.models import Profile

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


class Role(models.Model):
    name = models.CharField(max_length=100, unique=True)

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
    lead = models.ForeignKey(Profile, on_delete=models.SET_NULL,related_name='+', null=True)

    def __str__(self):
        return self.lead.user.username

    class Meta:
        verbose_name_plural = "Teams"

class Employee(models.Model):
    """
    Employee Data
    """
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, null=True)
    employee_id = models.CharField(max_length=100, null=True, unique=True, blank=True)
    fullName = models.CharField(max_length=200, null=True, blank=True)

    def upload_photo_dir(self, filename):
        ext = filename.split('.')[-1]
        path = 'profiles/photo/{}.{}'.format(self.profile.user.username, ext)
        return path

    photo = ProcessedImageField(upload_to=upload_photo_dir,
                                format='JPEG',
                                options={'quality': 80},
                                null=True
                                )
    email = models.CharField(max_length=100, null=True, blank=True)

    employement_status = models.ForeignKey(EmployementStatus, on_delete=models.CASCADE, related_name='+', null=True,
                                          blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='+', null=True, blank=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='+', null=True, blank=True)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name='+', null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='+', null=True, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    team_lead = models.ForeignKey('self', on_delete=models.CASCADE, related_name='+', null=True, blank=True)
    supervisor = models.ForeignKey('self', on_delete=models.CASCADE, related_name='+', null=True, blank=True)
    force_password_change= models.BooleanField(default=True)

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
            return self.profile.user.username

    class Meta:
        verbose_name_plural = "Employee"
        ordering = ('fullName',)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile = Profile.objects.create(user=instance)
        Employee.objects.create(profile=profile,
                                fullName=instance.first_name,
                                email=instance.email,
                                photo='profiles/photo/{}.jpg'.format(profile.user,firstName=instance.first_name))

class Role_Permissions(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE,related_name='+', null=True)
    add_client = models.BooleanField(default=False)
    view_client= models.BooleanField(default=False)
    add_project = models.BooleanField(default=False)
    view_project = models.BooleanField(default=False)
    add_sequence = models.BooleanField(default=False)
    view_sequence = models.BooleanField(default=False)
    add_shots = models.BooleanField(default=False)
    can_view_all_shots = models.BooleanField(default=False)
    can_view_team_shots = models.BooleanField(default=False)
    can_view_my_task = models.BooleanField(default=False)
    can_request_task_help = models.BooleanField(default=False)
    can_view_task_help = models.BooleanField(default=False)
    can_assign_shot = models.BooleanField(default=False)
    can_assign_lead = models.BooleanField(default=False)
    can_change_bid = models.BooleanField(default=False)
    can_view_client_bid = models.BooleanField(default=False)
    can_view_bid = models.BooleanField(default=False)
    can_change_eta = models.BooleanField(default=False)
    can_view_eta = models.BooleanField(default=False)
    can_view_client_eta = models.BooleanField(default=False)
    can_send_to_qc = models.BooleanField(default=False)
    can_approve = models.BooleanField(default=False)
    can_reject = models.BooleanField(default=False)
    can_view_reports = models.BooleanField(default=False)
    can_create_folder_permissions = models.BooleanField(default=False)

    def __str__(self):
        return self.role.name

    class Meta:
        verbose_name_plural = "Role Permissions"
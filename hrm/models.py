from colorfield.fields import ColorField
from django.contrib.auth.models import User
from django.db import models, transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.safestring import mark_safe
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

from profiles.models import Profile

# Create your models here.
class EmployementStatus(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Designation(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    color = ColorField(default='#FF0000')

    def __str__(self):
        return self.name

class Location(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Role(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Level(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Employee(models.Model):
    """
    User Profile
    """
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, null=True)
    employee_id = models.CharField(max_length=100, null=True, unique=True, blank=True)
    fullName = models.CharField(max_length=200, null=True, blank=True)
    firstName = models.CharField(max_length=100, null=True, blank=True)
    lastName = models.CharField(max_length=100, null=True, blank=True)

    def upload_photo_dir(self, filename):
        ext = filename.split('.')[-1]
        path = 'profiles/photo/{}.{}'.format(self.profile.user.username, ext)
        return path

    photo = ProcessedImageField(upload_to=upload_photo_dir,
                                processors=[ResizeToFill(800, 800)],
                                format='JPEG',
                                options={'quality': 80},
                                null=True
                                )

    date_of_birth = models.DateField(null=True, blank=True)
    gender_choice = (
        ('male', 'Male'),
        ('female', 'Female')
    )
    gender = models.CharField(max_length=10, choices=gender_choice, null=True, blank=True)
    marital_choice = (
        ('single', 'Single'),
        ('married', 'Married')
    )
    blood_group = models.CharField(max_length=200, null=True, blank=True)
    marital_status = models.CharField(max_length=10, choices=marital_choice, null=True, blank=True)
    # contact details
    address_1 = models.CharField(max_length=200, null=True, blank=True)
    address_2 = models.CharField(max_length=200, null=True, blank=True)
    address_city = models.CharField(max_length=100, null=True, blank=True)
    address_state = models.CharField(max_length=100, null=True, blank=True)
    address_zip = models.CharField(max_length=100, null=True, blank=True)
    address_country = models.CharField(max_length=100, null=True, blank=True)
    # correspondence details
    c_address_1 = models.CharField(max_length=200, null=True, blank=True)
    c_address_2 = models.CharField(max_length=200, null=True, blank=True)
    c_address_city = models.CharField(max_length=100, null=True, blank=True)
    c_address_state = models.CharField(max_length=100, null=True, blank=True)
    c_address_zip = models.CharField(max_length=100, null=True, blank=True)
    c_address_country = models.CharField(max_length=100, null=True, blank=True)

    work_email = models.CharField(max_length=100, null=True, blank=True)
    other_email = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    # Jobs Details
    joining_date = models.DateField(null=True, blank=True)
    resign_date = models.DateField(null=True, blank=True)
    employement_status = models.ForeignKey(EmployementStatus, on_delete=models.CASCADE, related_name='+', null=True,
                                          blank=True)
    designation = models.ForeignKey(Designation, on_delete=models.CASCADE, related_name='+', null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='+', null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='+', null=True, blank=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='+', null=True, blank=True)
    level = models.ForeignKey(Level, on_delete=models.CASCADE, related_name='+', null=True, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

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

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile = Profile.objects.create(user=instance)
        fullName = "{} {}".format(instance.first_name, instance.last_name)
        Employee.objects.create(profile=profile,
                                fullName=fullName,
                                firstName=instance.first_name,
                                lastName=instance.last_name,
                                work_email=instance.email,
                                photo='profiles/photo/{}.jpg'.format(profile.user,firstName=instance.first_name))
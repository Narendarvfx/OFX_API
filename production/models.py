from django.db import models
import pytz
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill


class Clients(models.Model):
    name = models.CharField(max_length=100, unique=True)
    email = models.EmailField(null=True, blank=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    TIMEZONES = tuple(zip(pytz.all_timezones, pytz.all_timezones))
    timezone = models.CharField(max_length=32, choices=TIMEZONES, default='Asia/Kolkata')
    status = models.CharField(max_length=40, default="Active", null=True, blank=True)

    def upload_photo_dir(self, filename):
        ext = filename.split('.')[-1]
        path = 'clients/photo/{}.{}'.format(self.name, ext)
        return path

    imageSrc = ProcessedImageField(upload_to=upload_photo_dir,
                                format='JPEG',
                                options={'quality': 80},
                                null=True
                                )

    def __str__(self):
        return self.name
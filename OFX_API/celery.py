from __future__ import absolute_import, unicode_literals
from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OFX_API.settings')

app = Celery('OFX_API')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.enable_utc = False

app.conf.update(
    task_acks_late=True,
    worker_prefetch_multiplier=1,
    task_track_started=True,  # Track task progress in Flower
    timezone = 'Asia/Calcutta'
)

app.autodiscover_tasks()
#  Copyright (c) 2023.
#  Designed & Developed by Narendar Reddy G, OscarFX Private Limited
#  All rights reserved.

from django.contrib import admin

from time_management.models import TimeManagement, TimeLogType

# Register your models here.

admin.site.register(TimeLogType)
admin.site.register(TimeManagement)

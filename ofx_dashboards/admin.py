#  Copyright (c) 2023.
#  Designed & Developed by Narendar Reddy G, OscarFX Private Limited
#  All rights reserved.

from django.contrib import admin

from ofx_dashboards.models import MandayAvailability, WaitingForBids

class MandayAvailabilityFields(admin.ModelAdmin):
    list_display = [f.name for f in MandayAvailability._meta.fields]

class WaitingForBidsFields(admin.ModelAdmin):
    list_display = [f.name for f in WaitingForBids._meta.fields]

# Register your models here.
admin.site.register(MandayAvailability, MandayAvailabilityFields)
admin.site.register(WaitingForBids, WaitingForBidsFields)
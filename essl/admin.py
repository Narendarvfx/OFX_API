from django.contrib import admin

# Register your models here.
from essl.models import Attendance

class AttendanceFields(admin.ModelAdmin):
    list_display = [f.name for f in Attendance._meta.fields]
    list_per_page = 15
    search_fields = ['employee_id']

admin.site.register(Attendance, AttendanceFields)
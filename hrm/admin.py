from django.contrib import admin
from .models import Employee, Department, Designation, Location, EmployementStatus, Role, Level


class EmployeeFields(admin.ModelAdmin):
    list_display = [f.name for f in Employee._meta.fields]
    list_display.insert(0, 'profile_photo')
    search_fields = ('employee_id', 'full_name')
    exclude = ("profile",)
    list_per_page = 10

admin.site.register(Employee, EmployeeFields)
admin.site.register(Department)
admin.site.register(Designation)
admin.site.register(Location)
admin.site.register(EmployementStatus)
admin.site.register(Role)
admin.site.register(Level)
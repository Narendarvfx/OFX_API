from django.contrib import admin
from .models import Employee, Department, EmployementStatus, Role, Grade, ProductionTeam, Permissions


class EmployeeFields(admin.ModelAdmin):
    list_display = [f.name for f in Employee._meta.fields]
    list_display.insert(0, 'profile_photo')
    search_fields = ('employee_id', 'fullName')
    exclude = ("profile",)
    list_per_page = 10

class PermissionFields(admin.ModelAdmin):
    list_display = [f.name for f in Permissions._meta.fields]

admin.site.register(Employee, EmployeeFields)
admin.site.register(ProductionTeam)
admin.site.register(Department)
admin.site.register(EmployementStatus)
admin.site.register(Role)
admin.site.register(Grade)
admin.site.register(Permissions, PermissionFields)
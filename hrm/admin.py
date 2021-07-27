from django.contrib import admin
from .models import Employee, Department, EmployementStatus, Role, Grade, ProductionTeam, Permissions


class EmployeeFields(admin.ModelAdmin):
    list_display = [f.name for f in Employee._meta.fields]
    list_display.insert(0, 'profile_photo')
    search_fields = ('employee_id', 'fullName')
    exclude = ("profile",)
    list_per_page = 15
    list_filter = ['department', 'role', 'employement_status', 'team']

    def get_dep(self, obj):
        return obj.department.name

    get_dep.admin_order_field = 'department'
    get_dep.short_description = 'Department'

    def get_role(self, obj):
        return obj.role.name

    get_role.admin_order_field = 'role'
    get_role.short_description = 'Role'

class PermissionFields(admin.ModelAdmin):
    list_display = [f.name for f in Permissions._meta.fields]

admin.site.register(Employee, EmployeeFields)
admin.site.register(ProductionTeam)
admin.site.register(Department)
admin.site.register(EmployementStatus)
admin.site.register(Role)
admin.site.register(Grade)
admin.site.register(Permissions, PermissionFields)
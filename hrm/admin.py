#  Copyright (c) 2023.
#  Designed & Developed by Narendar Reddy G, OscarFX Private Limited
#  All rights reserved.
import csv

from django.contrib import admin
from django.db.models.fields.files import FieldFile
from django.http import HttpResponse
from django.urls import resolve
from rest_framework.authtoken.admin import TokenAdmin

from .models import Employee, Department, EmployementStatus, Role, Grade, ProductionTeam, Permissions, Location, \
    EmployeeGroups, Leaves, Attendance, OrganizationHolidayTypes, OrganizationHolidays, DepartmentWorkingDays, \
    EmployeeWorkingDays, OrganizationWorkingDays, WorkingDayTypes, EmployeeRoleBinding, RoleRelationshipBinding

from rest_framework.authtoken.models import Token


class ExportCsvMixin:
    def export_as_csv(self, request, queryset):

        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

    #     response = HttpResponse(content_type='text/csv')
    #     response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
    #     writer = csv.writer(response)
    #
    #     writer.writerow(field_names)
    #     for obj in queryset:
    #         row = writer.writerow([getattr(obj, field) for field in field_names])
    #
    #     return response
    #
    # export_as_csv.short_description = "Export Selected"

        field_names = list(self.list_display)

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename={}.csv".format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            result = []
            for field in field_names:
                attr = getattr(obj, field, None)
                if attr and callable(attr):
                    result.append(attr())
                elif attr:
                    result.append(attr)
                else:
                    attr = getattr(self, field, None)
                    if attr:
                        result.append(attr(obj))
                    else:
                        result.append(attr)
            row = writer.writerow(result)

        return response


    export_as_csv.short_description = "Export Selected"

class EmployeeFields(admin.ModelAdmin, ExportCsvMixin):
    list_display = ('id', 'fullName', 'employee_id', 'get_dep', 'get_role', 'employement_status')

    search_fields = ('employee_id', 'fullName', 'contact', 'address')

    list_per_page = 15
    list_filter = ['department', 'role', 'employement_status','location']
    filter_horizontal = ('permissions',)
    list_display.append('manday')
    actions = ["export_as_csv"]
    autocomplete_fields = ['grade', ]

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            "profile", "employement_status", "department", "role", "grade", "location", 'team_lead', 'supervisor'
        ).prefetch_related("permissions", "employee_groups").defer("skills", "address")

    def manday(self, obj):
        if obj.grade:
            return obj.grade.a_man_day

    @admin.display(ordering="department__name")
    def get_dep(self, obj):
        return obj.department.name

    get_dep.admin_order_field = 'department'
    get_dep.short_description = 'Department'

    @admin.display(ordering="role__name")
    def get_role(self, obj):
        return obj.role.name

    get_role.admin_order_field = 'role'
    get_role.short_description = 'Role'

    @admin.display(ordering="employement_status__name")
    def get_employment_status(self, obj):
        return obj.employement_status.name if obj.employement_status else "-"

    @admin.display(ordering="location__name")
    def get_location(self, obj):
        return obj.location.name if obj.location else "-"


# admin.site.unregister(Site)
# class SiteAdmin(admin.ModelAdmin):
#     fields = ('id', 'name', 'domain')
#     readonly_fields = ('id',)
#     list_display = ('id', 'name', 'domain')
#     list_display_links = ('name',)
#     search_fields = ('name', 'domain')
# admin.site.unregister(Site)

class EmployeeGroupsFields(admin.ModelAdmin):
    list_display = [f.name for f in EmployeeGroups._meta.fields]

class PermissionFields(admin.ModelAdmin):
    list_display = [f.name for f in Permissions._meta.fields]

class TokenFields(TokenAdmin, admin.ModelAdmin):
    search_fields = ('user__username',)

class LeavesFields(admin.ModelAdmin):
    list_display = ['id','employee','targetDate','dateFrom','dateTo','leaveType','requestedOn','fromsession','tosession','status','isWorking','creationDate','modifiedDate' ]
    search_fields = ('employee__employee_id', 'employee__fullName', 'leaveType', 'status')
    date_hierarchy = 'creationDate'

    def fromsession(self, obj):
        if obj:
            return obj.sessionFrom.sessionType
    def tosession(self, obj):
        if obj:
            return obj.sessionTo.sessionType

class AttendanceFields(admin.ModelAdmin):
    list_display = ['id','employee','attendanceDate','firstInOfTheDay','lastOutOfTheDay','totalGrossHours','totalBreakDuration','totalEffectiveHours','dayType','creationDate','modifiedDate']
    search_fields = ('employee__employee_id', 'employee__fullName')

class GradeFields(admin.ModelAdmin):
    list_display = ['id','name','a_man_day']
    search_fields = ('name',)

class RoleFields(admin.ModelAdmin):
    list_display = ['id','name','get_permissions']
    filter_horizontal = ('permissions',)
    save_as = True

    def get_permissions(self, obj):
        return [permissions.name for permissions in obj.permissions.all()]

class DepartmentWorkingDaysFields(admin.ModelAdmin):
    list_display = ['id','name','targetDate', 'dept','sessionType_name','location']
    list_filter = ['location__name']
    def dept(self, obj):
        return [depart.name for depart in obj.department.all()]
    def sessionType_name(self, obj):
        if obj.sessionType:
            return obj.sessionType.sessionType
        else:
            return None

class EmployeeWorkingDaysFields(admin.ModelAdmin):
    list_display = ['id','name','targetDate', 'employee_name','assignedBy_name','sessionType_name','isSystem','location']
    list_filter = ['location__name']
    def employee_name(self, obj):
        return obj.employee.fullName
    def assignedBy_name(self, obj):
        return obj.assignedBy.fullName
    def sessionType_name(self, obj):
        if obj.type:
            return obj.sessionType.sessionType
        else:
            return None

class OrganizationWorkingDaysFields(admin.ModelAdmin):
    list_display = ['id','name','code','isWorkingDay','workingHours','location']
    list_filter = ['location__name']

class WorkingDayTypeFields(admin.ModelAdmin):
    list_display = ['id','sessionType']

class OrganizationHolidayTypesFields(admin.ModelAdmin):
    list_display = ['id','name']

class OrganizationHolidaysFields(admin.ModelAdmin):
    list_display = ['id','name','targetDate', 'holiday_type','sessionType_name','location']
    list_filter = ['location__name']
    def holiday_type(self, obj):
        if obj.type:
            return obj.type.name
        else:
            return None
    def sessionType_name(self, obj):
        if obj.type:
            return obj.sessionType.sessionType
        else:
            return None

class EmployeeRoleBindingFields(admin.ModelAdmin, ExportCsvMixin):
    list_display = ['id','emp_code','employee','act_status', 'department', 'role', 'bindWith', 'created_by', 'updated_by', 'creation_date', 'modified_date']
    list_filter = ['department__name', 'role__name']
    search_fields = ('employee__employee_id', 'employee__fullName', 'bindWith__fullName')
    actions = ["export_as_csv"]
    autocomplete_fields = ['employee', 'bindWith', 'created_by', 'updated_by']

    def emp_code(self, obj):
        return obj.employee.employee_id

    def act_status(self, obj):
        return obj.employee.employement_status

class RoleRelationshipBindingFields(admin.ModelAdmin):
    list_display = ['id', 'employee', 'department', 'role', 'bindWithEmployee', 'bindWithDepartment', 'bindWithRole', 'get_permissions', 'created_by', 'updated_by', 'creation_date', 'modified_date']
    filter_horizontal = ('permissions',)
    def get_permissions(self, obj):
        return obj.permissions.name

admin.site.register(Employee, EmployeeFields)
admin.site.register(EmployeeGroups, EmployeeGroupsFields)
admin.site.register(ProductionTeam)
admin.site.register(Department)
admin.site.register(EmployementStatus)
admin.site.register(Role, RoleFields)
admin.site.register(Grade, GradeFields)
admin.site.register(Location)
admin.site.register(Leaves, LeavesFields)
admin.site.register(Attendance, AttendanceFields)
admin.site.register(Permissions, PermissionFields)
admin.site.register(OrganizationHolidayTypes, OrganizationHolidayTypesFields)
admin.site.register(OrganizationHolidays, OrganizationHolidaysFields)
admin.site.register(DepartmentWorkingDays, DepartmentWorkingDaysFields)
admin.site.register(EmployeeWorkingDays, EmployeeWorkingDaysFields)
admin.site.register(OrganizationWorkingDays, OrganizationWorkingDaysFields)
admin.site.register(WorkingDayTypes, WorkingDayTypeFields)
admin.site.register(EmployeeRoleBinding, EmployeeRoleBindingFields)
admin.site.register(RoleRelationshipBinding, RoleRelationshipBindingFields)
admin.site.unregister(Token)
admin.site.register(Token, TokenFields)

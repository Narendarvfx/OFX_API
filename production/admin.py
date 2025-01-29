#  Copyright (c) 2023.
#  Designed & Developed by Narendar Reddy G, OscarFX Private Limited
#  All rights reserved.
import csv

from django.contrib import admin
from django.http import HttpResponse

from production.models import Clients, Projects,  ShotStatus, Complexity, Shots, Sequence, Task_Type, MyTask, \
    Assignments, Channels, Qc_Assignment, Groups, Permission_Groups, Folder_Permissions, \
    ShotVersions, ClientVersions, TaskHelp_Main, TaskHelp_Lead, TaskHelp_Artist, ShotLogs, TeamLead_Week_Reports, \
    Locality, DayLogs, QCVersions, TimeLogs, TaskDayLogs, Elements, RolePipelineSteps, AssignmentStepsOrder , StatusSegregation ,EstimationId

# Register your models here.
# class ShotStatusSegregationFields(admin.ModelAdmin):
#     list_display = [f.name for f in ShotStatusSegregation._meta.fields]
#     list_per_page = 15

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

class ClientFields(admin.ModelAdmin):
    list_display = [f.name for f in Clients._meta.fields]
    list_per_page = 15
    search_fields = ['name',]

class EstimationIdFields(admin.ModelAdmin):
    list_display = [f.name for f in EstimationId._meta.fields]
    list_per_page = 15
    search_fields = ['estimationId', 'zohoId','client__name']
    list_filter = ['status']

class ShotStatusFields(admin.ModelAdmin):
    list_display = [f.name for f in ShotStatus._meta.fields]
    list_per_page = 15

class StatusSegregationFields(admin.ModelAdmin):
    list_display = [f.name for f in StatusSegregation._meta.fields]
    list_per_page = 15

# Register your models here.
class ShotsFields(admin.ModelAdmin):
    list_display=[f.name for f in Shots._meta.fields]
    list_display.insert(1, 'get_client')
    list_display.insert(2, 'get_project')
    list_per_page = 15
    list_filter = ['task_type', 'sequence__project__client','sequence__project', 'status']
    date_hierarchy = 'eta'
    readonly_fields = ('status',)
    filter_horizontal = ('artists',)

    def get_readonly_fields(self, request, obj=None):
        if request.user.groups.filter(name='StatusUpdateGroup').exists():
            return []
        return self.readonly_fields

    def get_seq(self, obj):
        return obj.sequence.name

    get_seq.admin_order_field = 'sequence'
    get_seq.short_description = 'Sequence'

    def get_project(self, obj):
        return obj.sequence.project.name

    get_project.admin_order_field = 'project'
    get_project.short_description = 'Project'

    def get_client(self, obj):
        return obj.sequence.project.client.name

    get_client.admin_order_field = 'client'
    get_client.short_description = 'Client'
    search_fields = ['name','estimate_id']

class MyTaskFields(admin.ModelAdmin):
    list_display = [f.name for f in MyTask._meta.fields]
    list_per_page = 15
    list_filter = ['task_status']
    search_fields = ['artist__fullName']
    autocomplete_fields = ['artist','shot',]

class AssignmentFields(admin.ModelAdmin):
    list_display = [f.name for f in Assignments._meta.fields]
    list_per_page = 15
    search_fields = ['lead__fullName', 'shot__name']
    autocomplete_fields = ['lead', 'shot', ]

class SequenceFields(admin.ModelAdmin):
    list_display = [f.name for f in Sequence._meta.fields]
    list_per_page = 15
    search_fields = ['name']

class ProjectFields(admin.ModelAdmin):
    list_display = [f.name for f in Projects._meta.fields]
    list_per_page = 15
    search_fields = ['name']

class ShotLogsFields(admin.ModelAdmin):
    list_display = [f.name for f in ShotLogs._meta.fields]
    list_per_page = 15
    search_fields = ['name']

class DayLogsFields(admin.ModelAdmin):
    list_display = [f.name for f in DayLogs._meta.fields]
    list_per_page = 15
    list_filter = ['updated_date','artist__department__name']
    search_fields = ['shot__name', 'updated_by__fullName', 'artist__fullName', 'artist__employee_id']
    date_hierarchy = 'updated_date'

class TaskDayLogsFields(admin.ModelAdmin, ExportCsvMixin):
    #list_display = [f.name for f in TaskDayLogs._meta.fields]
    list_display = ('id','get_shot','percentage','day_percentage','task','artist','task_biddays','updated_task_biddays','consumed_man_day','updated_by','updated_date')
    list_per_page = 15
    list_select_related = ['task__shot','updated_by', 'task','task__artist','artist']
    list_filter = ['updated_date','artist__department__name']
    search_fields = ['task__shot__name', 'updated_by__fullName', 'artist__fullName', 'artist__employee_id']
    date_hierarchy = 'updated_date'
    actions = ["export_as_csv"]

    def get_shot(self, obj):
        return obj.task.shot.name

class ElementsFields(admin.ModelAdmin):
    list_display = [f.name for f in Elements._meta.fields]
    list_per_page = 15

    def get_pro(self, obj):
        return obj.project_id.name

    get_pro.admin_order_field = 'project'
    get_pro.short_description = 'Project'
    def get_seq(self, obj):
        return obj.seq_id.name

    get_seq.admin_order_field = 'sequence'
    get_seq.short_description = 'Sequence'

    def get_shot(self, obj):
        return obj.shot_id.name

    get_shot.admin_order_field = 'shot'
    get_shot.short_description = 'Shot'
    # def get_task(self, obj):
    #     return obj.task.artist.fullName
    #
    # get_task.admin_order_field = 'mytask'
    # get_task.short_description = 'MyTask'

    def get_emp(selfself, obj):
        return obj.created_by.fullName

    get_emp.admin_order_field = 'Employee'
    get_emp.short_description = 'Employee'

    search_fields = ['name']

class TimeLogsFields(admin.ModelAdmin):
    list_display = [f.name for f in TimeLogs._meta.fields]
    list_per_page = 15
    list_filter = ['creation_date','updated_by__department__name']
    search_fields = ['shot__name', 'updated_by__fullName', 'approved_by__fullName']

class ClientVersionsFields(admin.ModelAdmin):
    list_display = [f.name for f in ClientVersions._meta.fields]
    list_per_page = 15
    list_filter = ['sent_date','verified_date', 'sent_by__department__name']
    search_fields = ['shot__name', 'verified_by__fullName', 'sent_by__fullName']

class QcVersionsFields(admin.ModelAdmin):
    list_display = [f.name for f in QCVersions._meta.fields]
    list_per_page = 15
    list_filter = ['sent_date','verified_date', 'sent_by__department__name']
    search_fields = ['shot__name', 'verified_by__fullName', 'sent_by__fullName']

class ShotVersionsFields(admin.ModelAdmin):
    list_display = [f.name for f in ShotVersions._meta.fields]
    list_per_page = 15
    list_filter = ['sent_date','verified_date', 'sent_by__department__name']
    search_fields = ['shot__name', 'verified_by__fullName', 'sent_by__fullName']

class AssignmentStepsOrderFields(admin.ModelAdmin):
    list_display = ['id','department','role','shotStatus','get_authorised_roles','get_allowed_steps','acceptCase', 'rejectCase', 'onRejectSendTo', 'roleIndex', 'isBeforeArtist', 'created_by', 'updated_by','creation_date','modified_date']
    list_filter = ['department', 'role', 'isBeforeArtist','authorised_roles']
    filter_horizontal = ('authorised_roles','allowed_steps',)

    def get_authorised_roles(self, obj):
        return [allowed_role.name for allowed_role in obj.authorised_roles.all()]
    def get_allowed_steps(self, obj):
        return [acceptCase.name for acceptCase in obj.allowed_steps.all()]

class RolePipelineStepsFields(admin.ModelAdmin):
    list_display = ['id', 'department', 'role', 'status', 'get_allowed_steps', 'creation_date', 'modified_date']
    list_filter = ['department', 'role', 'status']
    filter_horizontal = ('allowed_steps',)
    def get_allowed_steps(self, obj):
        return [allowed_steps.code for allowed_steps in obj.allowed_steps.all()]

# admin.site.register(ShotStatusSegregation, ShotStatusSegregationFields)
admin.site.register(ShotStatus, ShotStatusFields)
admin.site.register(StatusSegregation, StatusSegregationFields)
admin.site.register(Complexity)
admin.site.register(Clients, ClientFields)
admin.site.register(Projects, ProjectFields)
admin.site.register(Sequence, SequenceFields)
admin.site.register(Task_Type)
admin.site.register(Shots, ShotsFields)
admin.site.register(AssignmentStepsOrder, AssignmentStepsOrderFields)
admin.site.register(MyTask, MyTaskFields)
admin.site.register(Assignments, AssignmentFields)
admin.site.register(Qc_Assignment)
admin.site.register(Groups)
admin.site.register(Channels)
admin.site.register(Permission_Groups)
admin.site.register(Folder_Permissions)
admin.site.register(ShotVersions, ShotVersionsFields)
admin.site.register(QCVersions, QcVersionsFields)
admin.site.register(ClientVersions, ClientVersionsFields)
admin.site.register(TaskHelp_Main)
admin.site.register(TaskHelp_Lead)
admin.site.register(TaskHelp_Artist)
admin.site.register(ShotLogs, ShotLogsFields)
admin.site.register(TeamLead_Week_Reports)
admin.site.register(Locality)
admin.site.register(DayLogs, DayLogsFields)
admin.site.register(TimeLogs, TimeLogsFields)
admin.site.register(TaskDayLogs, TaskDayLogsFields)


admin.site.register(Elements, ElementsFields)

class RolePipelineStepFields(admin.ModelAdmin):
    list_display = ['department__name','role__name','status__code','allowed__steps']

admin.site.register(RolePipelineSteps, RolePipelineStepsFields)
admin.site.register(EstimationId, EstimationIdFields)
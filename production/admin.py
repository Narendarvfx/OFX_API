from django.contrib import admin
from production.models import Clients, Projects, ShotStatus, Complexity, Shots, Sequence, Task_Type, MyTask, \
    Assignments, Channels, Qc_Assignment, Groups, Permission_Groups, Folder_Permissions, \
    ShotVersions, ClientVersions, TaskHelp_Main, TaskHelp_Lead, TaskHelp_Artist, ShotLogs, TeamLead_Week_Reports, \
    Locality, DayLogs, QCVersions, TimeLogs, TaskDayLogs


# Register your models here.
class ShotStatusFields(admin.ModelAdmin):
    list_display = [f.name for f in ShotStatus._meta.fields]
    list_per_page = 15

# Register your models here.
class ShotsFields(admin.ModelAdmin):
    list_display = [f.name for f in Shots._meta.fields]
    list_per_page = 15
    list_filter = ['task_type', 'sequence__project', 'status']

    def get_seq(self, obj):
        return obj.sequence.name

    get_seq.admin_order_field = 'sequence'
    get_seq.short_description = 'Sequence'

    def get_project(self, obj):
        return obj.sequence.project

    get_project.admin_order_field = 'project'
    get_project.short_description = 'Project'
    search_fields = ['name']

class MyTaskFields(admin.ModelAdmin):
    list_display = [f.name for f in MyTask._meta.fields]
    list_per_page = 15
    list_filter = ['task_status']
    search_fields = ['artist__fullName']

class AssignmentFields(admin.ModelAdmin):
    list_display = [f.name for f in Assignments._meta.fields]
    list_per_page = 15
    search_fields = ['lead__fullName', 'shot__name']

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
    search_fields = ['shot__name', 'updated_by__fullName', 'artist__fullName']

class TaskDayLogsFields(admin.ModelAdmin):
    list_display = [f.name for f in TaskDayLogs._meta.fields]
    list_per_page = 15
    list_filter = ['updated_date','artist__department__name']
    search_fields = ['task__shot__name', 'updated_by__fullName', 'artist__fullName']

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

admin.site.register(ShotStatus, ShotStatusFields)
admin.site.register(Complexity)
admin.site.register(Clients)
admin.site.register(Projects, ProjectFields)
admin.site.register(Sequence, SequenceFields)
admin.site.register(Task_Type)
admin.site.register(Shots, ShotsFields)
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

from django.contrib import admin
from django.contrib.admin import DateFieldListFilter

from history.models import ClientsHistory, ProjectsHistory, ShotsHistory, AssignmentsHistory, MyTaskHistory, \
    DayLogsHistory, TaskDayLogsHistory


@admin.register(ClientsHistory)
class ClientsHistoryAdmin(admin.ModelAdmin):
    list_display = [f.name for f in ClientsHistory._meta.fields]
    list_per_page = 15
    list_filter = (('created_at', DateFieldListFilter),)
    date_hierarchy = 'created_at'
    search_fields = ['who__fullName', 'who__employee_id', 'target__name']

@admin.register(ProjectsHistory)
class ProjectsHistoryAdmin(admin.ModelAdmin):
    list_display = [f.name for f in ProjectsHistory._meta.fields]
    list_per_page = 15
    list_filter = (('created_at', DateFieldListFilter),)
    date_hierarchy = 'created_at'
    search_fields = ['who__fullName', 'who__employee_id', 'target__name']

@admin.register(ShotsHistory)
class ShotsHistoryAdmin(admin.ModelAdmin):
    list_display = [f.name for f in ShotsHistory._meta.fields]
    list_per_page = 15
    list_filter = (('created_at', DateFieldListFilter),)
    date_hierarchy = 'created_at'
    search_fields = ['who__fullName', 'who__employee_id', 'target__name']

@admin.register(AssignmentsHistory)
class AssignmentsHistoryAdmin(admin.ModelAdmin):
    list_display = [f.name for f in AssignmentsHistory._meta.fields]
    list_per_page = 15
    list_filter = (('created_at', DateFieldListFilter),)
    date_hierarchy = 'created_at'
    search_fields = ['who__fullName', 'who__employee_id', 'target__shot__name']

@admin.register(MyTaskHistory)
class MyTaskHistoryAdmin(admin.ModelAdmin):
    list_display = [f.name for f in MyTaskHistory._meta.fields]
    list_per_page = 15
    list_filter = (('created_at', DateFieldListFilter),)
    date_hierarchy = 'created_at'
    search_fields = ['who__fullName', 'who__employee_id', 'target__shot__name']

@admin.register(DayLogsHistory)
class DayLogsHistoryAdmin(admin.ModelAdmin):
    list_display = [f.name for f in DayLogsHistory._meta.fields]
    list_per_page = 15
    list_filter = (('created_at', DateFieldListFilter),)
    date_hierarchy = 'created_at'
    search_fields = ['who__fullName', 'who__employee_id', 'target__name']

@admin.register(TaskDayLogsHistory)
class TaskDayLogsHistoryAdmin(admin.ModelAdmin):
    list_display = [f.name for f in TaskDayLogsHistory._meta.fields]
    list_per_page = 15
    list_filter = (('created_at', DateFieldListFilter),)
    date_hierarchy = 'created_at'
    search_fields = ['who__fullName', 'who__employee_id', 'target__shot__name']

from django.contrib import admin
from production.models import Clients, Projects, ShotStatus, Complexity, Shots, Sequence, Task_Type, MyTask, \
    Assignments, Channels, Qc_Assignment, Groups, HeadQc_Assignment, HeadQCTeam, Permission_Groups, Folder_Permissions, \
    ShotVersions, HQCVersions, ClientVersions


# Register your models here.
class ShotStatusFields(admin.ModelAdmin):
    list_display = [f.name for f in ShotStatus._meta.fields]
    list_per_page = 15

# Register your models here.
class ShotsFields(admin.ModelAdmin):
    list_display = [f.name for f in Shots._meta.fields]
    list_per_page = 15
    list_filter = ['task_type','sequence__project','status']

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

class SequenceFields(admin.ModelAdmin):
    list_display = [f.name for f in Sequence._meta.fields]
    list_per_page = 15
    search_fields = ['name']

class ProjectFields(admin.ModelAdmin):
    list_display = [f.name for f in Projects._meta.fields]
    list_per_page = 15
    search_fields = ['name']

admin.site.register(ShotStatus, ShotStatusFields)
admin.site.register(Complexity)
admin.site.register(Clients)
admin.site.register(Projects, ProjectFields)
admin.site.register(Sequence, SequenceFields)
admin.site.register(Task_Type)
admin.site.register(Shots, ShotsFields)
admin.site.register(MyTask, MyTaskFields)
admin.site.register(Assignments)
admin.site.register(Qc_Assignment)
admin.site.register(Groups)
admin.site.register(Channels)
admin.site.register(HeadQc_Assignment)
admin.site.register(HeadQCTeam)
admin.site.register(Permission_Groups)
admin.site.register(Folder_Permissions)
admin.site.register(ShotVersions)
admin.site.register(HQCVersions)
admin.site.register(ClientVersions)
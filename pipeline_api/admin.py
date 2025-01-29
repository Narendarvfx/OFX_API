from django.contrib import admin

from pipeline_api.models import ShotConfig, Dependencies, AssetTypes, ProjectConfig, LinuxProjectConfig, \
    WinProjectConfig, WinNukeVersions, LinuxNukeVersions, SBDesktopVersion
from django.utils.translation import gettext_lazy as _

def duplicate_records(modeladmin, request, queryset):
    for obj in queryset:
        obj.pk = None  # This will create a new object rather than updating the existing one
        obj.save()
    modeladmin.message_user(request, _("Selected records have been duplicated successfully."))

duplicate_records.short_description = _("Duplicate selected records")

# Register your models here.
@admin.register(ShotConfig)
class ShotConfigFields(admin.ModelAdmin):
    # list_display = [f.name for f in ShotConfig._meta.fields]
    list_per_page = 15
    search_fields = ['shot']
    autocomplete_fields = ['shot', 'dependencies', ]

@admin.register(Dependencies)
class DependencieFields(admin.ModelAdmin):
    list_display = [f.name for f in Dependencies._meta.fields]
    list_per_page = 15
    search_fields = ['shot']
    autocomplete_fields = ['shot']
    save_as = True
@admin.register(AssetTypes)
class AssetTypeFields(admin.ModelAdmin):
    list_display = [f.name for f in AssetTypes._meta.fields]
    list_per_page = 15
    search_fields = ['name']
    save_as = True
@admin.register(ProjectConfig)
class ProjectConfigFields(admin.ModelAdmin):
    list_display = ['client','project']
    list_display.insert(3, 'win_drive')
    list_display.insert(4, 'win_config')
    list_display.insert(5, 'linux_drive')
    list_display.insert(6, 'linux_config')
    list_per_page = 15
    search_fields = ['project__name']
    autocomplete_fields = ['win_config','linux_config',]
    save_as = True
    actions = [duplicate_records]  # Register the custom action

    def client(self, obj):
        return obj.project.client.name
    def win_config(self, obj):
        return obj.win_config.nuke_config_path

    def win_drive(self, obj):
        return obj.win_config.mnt_drive
    def linux_config(self, obj):
        return obj.linux_config.nuke_config_path

    def linux_drive(self, obj):
        return obj.linux_config.mnt_drive

@admin.register(WinProjectConfig)
class WinProjectConfigFields(admin.ModelAdmin):
    list_display = ['mnt_drive','nuke_config_path']
    list_per_page = 15
    search_fields = ['nuke_config_path']
    save_as = True
    actions = [duplicate_records]  # Register the custom action
@admin.register(LinuxProjectConfig)
class LinuxProjectConfigFields(admin.ModelAdmin):
    list_display = ['mnt_drive','nuke_config_path']
    list_per_page = 15
    search_fields = ['nuke_config_path']
    save_as = True
    actions = [duplicate_records]  # Register the custom action
@admin.register(WinNukeVersions)
class WinNukeVersionsFields(admin.ModelAdmin):
    list_display = [f.name for f in WinNukeVersions._meta.fields]
    list_per_page = 15
    search_fields = ['name']
    save_as = True
    actions = [duplicate_records]  # Register the custom action
@admin.register(LinuxNukeVersions)
class LinuxNukeVersionsFields(admin.ModelAdmin):
    list_display = [f.name for f in LinuxNukeVersions._meta.fields]
    list_per_page = 15
    search_fields = (['name'])
    save_as = True
    actions = [duplicate_records]  # Register the custom action

@admin.register(SBDesktopVersion)
class SBDesktopVersionFields(admin.ModelAdmin):
    list_display = ['version','download_path']
    list_per_page = 15
    search_fields = ['version']
    save_as = True
    ordering = ('-version',)
    actions = [duplicate_records]  # Register the custom action
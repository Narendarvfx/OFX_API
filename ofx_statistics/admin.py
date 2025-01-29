#  Copyright (c) 2023.
#  Designed & Developed by Narendar Reddy G, OscarFX Private Limited
#  All rights reserved.
import csv

from django.contrib import admin
from django.contrib.admin import DateFieldListFilter
from django.http import HttpResponse

from ofx_statistics.models import EmployeeDailyStatistics, TLDailyStatistics, ClientStatistics, \
    LeadDailyStatistics, ClientArtistStatistics

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

@admin.register(EmployeeDailyStatistics)
class EmployeeDailyStatisticsAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ('id','employee','tmd','amd','rwh','aeh','ash','leaves','logDate','creation_date','modified_date')
    list_per_page = 15
    list_filter = (('logDate', DateFieldListFilter),)
    date_hierarchy = 'logDate'
    search_fields = ['employee__fullName', 'employee__employee_id']
    actions = ["export_as_csv"]
@admin.register(TLDailyStatistics)
class TLDailyStatisticsAdmin(admin.ModelAdmin):
    list_display = ('id','tl','artists_count','team_ability','tmd','amd','rwh','aeh','ash','leaves','logDate','creation_date','modified_date')
    list_per_page = 15
    list_filter = (('logDate', DateFieldListFilter),)
    date_hierarchy = 'logDate'
    search_fields = ['tl__fullName', 'tl__employee_id']
    filter_horizontal = ('artists',)
@admin.register(LeadDailyStatistics)
class LeadDailyStatisticsAdmin(admin.ModelAdmin):
    list_display = ('id','lead','role','artists_count','team_ability','tmd','amd','shot_amd','rwh','aeh','ash','leaves','logDate','creation_date','modified_date')
    list_per_page = 15
    list_filter = (('logDate', DateFieldListFilter),'role')
    date_hierarchy = 'logDate'
    search_fields = ['lead__fullName', 'lead__employee_id']
    filter_horizontal = ('artists',)

@admin.register(ClientStatistics)
class ClientStatisticsAdmin(admin.ModelAdmin):
    list_display = ('id','client','project','dep',"tmd","amd","highest_ver","highest_ver_shotCount","retake_per","artistcount","artistTMD","missedEta","totalshots")
    list_per_page = 15
    list_filter = ('client','project','dep')
    search_fields = ['client__name', 'project__name']
@admin.register(ClientArtistStatistics)
class ClientStatisticsAdmin(admin.ModelAdmin):
    list_display = ('id','client','project','dep','artist', 'tl', 'supervisor', 'hod', "tmd","amd","shotsCount" )
    list_per_page = 15
    list_filter = ('client','project','dep')
    search_fields = ['client__name', 'project__name', 'artist__fullName']

# Register your models here.
# admin.site.register(EmployeeDailyStatistics)
# admin.site.register(TLDailyStatistics)

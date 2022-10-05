from django.conf.urls import url
from . import api, views
from .api import ShotsDataFilter

urlpatterns = [
    ################## Web Urls ######################
    url(r'^production/production_report/$', views.production_reports, name='Client reports'),
    url(r'^production/export_prod_report/$', views.export_prod_report, name='Client reports'),
    url(r'^production/export_ver_report/$', views.export_ver_report, name='Version reports'),
    url(r'^production/teamleadreports$', views.teamlead_report, name="Team Lead Reports"),
    url(r'^production/studio_reports$', views.studio_report, name="Studio Reports"),
    url(r'^production/department_reports$', views.department_report, name="Team Lead Reports"),
    url(r'^production/artist_reports$', views.artist_report, name="Artist Reports"),
    url(r'^production/version_reports$', views.version_report, name="Version Reports"),
    url(r'^production/teamleadreports_export/$', views.export_teamlead_report, name='TeamLeadReports'),
    url(r'^production/artistreports_export/$', views.export_artist_report, name='Artist Reports'),
    url(r'^production/dept_reports_export/$', views.export_dept_report, name='TeamLeadReports'),
    url(r'^production/studio_reports_export/$', views.export_studio_report, name='StudioReports'),
    url(r'^production/client_report/$', views.reports, name="Multi Reports"),
    url(r'^production/reports/multi_export/$', views.reports_export, name="Multi Reports"),

    url(r'^production/projects/', views.projects, name="Projects"),
    url(r'^production/clients/', views.clients, name="Clients"),

    url(r'^production/time_card/$',views.time_card, name="Time Card"),

    ########## API URLS #################
    url(r'^api/production/status/$', api.StatusInfo.as_view(), name='Status API'),
    url(r'^api/production/localities/$', api.LocalityInfo.as_view(), name='Locality API'),
    url(r'^api/production/complexity/$', api.ComplexityInfo.as_view(), name='Complexity API'),

    # Client Urls
    url(r'^api/production/clients/$', api.ClientDetail.as_view(), name='Client API'),
    url(r'^api/production/clients/(?P<client_id>\d+)/$', api.ClientUpdate.as_view(), name='Client Update API'),

    # Project Urls
    url(r'^api/production/projects/$', api.ProjectDetail.as_view(), name='Project API'),
    url(r'^api/production/projects/(?P<client_id>\d+)/$', api.ProjectByClient.as_view(), name='Project API'),
    url(r'^api/production/projects/(?P<projectId>\d+)/$', api.ProjectUpdate.as_view(), name='Project API'),

    # Sequence Urls
    url(r'^api/production/projects/sequence/$', api.SequenceDetail.as_view(), name='Sequence API'),
    url(r'^api/production/projects/sequence/(?P<projectId>\d+)/$', api.ProjectSequenceData.as_view(), name='Projects Sequence API'),

    # Shots Urls
    url(r'^api/production/shots/$', api.ShotsData.as_view(), name='Shots API'),
    url(r'^api/production/production_sheet/$', api.ProductSheet.as_view(), name='Production Shots API'),
    url(r'^api/production/shots_filter/$', ShotsDataFilter.as_view(), name='Shots Filters API'),
    url(r'^api/production/projects/sequence/shots/(?P<sequenceId>\d+)/$', api.ProjectShotsData.as_view(), name='Projects Shots API'),
    url(r'^api/production/shots/(?P<shotId>\d+)/$', api.ShotUpdate.as_view(), name='Shot Update API'),

    # MyTask Urls
    url(r'^api/production/mytask/$', api.MyTaskData.as_view(), name='MyTask API'),
    url(r'^api/production/mytask/shot/(?P<shotId>\d+)/$', api.MyTaskShotData.as_view(), name='MyTask API'),
    url(r'^api/production/mytask/(?P<taskId>\d+)/$', api.MyTaskDetail.as_view(), name='MyTask API'),
    url(r'^api/production/mytask/artist/(?P<artistid>\d+)/$', api.MyTaskArtistData.as_view(), name='MyTask API'),

    # Assignment Urls
    url(r'^api/production/shot/assignments/$', api.ShotAssignment.as_view(), name='MyTask API'),

    # Lead Urls
    url(r'^api/production/leads/shots/$', api.LeadShotsData.as_view(), name='Projects Shots API'),
    url(r'^api/production/shots/leads_filter/$', api.LeadsData.as_view(), name='Leads Shots API'),

    # Channel Urls
    url(r'^api/production/channels/(?P<shotId>\d+)/$', api.ChannelsData.as_view(), name='Channels API'),
    url(r'^api/production/channels/', api.ChannelsPostData.as_view(), name='Channels API'),

    # Channel group urls
    url(r'^api/production/groups/(?P<groupId>[\w\-]+)/$', api.GroupsData.as_view(), name='Channels API'),
    url(r'^api/production/groups/', api.GroupsPostData.as_view(), name='Channels API'),

    # Qc Assignment urls
    url(r'^api/production/update_qc/(?P<qcId>\d+)/$', api.QCDataById.as_view(), name='QC Update API'),
    url(r'^api/production/qc/(?P<teamId>\d+)/$', api.QCDataByTeamId.as_view(), name='QC Assignments API'),
    url(r'^api/production/qc/qc/', api.QCData.as_view(), name='QC Assignments API'),

    # Folder Permission Url
    url(r'^api/production/permissions_groups/', api.Perm_Groups.as_view(), name='Permission Groups'),

    # Artist to Lead Version urls
    url(r'^api/production/shotversions/$', api.ShotVersionsAPI.as_view(), name="Shot Versions"),
    url(r'^api/production/shotversions/(?P<shotId>\d+)/$', api.LastShotVersionById.as_view(), name="Shot Versions"),
    url(r'^api/production/allshotversions/(?P<verId>\d+)/$', api.ShotVersionsById.as_view(), name="Shot Versions"),

    # Lead to Qc Version urls
    url(r'^api/production/qcversions/$', api.QcVersionsAPI.as_view(), name="Qc Versions"),
    url(r'^api/production/qcversions/(?P<shotId>\d+)/$', api.LastQcVersionById.as_view(), name="Qc Versions"),
    url(r'^api/production/allqcversions/(?P<verId>\d+)/$', api.QcVersionsById.as_view(), name="Qc Versions"),

    # Client Version urls
    url(r'^api/production/client_versions/$', api.ClientVersionsAPI.as_view(), name="Client Versions"),
    url(r'^api/production/client_versions/(?P<shotId>\d+)/$', api.LastClientVersionById.as_view(), name="Client Versions"),
    url(r'^api/production/all_client_versions/(?P<verId>\d+)/$', api.ClientVersionsById.as_view(), name="Client Versions"),

    #Task Help Urls
    url(r'^api/production/taskhelp_main/$', api.TaskHelp_Main_API.as_view(), name="Task Help Main"),
    url(r'^api/production/taskhelp_main/(?P<parentId>\d+)/$', api.TaskHelpMainUpdate.as_view(), name='Task Help Main Update API'),
    url(r'^api/production/taskhelp_lead/$', api.TaskHelp_Lead_API.as_view(), name="Task Help Lead"),
    url(r'^api/production/taskhelp_artist/$', api.TaskHelp_Artist_API.as_view(), name="Task Help Artist"),
    url(r'^api/production/taskhelp_artist/(?P<taskId>\d+)/$', api.TaskHelpArtistDetail.as_view(), name="Task Help Artist"),
    url(r'^api/production/taskhelp_artist/artist/(?P<artistId>\d+)/$', api.TaskHelpArtistData.as_view(), name='Task Help Artist By Id'),

    #ShotLogs url
    url(r'^api/production/shotlogs/$', api.ShotLogsData.as_view(), name='Shots API'),
    url(r'^api/production/daylogs/$', api.DayLogsData.as_view(), name='DayLogs API'),
    url(r'^api/production/taskdaylogs/$', api.TaskDayLogsData.as_view(), name='TaskDayLogs API'),
    url(r'^api/production/timelogs/$', api.TimeLogsData.as_view(), name='TimeLogs API'),
    url(r'^api/production/timecards/$', api.TimeCardData.as_view(), name='TimeLogs API'),
    url(r'^api/production/shot/timecards/(?P<shotId>\d+)$', api.ShotTimeCardData.as_view(), name='Get Shot TimeLogs API'),
    url(r'^api/production/timecards/(?P<taskId>\d+)$', api.UpdateTimeCard.as_view(), name='Update TimeLogs API'),
    url(r'^api/production/lightboxdata/$', api.LightBoxData.as_view(), name='TimeLogs API'),
    # url(r'^api/production/daylogs/(?P<shotId>\d+)/$', api.DayLogsByShot.as_view(), name='DayLogs API'),

    #Teamlead Report Urls
    url(r'^api/production/teamleadreports/$', api.TeamLeadReports.as_view(), name='TeamLeadReports'),

    #Department Report Urls
    url(r'^api/production/teamleadreports/$', api.TeamLeadReports.as_view(), name='TeamLeadReports'),

    ## Team Lead Urls
    url(r'api/production/custom/teamleadreports/$', api.CustomLeadReports.as_view(), name="Custom Lead Reports"),

    ## Artist Urls
    url(r'api/production/custom/artist_reports/$', api.CustomArtistReports.as_view(), name="Custom Lead Reports"),

    #Department Urls
    url(r'api/production/custom/dep_reports/$', api.CustomDeptReports.as_view(), name="Custom Dept Reports"),

    #Studio Urls
    url(r'api/production/custom/studio_reports/$', api.CustomStudioReports.as_view(), name="Custom Studio Reports"),

    ## Chart Urls
    url(r'api/production/status_count/$', api.StatusCount.as_view(), name="Status Count")
]
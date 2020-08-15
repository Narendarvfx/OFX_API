from django.conf.urls import url
from . import api

urlpatterns = [
    url(r'^api/production/status/$', api.StatusInfo.as_view(), name='Status API'),
    url(r'^api/production/complexity/$', api.ComplexityInfo.as_view(), name='Complexity API'),

    # Client Urls
    url(r'^api/production/clients/$', api.ClientDetail.as_view(), name='Client API'),
    url(r'^api/production/clients/(?P<client_id>\d+)/$', api.ClientUpdate.as_view(), name='Client Update API'),

    # Project Urls
    url(r'^api/production/projects/$', api.ProjectDetail.as_view(), name='Project API'),
    url(r'^api/production/projects/(?P<projectId>\d+)/$', api.ProjectUpdate.as_view(), name='Project API'),
    url(r'^api/production/fileexplorer/(?P<projectId>\d+)/$', api.FileExplorer.as_view(), name='File Explorer'),

    # Sequence Urls
    url(r'^api/production/projects/sequence/$', api.SequenceDetail.as_view(), name='Sequence API'),
    url(r'^api/production/projects/sequence/(?P<projectId>\d+)/$', api.ProjectSequenceData.as_view(), name='Projects Sequence API'),
    # url(r'^api/production/projects/(?P<projectId>\d+)/$', api.ProjectUpdate.as_view(), name='Project API'),
    # url(r'^api/production/fileexplorer/(?P<projectId>\d+)/$', api.FileExplorer.as_view(), name='File Explorer'),

    # Shots Urls
    url(r'^api/production/shots/$', api.ShotsData.as_view(), name='Shots API'),
    url(r'^api/production/projects/sequence/shots/(?P<sequenceId>\d+)/$', api.ProjectShotsData.as_view(), name='Projects Shots API'),
    url(r'^api/production/shots/(?P<shotId>\d+)/$', api.ShotUpdate.as_view(), name='Shot Update API'),

    # MyTask Urls
    url(r'^api/production/mytask/$', api.MyTaskData.as_view(), name='MyTask API'),
    url(r'^api/production/mytask/shot/(?P<shotId>\d+)/$', api.MyTaskShotData.as_view(), name='MyTask API'),
    url(r'^api/production/mytask/(?P<taskId>\d+)/$', api.MyTaskDetail.as_view(), name='MyTask API'),

    # Assignment Urls
    url(r'^api/production/shot/assignments/$', api.ShotAssignment.as_view(), name='MyTask API'),
]
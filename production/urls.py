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

    # Shots Urls
    url(r'^api/production/shots/$', api.ShotsData.as_view(), name='Shots API'),
]
#  Copyright (c) 2023.
#  Designed & Developed by Narendar Reddy G, OscarFX Private Limited
#  All rights reserved.
from django.conf.urls import url

from pipeline_api import api

urlpatterns = [
    url(r'^api/ofx_pipeline/shots/$', api.PipelineShotsData.as_view(), name='Shots Config API'),
    url(r'^api/ofx_pipeline/shots/dependencies/$', api.ShotsDependenciesData.as_view(), name='Shots Config API'),
    url(r'^api/ofx_pipeline/project_config/$', api.ProjectConfigApi.as_view(), name='Project Config API'),
    url(r'^api/sb_desktop/get_latest_version/$', api.SBLatestVersion.as_view(), name='SB Desktop Latest Version API'),
]
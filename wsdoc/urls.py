#  Copyright (c) 2023.
#  Designed & Developed by Narendar Reddy G, OscarFX Private Limited
#  All rights reserved.

from django.urls import path
from . import views

urlpatterns = [
    path('', views.homePage, name='homePage'),
    # path('async/', views.homePage, name='homePage'),
]
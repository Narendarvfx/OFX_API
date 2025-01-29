#  Copyright (c) 2023.
#  Designed & Developed by Narendar Reddy G, OscarFX Private Limited
#  All rights reserved.

from django.urls import path
from . import views

urlpatterns = [
    path('getwstoken/', views.getwstoken, name='getwstoken'),
]
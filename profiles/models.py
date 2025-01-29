#  Copyright (c) 2023.
#  Designed & Developed by Narendar Reddy G, OscarFX Private Limited
#  All rights reserved.
from django.db.models import signals
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    """
    User Profile
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_creation_date = models.DateTimeField(auto_now_add=True)
    password_changed = models.BooleanField(default=False, blank=True)
    force_password_change = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username
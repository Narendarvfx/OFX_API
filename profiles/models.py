from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    """
    User Profile
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_creation_date = models.DateTimeField(auto_now_add=True)
    password_changed = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return self.user.username
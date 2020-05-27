from django.contrib import admin
from production.models import Clients, Projects, Status, Complexity, Shots

# Register your models here.
admin.site.register(Status)
admin.site.register(Complexity)
admin.site.register(Clients)
admin.site.register(Projects)
admin.site.register(Shots)
from django.contrib import admin
from production.models import Clients, Projects, ShotStatus, Complexity, Shots, Sequence, Task_Type, MyTask, \
    Assignments, Channels, Groups

# Register your models here.
admin.site.register(ShotStatus)
admin.site.register(Complexity)
admin.site.register(Clients)
admin.site.register(Projects)
admin.site.register(Sequence)
admin.site.register(Task_Type)
admin.site.register(Shots)
admin.site.register(MyTask)
admin.site.register(Assignments)
admin.site.register(Groups)
admin.site.register(Channels)
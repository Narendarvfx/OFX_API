from django.db.models import Count

from production.models import Shots

shots = Shots.objects.values('name','task_type').annotate(records=Count('name')).filter(records__gt=1)

for shot in shots:
    filter = Shots.objects.filter(name=shot['name'], task_type=shot['task_type'])
    print(filter)
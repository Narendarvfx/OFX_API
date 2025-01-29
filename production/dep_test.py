#  Copyright (c) 2023.
#  Designed & Developed by Narendar Reddy G, OscarFX Private Limited
#  All rights reserved.

from unittest import TestCase

from django.db.models import Count

from production.models import Shots, Clients


class DeptTestCase(TestCase):
    def test_dep_suite(self):
        clients = Clients.objects.select_related('locality').all()
        for client in clients:
            yts = Shots.objects.select_related('sequence__project', 'sequence', 'task_type',
                                               'sequence__project__client',
                                               'status', 'complexity', 'team_lead', 'artist', 'qc_name', 'location',
                                               'sequence__project__client__locality').filter(
                sequence__project__client=client).all().annotate(yts_status=Count('YTS'))

            _dict = {
                'yts': yts,
            }
            print(_dict)
            break;

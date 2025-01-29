#  Copyright (c) 2023.
#  Designed & Developed by Narendar Reddy G, OscarFX Private Limited
#  All rights reserved.

import json
from unittest import TestCase

from django.db.models import Count, Q, Sum, Aggregate

from production.models import Shots, Clients, ShotStatus
from production.serializers import ShotsSerializer


class DepartmentTestCase(TestCase):
    def test_dept_version(self):
        clients = Clients.objects.select_related('locality').all()
        status = Shots.objects.values('sequence__project__client','status__code').filter(sequence__project__client__name="SHP").annotate(status_count=Count('status__code')).values('sequence__project__client__name','status__code','status_count').order_by('sequence__project__client__name','sequence__project__name')
        print(len(status))
        for sta in status:
            print(sta)
        # totalshots_i = Shots.objects.select_related('sequence__project', 'sequence', 'task_type',
        #                                           'sequence__project__client',
        #                                           'status', 'complexity', 'team_lead', 'artist', 'qc_name', 'location',
        #                                           'sequence__project__client__locality').filter(
        #     sequence__project__client__in=[x.id for x in clients]).values('id', 'sequence__project__client__id')
        # yts_i = Shots.objects.select_related('sequence__project', 'sequence', 'task_type', 'sequence__project__client',
        #                                    'status', 'complexity', 'team_lead', 'artist', 'qc_name', 'location',
        #                                    'sequence__project__client__locality').filter(
        #     sequence__project__client__in=[x.id for x in clients], status__code__in=['YTA', 'ATL', 'YTS']).values('id',
        #                                                                                                'sequence__project__client__id')
        # wip_i = Shots.objects.select_related('sequence__project', 'sequence', 'task_type', 'sequence__project__client',
        #                                    'status', 'complexity', 'team_lead', 'artist', 'qc_name', 'location',
        #                                    'sequence__project__client__locality').filter(
        #     sequence__project__client__in=[x.id for x in clients], status__code__in=['WIP', 'STC', 'LRT', 'STQ', 'IRT', 'LAP']).values('id',
        #                                                                                                'sequence__project__client__id')
        # completed_i = Shots.objects.select_related('sequence__project', 'sequence', 'task_type', 'sequence__project__client',
        #                                    'status', 'complexity', 'team_lead', 'artist', 'qc_name', 'location',
        #                                    'sequence__project__client__locality').filter(
        #     sequence__project__client__in=[x.id for x in clients], status__code__in=['CAP', 'DTC', 'IAP']).values('id',
        #                                                                                                           'sequence__project__client__id')
        # r_data = {}
        #
        # for x in totalshots_i:
        #     ClinetKey = 'key'+str(x['sequence__project__client__id']);
        #     if r_data.get(ClinetKey,None) is None:
        #         r_data[ClinetKey]={
        #             'client_id': x['sequence__project__client__id'],
        #             'totalshots': 0,
        #             'yts': 0,
        #             'wip': 0,
        #             'completed': 0,
        #             }
        #     r_data[ClinetKey]['totalshots'] = r_data[ClinetKey]['totalshots'] + 1
        # for x in yts_i:
        #     ClinetKey = 'key'+str(x['sequence__project__client__id']);
        #     if r_data.get(ClinetKey,None) is None:
        #         r_data[ClinetKey]={
        #             'client_id': x['sequence__project__client__id'],
        #             'totalshots': 0,
        #             'yts': 0,
        #             'wip': 0,
        #             'completed': 0,
        #             }
        #     r_data[ClinetKey]['yts'] = r_data[ClinetKey]['yts'] + 1
        # for x in wip_i:
        #     ClinetKey = 'key'+str(x['sequence__project__client__id']);
        #     if r_data.get(ClinetKey,None) is None:
        #         r_data[ClinetKey]={
        #             'client_id': x['sequence__project__client__id'],
        #             'totalshots': 0,
        #             'yts': 0,
        #             'wip': 0,
        #             'completed': 0,
        #             }
        #     r_data[ClinetKey]['wip'] = r_data[ClinetKey]['wip'] + 1
        # for x in completed_i:
        #     ClinetKey = 'key'+str(x['sequence__project__client__id']);
        #     if r_data.get(ClinetKey,None) is None:
        #         r_data[ClinetKey]={
        #             'client_id': x['sequence__project__client__id'],
        #             'totalshots': 0,
        #             'yts': 0,
        #             'wip': 0,
        #             'completed': 0,
        #             }
        #     r_data[ClinetKey]['completed'] = r_data[ClinetKey]['completed'] + 1
        # print(r_data)

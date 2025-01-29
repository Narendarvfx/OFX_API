from rest_framework.response import Response
from rest_framework.views import APIView

from pipeline_api.models import ShotConfig, Dependencies, ProjectConfig, SBDesktopVersion
from pipeline_api.serializers import ApiShotsSerializer, ShotsDependencySerializer, ProjectConfigSerializer, \
    SBDesktopVersionSerializer
from production.models import Shots
from production.serializers import ShotTimeLogSerializer


class PipelineShotsData(APIView):

    def get(self, request, format=None):
        query_params = self.request.query_params
        argumentos = {}
        if query_params.get('shot_id'):
            argumentos['shot__pk'] = query_params.get('shot_id')

        if query_params.get('client_id'):
            clients = []
            for client in query_params.get('client_id').split('|'):
                clients.append(client)
            argumentos['shot__sequence__project__client__pk__in'] = clients
        if query_params.get('client_name'):
            client_names = []
            for client_name in query_params.get('client_name').split('|'):
                client_names.append(client_name)
            argumentos['shot__sequence__project__client__name__in'] = client_names

        if query_params.get('project_id'):
            projects = []
            for project in query_params.get('project_id').split('|'):
                projects.append(project)
            argumentos['shot__sequence__project__pk__in'] = projects
        if query_params.get('project_name'):
            project_names = []
            for project_name in query_params.get('project_name').split('|'):
                project_names.append(project_name)
            argumentos['shot__sequence__project__name__in'] = project_names

        if query_params.get('status'):
            status = []
            for stat in query_params.get('status').split('|'):
                status.append(stat)
            argumentos['shot__status__code__in'] = status
        if query_params.get('dept'):
            depts = []
            for dept in query_params.get('dept').split('|'):
                depts.append(dept)
            argumentos['shot__task_type__name__in'] = depts
        if query_params.get('shot_ids'):
            shot_ids = []
            for shot_id in query_params.get('shot_ids').split('|'):
                shot_ids.append(shot_id)
            argumentos['shot__pk__in'] = shot_ids
            queryset = ShotConfig.objects.prefetch_related('shot__timelogs','shot__artists','shot__artists__role','shot__artists__department','shot__artists__role__permissions').select_related('shot','shot__sequence', 'shot__task_type',
                                                                                 'shot__sequence__project',
                                                                                 'shot__sequence__project__client', 'shot__status',
                                                                                 'shot__complexity',
                                                                                 'shot__team_lead', 'shot__artist', 'shot__location',
                                                                                 'shot__sequence__project__client__locality','shot__status__status_segregation','shot__supervisor','shot__hod').filter(**argumentos)
        elif len(argumentos) > 0:
            queryset = ShotConfig.objects.prefetch_related('shot__timelogs','shot__artists','shot__artists__role','shot__artists__department','shot__artists__role__permissions').select_related('shot','shot__sequence', 'shot__task_type',
                                                                                 'shot__sequence__project',
                                                                                 'shot__sequence__project__client', 'shot__status',
                                                                                 'shot__complexity',
                                                                                 'shot__team_lead', 'shot__artist', 'shot__location',
                                                                                 'shot__sequence__project__client__locality','shot__status__status_segregation','shot__supervisor','shot__hod').filter(
                **argumentos).exclude(shot__sequence__project__status="ARCHIVED")
        else:
            # queryset = Shots.objects.all()
            queryset = ShotConfig.objects.prefetch_related('shot__timelogs','shot__artists','shot__artists__role','shot__artists__department','shot__artists__role__permissions').select_related('shot','shot__sequence', 'shot__task_type',
                                                                                 'shot__sequence__project',
                                                                                 'shot__sequence__project__client', 'shot__status',
                                                                                 'shot__complexity',
                                                                                 'shot__team_lead', 'shot__artist', 'shot__location',
                                                                                 'shot__sequence__project__client__locality','shot__status__status_segregation','shot__supervisor','shot__hod').all()

        serializer = ApiShotsSerializer(instance=queryset, many=True)
        # shots_data = []
        # for _shotdata in serializer.data:
        #     total_spent = 0
        #     for spent in _shotdata['timelogs']:
        #         total_spent += spent['spent_hours']
        #     _tim = {
        #         'total_spent': total_spent / 8
        #     }
        #     _shotdata.update(_tim)
        #     shots_data.append(_shotdata)

        return Response(serializer.data)

class ShotsDependenciesData(APIView):

    def get(self, request, format=None):
        query_params = self.request.query_params
        argumentos = {}
        if query_params.get('shot_id'):
            argumentos['shot__pk'] = query_params.get('shot_id')

        if query_params.get('client_id'):
            clients = []
            for client in query_params.get('client_id').split('|'):
                clients.append(client)
            argumentos['shot__sequence__project__client__pk__in'] = clients
        if query_params.get('client_name'):
            client_names = []
            for client_name in query_params.get('client_name').split('|'):
                client_names.append(client_name)
            argumentos['shot__sequence__project__client__name__in'] = client_names

        if query_params.get('project_id'):
            projects = []
            for project in query_params.get('project_id').split('|'):
                projects.append(project)
            argumentos['shot__sequence__project__pk__in'] = projects
        if query_params.get('project_name'):
            project_names = []
            for project_name in query_params.get('project_name').split('|'):
                project_names.append(project_name)
            argumentos['shot__sequence__project__name__in'] = project_names

        if query_params.get('status'):
            status = []
            for stat in query_params.get('status').split('|'):
                status.append(stat)
            argumentos['shot__status__code__in'] = status
        if query_params.get('dept'):
            depts = []
            for dept in query_params.get('dept').split('|'):
                depts.append(dept)
            argumentos['shot__task_type__name__in'] = depts
        if query_params.get('shot_ids'):
            shot_ids = []
            for shot_id in query_params.get('shot_ids').split('|'):
                shot_ids.append(shot_id)
            argumentos['shot__pk__in'] = shot_ids
            queryset = Dependencies.objects.prefetch_related('shot__artists','shot__artists__role','shot__artists__department','shot__artists__role__permissions').select_related('shot','shot__sequence', 'shot__task_type',
                                                                                 'shot__sequence__project',
                                                                                 'shot__sequence__project__client', 'shot__status',
                                                                                 'shot__complexity',
                                                                                 'shot__team_lead', 'shot__artist', 'shot__location',
                                                                                 'shot__sequence__project__client__locality','shot__status__status_segregation','shot__supervisor','shot__hod').filter(**argumentos)
        elif len(argumentos) > 0:
            queryset = Dependencies.objects.prefetch_related('shot__artists','shot__artists__role','shot__artists__department','shot__artists__role__permissions').select_related('shot','shot__sequence', 'shot__task_type',
                                                                                 'shot__sequence__project',
                                                                                 'shot__sequence__project__client', 'shot__status',
                                                                                 'shot__complexity',
                                                                                 'shot__team_lead', 'shot__artist', 'shot__location',
                                                                                 'shot__sequence__project__client__locality','shot__status__status_segregation','shot__supervisor','shot__hod').filter(
                **argumentos).exclude(shot__sequence__project__status="ARCHIVED")
        else:
            # queryset = Shots.objects.all()
            queryset = Dependencies.objects.prefetch_related('shot__artists','shot__artists__role','shot__artists__department','shot__artists__role__permissions').select_related('shot','shot__sequence', 'shot__task_type',
                                                                                 'shot__sequence__project',
                                                                                 'shot__sequence__project__client', 'shot__status',
                                                                                 'shot__complexity',
                                                                                 'shot__team_lead', 'shot__artist', 'shot__location',
                                                                                 'shot__sequence__project__client__locality','shot__status__status_segregation','shot__supervisor','shot__hod').all()

        serializer = ShotsDependencySerializer(instance=queryset, many=True)
        # shots_data = []
        # for _shotdata in serializer.data:
        #     total_spent = 0
        #     for spent in _shotdata['timelogs']:
        #         total_spent += spent['spent_hours']
        #     _tim = {
        #         'total_spent': total_spent / 8
        #     }
        #     _shotdata.update(_tim)
        #     shots_data.append(_shotdata)

        return Response(serializer.data)


class ProjectConfigApi(APIView):
    def get(self, request, format=None):
        query_params = self.request.query_params
        argumentos = {}
        if query_params.get('project_id'):
            argumentos['project__pk'] = query_params.get('project_id')
        if query_params.get('project_name'):
            argumentos['project__name'] = query_params.get('project_name')
        if len(argumentos) > 0:
            queryset = ProjectConfig.objects.select_related('project','project__client','win_config','linux_config').filter(
                **argumentos)
        else:
            queryset = ProjectConfig.objects.select_related('project','project__client','win_config','linux_config').all()
        serializer = ProjectConfigSerializer(instance=queryset, many=True)

        return Response(serializer.data)

class SBLatestVersion(APIView):
    def get(self, request, format=None):
        queryset = SBDesktopVersion.objects.latest('version')
        serializer = SBDesktopVersionSerializer(instance=queryset)

        return Response(serializer.data)
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from production.models import Clients, Projects, ShotStatus, Shots, Complexity, Sequence, MyTask, Assignments, Channels, \
    Groups, Qc_Assignment, Permission_Groups, ShotVersions, TaskHelp_Main, TaskHelp_Lead, \
    TaskHelp_Artist, ShotLogs, Locality, DayLogs, TeamLead_Week_Reports, QCVersions, ClientVersions
from production.reports.custom_artist_reports import calculate_artist_data
from production.reports.custom_dep_reports import calculate_dept_data
from production.reports.custom_lead_reports import calculate_data
from production.reports.custom_studio_reports import calculate_studio_data
from production.serializers import ClientSerializer, ProjectSerializer, StatusSerializer, ShotsSerializer, \
    ShotsPostSerializer, ComplexitySerializer, SequenceSerializer, SequencePostSerializer, MyTaskSerializer, \
    MyTaskPostSerializer, MyTaskShotSerializer, AssignmentSerializer, AssignmentPostSerializer, MyTaskArtistSerializer, \
    ChannelsSerializer, ChannelsPostSerializer, GroupsSerializer, QCSerializer, TeamQCSerializer, \
    MyTaskUpdateSerializer, PGSerializer, ProjectClientSerializer, \
    ProjectPostSerializer, MyTaskStatusSerializer, ShotVersionsSerializer, AllShotVersionsSerializer, \
    TaskHelpMainSerializer, TaskHelpLeadSerializer, \
    TaskHelpArtistSerializer, TaskHelpMainPostSerializer, TaskHelpArtistPostSerializer, TaskHelpArtistUpdateSerializer, \
    TaskHelpArtistStatusSerializer, ShotLogsSerializer, ShotLogsPostSerializer, LocalitySerializer, DayLogsSerializer, \
    DayLogsPostSerializer, TeamReportSerializer, QcVersionsSerializer, AllShotQcVersionsSerializer, \
    ClientVersionsSerializer, AllShotClientVersionsSerializer


class StatusInfo(APIView):

    def get(self, request, format=None):
        status = ShotStatus.objects.all()
        serializer = StatusSerializer(status, many=True, context={"request": request})
        return Response(serializer.data)


class LocalityInfo(APIView):

    def get(self, request, format=None):
        locality = Locality.objects.all()
        serializer = LocalitySerializer(locality, many=True, context={"request": request})
        return Response(serializer.data)


class ComplexityInfo(APIView):

    def get(self, request, format=None):
        complexity = Complexity.objects.all()
        serializer = ComplexitySerializer(complexity, many=True, context={"request": request})
        return Response(serializer.data)


class ClientDetail(APIView):

    def get(self, request, format=None):
        query_params = self.request.query_params
        if query_params:
            locality = query_params.get('locality', None)
            print(locality)
            if locality:
                client = Clients.objects.filter(locality__name=locality)
            else:
                client = Clients.objects.all()
        else:
            client = Clients.objects.all()
        serializer = ClientSerializer(client, many=True, context={"request": request})
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ClientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClientUpdate(APIView):

    def get(self, request, client_id, format=None):
        client = Clients.objects.get(id=client_id)
        serializer = ClientSerializer(client)
        return Response(serializer.data)

    def put(self, request, client_id):
        client = Clients.objects.get(id=client_id)
        serializer = ClientSerializer(client, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, client_id, format=None):
        model_object = Clients.objects.get(id=client_id)
        model_object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProjectDetail(APIView):

    def get(self, request, format=None):
        project = Projects.objects.all().select_related('client', 'status')
        serializer = ProjectSerializer(project, many=True, context={"request": request})
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ProjectPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectByClient(APIView):

    def get(self, request, client_id, format=None):
        project = Projects.objects.filter(client__id=client_id).select_related('client', 'status')
        serializer = ProjectClientSerializer(project, many=True, context={"request": request})
        return Response(serializer.data)


class SequenceDetail(APIView):

    def get(self, request, format=None):
        sequence = Sequence.objects.select_related('project', 'project__client').all()
        serializer = SequenceSerializer(sequence, many=True, context={"request": request})
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = SequencePostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectUpdate(APIView):

    def get(self, request, projectId, format=None):
        project = Projects.objects.get(id=projectId)
        serializer = ProjectSerializer(project)
        return Response(serializer.data)

    def put(self, request, projectId):
        project = Projects.objects.get(id=projectId)
        serializer = ProjectSerializer(project, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, projectId, format=None):
        model_object = Projects.objects.get(id=projectId)
        model_object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ShotsData(APIView):

    def get(self, request, format=None):
        query_params = self.request.query_params

        if query_params:
            project_id = query_params.get('project_id', None)
            client_id = query_params.get('client_id', None)
            if project_id:
                shot = Shots.objects.select_related('sequence', 'task_type', 'sequence__project',
                                                    'sequence__project__client', 'status', 'complexity', 'team_lead',
                                                'artist', 'location').filter(sequence__project_id=project_id)
            elif client_id:
                shot = Shots.objects.select_related('sequence', 'task_type', 'sequence__project',
                                                'sequence__project__client', 'status', 'complexity', 'team_lead',
                                                'artist', 'location').filter(sequence__project__client_id=client_id)
            else:
                status_list = query_params.get('status', None)
                dept = query_params.get('dept', None)
                status = []
                if status_list is not None:
                    for stat in status_list.split('|'):
                        status.append(stat)
                if dept is not None:
                    shot = Shots.objects.select_related('sequence', 'task_type', 'sequence__project',
                                                        'sequence__project__client', 'status', 'complexity',
                                                        'team_lead', 'artist', 'location').filter(
                        status__code__in=status, task_type__name=dept)
                else:
                    shot = Shots.objects.select_related('sequence', 'task_type', 'sequence__project',
                                                        'sequence__project__client', 'status', 'complexity',
                                                        'team_lead', 'artist', 'location').filter(
                        status__code__in=status)
        else:
            shot = Shots.objects.select_related('sequence', 'task_type', 'sequence__project',
                                                'sequence__project__client', 'status', 'complexity', 'team_lead',
                                                'artist', 'location').all()

        serializer = ShotsSerializer(shot, many=True, context={"request": request})
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ShotsPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ShotsDataFilter(ListAPIView):

    def get(self, request, format=None):
        query_params = self.request.query_params
        argumentos = {}
        if query_params.get('client_id'):
            clients = []
            for client in query_params.get('client_id').split('|'):
                clients.append(client)
            argumentos['sequence__project__client_id__in'] = clients
        if query_params.get('project_id'):
            projects = []
            for project in query_params.get('project_id').split('|'):
                projects.append(project)
            argumentos['sequence__project_id__in'] = projects
        if query_params.get('status'):
            status = []
            for stat in query_params.get('status').split('|'):
                status.append(stat)
            argumentos['status_id__in'] = status
        if query_params.get('dept'):
            depts = []
            for dept in query_params.get('dept').split('|'):
                depts.append(dept)
            argumentos['task_type__name__in'] = depts
        if len(argumentos) > 0:
            shot = Shots.objects.select_related('sequence', 'task_type', 'sequence__project',
                                                'sequence__project__client', 'status', 'complexity',
                                                'team_lead', 'artist', 'location').filter(
                **argumentos)
        else:
            shot =[]
            # shot = Shots.objects.select_related('sequence', 'task_type', 'sequence__project',
            #                                     'sequence__project__client', 'status', 'complexity', 'team_lead',
            #                                     'artist', 'location').all()

        serializer = ShotsSerializer(shot, many=True, context={"request": request})
        return Response(serializer.data)

class ShotLogsData(APIView):

    def get(self, request, format=None):
        shotlogs = ShotLogs.objects.all()
        serializer = ShotLogsSerializer(shotlogs, many=True, context={"request": request})
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ShotLogsPostSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DayLogsData(APIView):

    def get(self, request, format=None):
        '''
        [::-1] reverse order
        [:2] last two records
        '''
        query_params = self.request.query_params
        if query_params:
            shot_id = query_params.get('shot_id', None)
            log_id = query_params.get('log_id', None)
            start_date = query_params.get('start_date', None)
            end_date = query_params.get('end_date', None)
            lead_id = query_params.get('lead_id', None)
            if shot_id:
                daylogs = DayLogs.objects.filter(shot_id=shot_id).select_related('shot', 'artist', 'updated_by')[::-1][
                          :2]
                serializer = DayLogsSerializer(daylogs, many=True, context={"request": request})
            elif log_id:
                daylogs = DayLogs.objects.get(id=log_id).select_related('shot','artist','updated_by', 'shot__sequence',
                                                                                                                       'shot__sequence__project','shot__status',
                                                                                                                       'shot__task_type', 'shot__location', 'shot__team_lead','shot__artist',
                                                                                                                       'shot__sequence__project__client', 'shot__sequence__project__client__locality')
                serializer = DayLogsSerializer(daylogs, context={"request": request})
            elif start_date is not None and end_date is not None and lead_id is not None:
                daylogs = DayLogs.objects.filter(updated_date__range=[start_date, end_date], shot__team_lead__profile_id = lead_id).select_related('shot','artist','updated_by', 'shot__sequence',
                                                                                                                        'shot__sequence__project', 'shot__status',
                                                                                                                       'shot__task_type', 'shot__location','shot__team_lead','shot__artist',
                                                                                                                       'shot__sequence__project__client', 'shot__sequence__project__client__locality')
                serializer = DayLogsSerializer(daylogs, many=True, context={"request": request})
        else:
            daylogs = DayLogs.objects.all().select_related('shot', 'artist', 'updated_by')
            serializer = DayLogsSerializer(daylogs, many=True, context={"request": request})

        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = DayLogsPostSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        query_params = self.request.query_params
        if query_params:
            log_id = query_params.get('log_id', None)
            if log_id:
                day_logs = DayLogs.objects.get(id=log_id)
                serializer = DayLogsSerializer(day_logs, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectShotsData(APIView):

    def get(self, request, sequenceId, format=None):
        shot = Shots.objects.select_related('sequence', 'sequence__project', 'sequence__project__client', 'status',
                                            'complexity').filter(sequence=sequenceId)
        serializer = ShotsSerializer(shot, many=True, context={"request": request})
        return Response(serializer.data)


class ProjectSequenceData(APIView):

    def get(self, request, projectId, format=None):
        sequence = Sequence.objects.filter(project=projectId)
        serializer = SequenceSerializer(sequence, many=True, context={"request": request})
        return Response(serializer.data)


class ShotUpdate(APIView):

    def get(self, request, shotId, format=None):
        shot = Shots.objects.select_related('sequence__project', 'sequence', 'sequence__project__client', 'status',
                                            'task_type', 'complexity').prefetch_related( 'status', 'complexity',
                                                                                        'sequence').get(id=shotId)
        serializer = ShotsSerializer(shot)
        return Response(serializer.data)

    def put(self, request, shotId):
        shot = Shots.objects.get(id=shotId)
        serializer = ShotsPostSerializer(shot, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            serializer = ShotsSerializer(shot)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, shotId, format=None):
        model_object = Shots.objects.get(id=shotId)
        model_object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MyTaskData(APIView):

    def get(self, request, format=None):
        mytask = MyTask.objects.select_related('shot__task_type', 'shot__sequence', 'shot__sequence__project', 'artist',
                                               'assigned_by', 'task_status').all()
        serializer = MyTaskSerializer(mytask, many=True, context={"request": request})
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = MyTaskPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # create_dir_permissions(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MyTaskShotData(APIView):

    def get(self, request, shotId, format=None):
        mytask = MyTask.objects.select_related('artist', 'assigned_by', 'task_status').filter(shot=shotId)
        serializer = MyTaskShotSerializer(mytask, many=True)
        return Response(serializer.data)


class MyTaskDetail(APIView):

    def get(self, request, taskId, format=None):
        task = MyTask.objects.select_related('artist', 'task_status', 'shot', 'assigned_by').get(id=taskId)
        serializer = MyTaskSerializer(task)
        return Response(serializer.data)

    def put(self, request, taskId):
        task = MyTask.objects.get(id=taskId)
        serializer = MyTaskUpdateSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()

            serializer = MyTaskStatusSerializer(task)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, shotId, format=None):
        model_object = Shots.objects.get(id=shotId)
        model_object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MyTaskArtistData(APIView):

    def get(self, request, artistid):
        print(artistid)
        mytask = MyTask.objects.select_related('assigned_by', 'shot', 'shot__task_type', 'shot__sequence__project',
                                               'shot__status', 'task_status', 'artist', 'shot__sequence',
                                               'shot__sequence__project__client').filter(artist=artistid).all()
        serializer = MyTaskArtistSerializer(mytask, many=True)
        return Response(serializer.data)


class ShotAssignment(APIView):

    def get(self, request, format=None):
        assignment = Assignments.objects.all()
        serializer = AssignmentSerializer(assignment, many=True, context={"request": request})
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = AssignmentPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LeadShotsData(APIView):

    def get(self, request, format=None):
        query_params = self.request.query_params
        if query_params:
            leadId = query_params.get('lead_id', None)
            status_list = query_params.get('status', None)
            start_date = query_params.get('start_date', None)
            end_date = query_params.get('end_date', None)
            status = []
            if status_list is not None:
                for stat in status_list.split('|'):
                    status.append(stat)
                if start_date is not None and end_date is not None:
                    lead = Assignments.objects.filter(lead_id=leadId, shot__status__code__in=status, assigned_date__range=[start_date, end_date
                                                                                                                        ]).select_related('lead',
                                                                                                                 'shot',
                                                                                                                 'shot__sequence',
                                                                                                                 'shot__sequence__project',
                                                                                                                 'shot__sequence__project__client',
                                                                                                                 'shot__status',
                                                                                                                 'shot__task_type',
                                                                                                                 'assigned_by',
                                                                                                                 'shot__artist',
                                                                                                                 'shot__team_lead')
                else:
                    lead = Assignments.objects.filter(lead=leadId, shot__status__code__in=status).select_related('lead', 'shot',
                                                                                                                 'shot__sequence',
                                                                                                                 'shot__sequence__project',
                                                                                                                 'shot__sequence__project__client',
                                                                                                                 'shot__status',
                                                                                                                 'shot__task_type',
                                                                                                                 'assigned_by',
                                                                                                                 'shot__artist',
                                                                                                                 'shot__team_lead')
            else:
                if start_date is not None and end_date is not None:
                    lead = Assignments.objects.filter(lead_id=leadId, assigned_date__range=[start_date, end_date]).select_related('lead',
                                                                                                                 'shot',
                                                                                                                 'shot__sequence',
                                                                                                                 'shot__sequence__project',
                                                                                                                 'shot__sequence__project__client',
                                                                                                                 'shot__status',
                                                                                                                 'shot__task_type',
                                                                                                                 'assigned_by',
                                                                                                                 'shot__artist',
                                                                                                                 'shot__team_lead')
        else:
            lead = Assignments.objects.select_related('lead', 'shot', 'shot__sequence', 'shot__sequence__project',
                                                      'shot__sequence__project__client', 'shot__status',
                                                      'shot__task_type', 'assigned_by', 'shot__team_lead',
                                                      'shot__artist')
        serializer = AssignmentSerializer(lead, many=True, context={"request": request})
        return Response(serializer.data)

class LeadsData(ListAPIView):
    def get(self, request, format=None):
        query_params = self.request.query_params
        argumentos = {}
        if query_params.get('client_id'):
            clients = []
            for client in query_params.get('client_id').split('|'):
                clients.append(client)
            argumentos['shot__sequence__project__client_id__in'] = clients
        if query_params.get('project_id'):
            projects = []
            for project in query_params.get('project_id').split('|'):
                projects.append(project)
            argumentos['shot__sequence__project_id__in'] = projects
        if query_params.get('status'):
            status = []
            for stat in query_params.get('status').split('|'):
                status.append(stat)
            argumentos['shot__status_id__in'] = status
        if query_params.get('dept'):
            depts = []
            for dept in query_params.get('dept').split('|'):
                depts.append(dept)
            argumentos['shot__task_type__name__in'] = depts
        if query_params.get('lead'):
            argumentos['lead_id'] = query_params.get('lead')
        if len(argumentos) > 0:
            lead_shot = Assignments.objects.select_related('lead',
                                                     'shot',
                                                     'shot__sequence',
                                                     'shot__sequence__project',
                                                     'shot__sequence__project__client',
                                                     'shot__status',
                                                     'shot__task_type',
                                                     'assigned_by',
                                                     'shot__artist',
                                                     'shot__team_lead').filter(**argumentos)
        else:
            lead_shot =[]
            # shot = Shots.objects.select_related('sequence', 'task_type', 'sequence__project',
            #                                     'sequence__project__client', 'status', 'complexity', 'team_lead',
            #                                     'artist', 'location').all()

        serializer = AssignmentSerializer(lead_shot, many=True, context={"request": request})
        return Response(serializer.data)

class ChannelsData(APIView):

    def get(self, request, shotId):
        data = Channels.objects.select_related('shot', 'sender').filter(shot=shotId)
        serializer = ChannelsSerializer(data, many=True, context={"request": request})
        return Response(serializer.data)


class ChannelsPostData(APIView):

    def get(self, request):
        data = Channels.objects.select_related('shot', 'sender').all()
        serializer = ChannelsSerializer(data, many=True, context={"request": request})
        return Response(serializer.data)

    def post(self, request):
        serializer = ChannelsPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GroupsData(APIView):

    def get(self, request, groupId):
        data = Groups.objects.get(name=groupId)
        serializer = GroupsSerializer(data, context={"request": request})
        return Response(serializer.data)


class GroupsPostData(APIView):

    def get(self, request):
        data = Groups.objects.all()
        serializer = GroupsSerializer(data, many=True, context={"request": request})
        return Response(serializer.data)

    def post(self, request):
        serializer = GroupsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QCData(APIView):

    def get(self, request):
        data = Qc_Assignment.objects.all()
        serializer = TeamQCSerializer(data, many=True, context={"request": request})
        return Response(serializer.data)

    def post(self, request):
        serializer = QCSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QCDataByTeamId(APIView):

    def get(self, request, teamId):
        data = Qc_Assignment.objects.select_related('task__shot__sequence__project',
                                                    'task__shot__sequence__project__client', 'task__shot__sequence',
                                                    'task__shot__task_type', 'task__shot__status', 'task__task_status',
                                                    'qc_status').filter(team=teamId)
        serializer = TeamQCSerializer(data, many=True, context={"request": request})
        return Response(serializer.data)


class QCDataById(APIView):

    def get(self, request, qcId):
        data = Qc_Assignment.objects.get(id=qcId)
        serializer = TeamQCSerializer(data, many=True, context={"request": request})
        return Response(serializer.data)

    def put(self, request, qcId):
        qc_task = Qc_Assignment.objects.get(id=qcId)
        serializer = TeamQCSerializer(qc_task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ShotVersionsAPI(APIView):

    def get(self, request):
        data = ShotVersions.objects.select_related('status').order_by('version')
        serializer = ShotVersionsSerializer(data, many=True, context={"request": request})
        return Response(serializer.data)

    def post(self, request):
        serializer = ShotVersionsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LastShotVersionById(APIView):

    def get(self, request, shotId):
        data = ShotVersions.objects.select_related('status').filter(shot=shotId).last()
        serializer = ShotVersionsSerializer(data, context={"request": request})
        return Response(serializer.data)


class ShotVersionsById(APIView):
    def get(self, request, verId):
        data = ShotVersions.objects.filter(shot=verId).select_related('sent_by', 'status')
        serializer = AllShotVersionsSerializer(data, many=True, context={"request": request})
        return Response(serializer.data)

    def put(self, request, verId):
        data = ShotVersions.objects.get(id=verId)
        serializer = ShotVersionsSerializer(data, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class QcVersionsAPI(APIView):

    def get(self, request):
        data = QCVersions.objects.select_related('status').order_by('version')
        serializer = QcVersionsSerializer(data, many=True, context={"request": request})
        return Response(serializer.data)

    def post(self, request):
        serializer = QcVersionsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LastQcVersionById(APIView):

    def get(self, request, shotId):
        data = QCVersions.objects.select_related('status').filter(shot=shotId).last()
        serializer = QcVersionsSerializer(data, context={"request": request})
        return Response(serializer.data)


class QcVersionsById(APIView):
    def get(self, request, verId):
        data = QCVersions.objects.filter(shot=verId).select_related('sent_by', 'status')
        serializer = AllShotQcVersionsSerializer(data, many=True, context={"request": request})
        return Response(serializer.data)

    def put(self, request, verId):
        data = QCVersions.objects.get(id=verId)
        serializer = QcVersionsSerializer(data, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ClientVersionsAPI(APIView):

    def get(self, request):
        data = ClientVersions.objects.select_related('shot','sent_by','verified_by','status').order_by('version')
        serializer = ClientVersionsSerializer(data, many=True, context={"request": request})
        return Response(serializer.data)

    def post(self, request):
        serializer = ClientVersionsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LastClientVersionById(APIView):

    def get(self, request, shotId):
        data = ClientVersions.objects.select_related('status').filter(shot=shotId).last()
        serializer = ClientVersionsSerializer(data, context={"request": request})
        return Response(serializer.data)


class ClientVersionsById(APIView):
    def get(self, request, verId):
        data = ClientVersions.objects.filter(shot=verId).select_related('sent_by', 'status')
        serializer = AllShotClientVersionsSerializer(data, many=True, context={"request": request})
        return Response(serializer.data)

    def put(self, request, verId):
        data = ClientVersions.objects.get(id=verId)
        serializer = ClientVersionsSerializer(data, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Perm_Groups(APIView):

    def get(self, request):
        data = Permission_Groups.objects.all()
        serializer = PGSerializer(data, many=True, context={"request": request})
        return Response(serializer.data)


# TaskHelp Main API
class TaskHelp_Main_API(APIView):

    def get(self, request):
        data = TaskHelp_Main.objects.select_related('shot', 'shot__sequence', 'task_type', 'requested_by',
                                                    'shot__sequence__project', 'shot__sequence__project__client',
                                                    'shot__status', 'shot__task_type', 'status').all()
        serializer = TaskHelpMainSerializer(data, many=True, context={"request": request})
        return Response(serializer.data)

    def post(self, request):
        serializer = TaskHelpMainPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskHelpMainUpdate(APIView):

    def get(self, request, parentId, format=None):
        taskhelp_main = TaskHelp_Main.objects.select_related('shot', 'shot__sequence__project', 'shot__sequence',
                                                             'sequence__project__client', 'status', 'task_type',
                                                             'complexity').prefetch_related('task', 'status',
                                                                                            'complexity',
                                                                                            'sequence').get(id=parentId)
        serializer = TaskHelpMainSerializer(taskhelp_main)
        return Response(serializer.data)

    def put(self, request, parentId):
        taskhelp_main = TaskHelp_Main.objects.get(id=parentId)
        serializer = TaskHelpMainPostSerializer(taskhelp_main, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            serializer = TaskHelpMainSerializer(taskhelp_main)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskHelp_Lead_API(APIView):

    def get(self, request):
        data = TaskHelp_Lead.objects.all()
        serializer = TaskHelpLeadSerializer(data, many=True, context={"request": request})
        return Response(serializer.data)

    def post(self, request):
        serializer = TaskHelpLeadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskHelp_Artist_API(APIView):

    def get(self, request):
        data = TaskHelp_Artist.objects.all()
        serializer = TaskHelpArtistSerializer(data, many=True, context={"request": request})
        return Response(serializer.data)

    def post(self, request):
        serializer = TaskHelpArtistPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskHelpArtistData(APIView):

    def get(self, request, artistId, format=None):
        mytask = TaskHelp_Artist.objects.select_related('assigned_by', 'shot__task_type', 'shot__sequence__project',
                                                        'shot__status', 'status', 'assigned_to', 'shot__sequence',
                                                        'shot__sequence__project__client').filter(
            assigned_to=artistId).all()
        serializer = TaskHelpArtistSerializer(mytask, many=True)
        return Response(serializer.data)


class TaskHelpArtistDetail(APIView):

    def get(self, request, taskId, format=None):
        task = TaskHelp_Artist.objects.select_related('assigned_to', 'status', 'shot', 'assigned_by').get(id=taskId)
        serializer = TaskHelpArtistSerializer(task)
        return Response(serializer.data)

    def put(self, request, taskId):
        task = TaskHelp_Artist.objects.get(id=taskId)
        serializer = TaskHelpArtistUpdateSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()

            serializer = TaskHelpArtistStatusSerializer(task)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TeamLeadReports(APIView):

    def get(self, request):
        query_params = self.request.query_params
        if query_params:
            lead_id = query_params.get('lead_id', None)
            start_date = query_params.get('start_date', None)
            end_date = query_params.get('end_date', None)
            if lead_id is not None and start_date is None:
                leadreports = TeamLead_Week_Reports.objects.filter(team_lead=lead_id)
                serializer = TeamReportSerializer(leadreports, many=True, context={"request": request})
            elif lead_id is not None and start_date is not None:
                reports = TeamLead_Week_Reports.objects.filter(team_lead=lead_id, from_date=start_date,
                                                               to_date=end_date)
                serializer = TeamReportSerializer(reports,many=True, context={"request": request})
        else:
            leadreports = TeamLead_Week_Reports.objects.all()
            serializer = TeamReportSerializer(leadreports, many=True, context={"request": request})
        return Response(serializer.data)

    def post(self, request):
        serializer = TeamReportSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        query_params = self.request.query_params
        pass
        # if query_params:
        #     log_id = query_params.get('log_id', None)
        #     if log_id:
        #         day_logs = DayLogs.objects.get(id=log_id)
        #         serializer = TeamReportSerializer(day_logs, data=request.data, partial=True)
        #         if serializer.is_valid():
        #             serializer.save()
        #             return Response(serializer.data, status=status.HTTP_201_CREATED)
        #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomLeadReports(APIView):

    def get(self, request):
        query_params = self.request.query_params
        if query_params:
            lead_id = query_params.get('lead_id', None)
            start_date = query_params.get('start_date', None)
            end_date = query_params.get('end_date', None)
            returned_data = calculate_data(lead_id, start_date, end_date)
        return Response(returned_data)

class CustomArtistReports(APIView):

    def get(self, request):
        query_params = self.request.query_params
        if query_params:
            artist_id = query_params.get('artist_id', None)
            start_date = query_params.get('start_date', None)
            end_date = query_params.get('end_date', None)
            returned_data = calculate_artist_data(artist_id, start_date, end_date)
        return Response(returned_data)

class CustomDeptReports(APIView):

    def get(self, request):
        query_params = self.request.query_params
        if query_params:
            dept = query_params.get('dept', None)
            start_date = query_params.get('start_date', None)
            end_date = query_params.get('end_date', None)
            returned_data = calculate_dept_data(dept, start_date, end_date)
        return Response(returned_data)

class CustomStudioReports(APIView):

    def get(self, request):
        query_params = self.request.query_params
        if query_params:
            start_date = query_params.get('start_date', None)
            end_date = query_params.get('end_date', None)
            returned_data = calculate_studio_data(start_date, end_date)
        return Response(returned_data)
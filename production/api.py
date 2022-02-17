import operator
import os

from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from hrm.models import Employee
from hrm.serializers import EmployeeSerializer
from production.models import Clients, Projects, ShotStatus, Shots, Complexity, Sequence, MyTask, Assignments, Channels, \
    Groups, Qc_Assignment, Folder_Permissions, Permission_Groups, ShotVersions, TaskHelp_Main, TaskHelp_Lead, \
    TaskHelp_Artist, ShotLogs, Locality
from production.serializers import ClientSerializer, ProjectSerializer, StatusSerializer, ShotsSerializer, \
    ShotsPostSerializer, ComplexitySerializer, SequenceSerializer, SequencePostSerializer, MyTaskSerializer, \
    MyTaskPostSerializer, MyTaskShotSerializer, AssignmentSerializer, AssignmentPostSerializer, MyTaskArtistSerializer, \
    ChannelsSerializer, ChannelsPostSerializer, GroupsSerializer, QCSerializer, TeamQCSerializer, \
    MyTaskUpdateSerializer, PGSerializer, ProjectClientSerializer, \
    ProjectPostSerializer, MyTaskStatusSerializer, ShotVersionsSerializer, AllShotVersionsSerializer, \
    TaskHelpMainSerializer, TaskHelpLeadSerializer, \
    TaskHelpArtistSerializer, TaskHelpMainPostSerializer, TaskHelpArtistPostSerializer, TaskHelpArtistUpdateSerializer, \
    TaskHelpArtistStatusSerializer, ShotLogsSerializer, ShotLogsPostSerializer, LocalitySerializer

import configparser

class StatusInfo(APIView):

    def get(self, request, format=None):
        status = ShotStatus.objects.all()
        serializer = StatusSerializer(status, many=True, context={"request":request} )
        return Response(serializer.data)

class LocalityInfo(APIView):

    def get(self, request, format=None):
        locality = Locality.objects.all()
        serializer = LocalitySerializer(locality, many=True, context={"request":request} )
        return Response(serializer.data)

class ComplexityInfo(APIView):

    def get(self, request, format=None):
        complexity = Complexity.objects.all()
        serializer = ComplexitySerializer(complexity, many=True, context={"request":request} )
        return Response(serializer.data)

class ClientDetail(APIView):

    def get(self, request, format=None):
        client = Clients.objects.all()
        serializer = ClientSerializer(client, many=True, context={"request":request} )
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
        project = Projects.objects.all().select_related('client','status')
        serializer = ProjectSerializer(project, many=True, context={"request":request})
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ProjectPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProjectByClient(APIView):

    def get(self, request,client_id, format=None):
        project = Projects.objects.filter(client__id=client_id).select_related('client','status')
        serializer = ProjectClientSerializer(project, many=True, context={"request":request})
        return Response(serializer.data)

class SequenceDetail(APIView):

    def get(self, request, format=None):
        sequence = Sequence.objects.select_related('project','project__client').all()
        serializer = SequenceSerializer(sequence, many=True, context={"request":request})
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
            if project_id:
                shot = Shots.objects.select_related('sequence', 'task_type', 'sequence__project', 'sequence__project__client', 'status', 'complexity', 'team_lead','artist', 'location').filter(sequence__project_id=project_id)
            else:
                status_list = query_params.get('status', None)
                dept = query_params.get('dept', None)
                status = []
                if status_list is not None:
                    for stat in status_list.split('|'):
                        status.append(stat)
                if dept is not None:
                    shot = Shots.objects.select_related('sequence','task_type','sequence__project','sequence__project__client', 'status', 'complexity', 'team_lead','artist','location').filter(status__code__in=status, task_type__name=dept)
                else:
                    shot = Shots.objects.select_related('sequence','task_type','sequence__project','sequence__project__client', 'status', 'complexity', 'team_lead','artist','location').filter(status__code__in=status)
        else:
            shot = Shots.objects.select_related('sequence', 'task_type', 'sequence__project',
                                                'sequence__project__client', 'status', 'complexity','team_lead','artist','location')

        serializer = ShotsSerializer(shot, many=True, context={"request":request})
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ShotsPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ShotLogsData(APIView):

    def get(self, request, format=None):
        shotlogs = ShotLogs.objects.all()
        serializer = ShotLogsSerializer(shotlogs, many=True, context={"request":request})
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ShotLogsPostSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProjectShotsData(APIView):

    def get(self, request, sequenceId, format=None):
        shot = Shots.objects.select_related('sequence','sequence__project','sequence__project__client','status','complexity').filter(sequence=sequenceId)
        serializer = ShotsSerializer(shot, many=True, context={"request":request})
        return Response(serializer.data)

class ProjectSequenceData(APIView):

    def get(self, request, projectId, format=None):
        sequence = Sequence.objects.filter(project=projectId)
        serializer = SequenceSerializer(sequence, many=True, context={"request":request})
        return Response(serializer.data)

class ShotUpdate(APIView):

    def get(self, request, shotId, format=None):
        shot = Shots.objects.select_related('sequence__project','sequence','sequence__project__client','status','task_type','complexity').prefetch_related('task','status','complexity','sequence').get(id=shotId)
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
        mytask = MyTask.objects.select_related('shot__task_type','shot__sequence','shot__sequence__project','artist','assigned_by','task_status').all()
        serializer = MyTaskSerializer(mytask, many=True, context={"request":request})
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = MyTaskPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # create_dir_permissions(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MyTaskShotData(APIView):

    def get(self, request,shotId, format=None):
        mytask = MyTask.objects.select_related('artist','assigned_by','task_status').filter(shot=shotId)
        serializer = MyTaskShotSerializer(mytask, many=True)
        return Response(serializer.data)

class MyTaskDetail(APIView):

    def get(self, request, taskId, format=None):
        task = MyTask.objects.select_related('artist','task_status','shot','assigned_by').get(id=taskId)
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

    def get(self, request,artistId, format=None):
        mytask = MyTask.objects.select_related('assigned_by','shot','shot__task_type','shot__sequence__project','shot__status','task_status','artist','shot__sequence','shot__sequence__project__client').filter(artist=artistId).all()
        serializer = MyTaskArtistSerializer(mytask, many=True)
        return Response(serializer.data)

class ShotAssignment(APIView):

    def get(self, request, format=None):
        assignment = Assignments.objects.all()
        serializer = AssignmentSerializer(assignment, many=True, context={"request":request})
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
            status = []
            if status_list is not None:
                for stat in status_list.split('|'):
                    status.append(stat)
            lead = Assignments.objects.filter(lead=leadId, shot__status__code__in=status).select_related('lead', 'shot', 'shot__sequence', 'shot__sequence__project', 'shot__sequence__project__client', 'shot__status', 'shot__task_type', 'assigned_by', 'shot__artist','shot__team_lead')
        else:
            lead = Assignments.objects.select_related('lead', 'shot', 'shot__sequence', 'shot__sequence__project', 'shot__sequence__project__client', 'shot__status', 'shot__task_type', 'assigned_by','shot__team_lead','shot__artist')
        serializer = AssignmentSerializer(lead, many=True, context={"request":request})
        return Response(serializer.data)

class ChannelsData(APIView):

    def get(self, request, shotId):
        data = Channels.objects.select_related('shot','sender').filter(shot=shotId)
        serializer = ChannelsSerializer(data, many=True, context={"request": request})
        return Response(serializer.data)

class ChannelsPostData(APIView):

    def get(self, request):
        data = Channels.objects.select_related('shot','sender').all()
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
        serializer = TeamQCSerializer(data, many=True,context={"request": request})
        return Response(serializer.data)

    def post(self, request):
        serializer = QCSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class QCDataByTeamId(APIView):

    def get(self, request,teamId):
        data = Qc_Assignment.objects.select_related('task__shot__sequence__project','task__shot__sequence__project__client','task__shot__sequence','task__shot__task_type','task__shot__status','task__task_status','qc_status').filter(team=teamId)
        serializer = TeamQCSerializer(data, many=True, context={"request": request})
        return Response(serializer.data)

class QCDataById(APIView):

    def get(self, request,qcId):
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
        return  Response(serializer.data)

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
        return  Response(serializer.data)

class ShotVersionsById(APIView):
    def get(self, request, verId):
        data = ShotVersions.objects.filter(shot=verId).select_related('sent_by','status')
        serializer = AllShotVersionsSerializer(data, many=True, context={"request": request})
        return Response(serializer.data)

    def put(self, request, verId):
        data = ShotVersions.objects.get(id=verId)
        serializer = ShotVersionsSerializer(data, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Perm_Groups(APIView):

    def get(self, request):
        data = Permission_Groups.objects.all()
        serializer = PGSerializer(data, many=True, context={"request": request})
        return Response(serializer.data)

#TaskHelp Main API
class TaskHelp_Main_API(APIView):

    def get(self, request):
        data = TaskHelp_Main.objects.select_related('shot','shot__sequence','task_type','requested_by','shot__sequence__project','shot__sequence__project__client','shot__status','shot__task_type','status').all()
        serializer = TaskHelpMainSerializer(data, many=True, context={"request": request})
        return  Response(serializer.data)

    def post(self, request):
        serializer = TaskHelpMainPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskHelpMainUpdate(APIView):

    def get(self, request, parentId, format=None):
        taskhelp_main = TaskHelp_Main.objects.select_related('shot','shot__sequence__project','shot__sequence','sequence__project__client','status','task_type','complexity').prefetch_related('task','status','complexity','sequence').get(id=parentId)
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
        return  Response(serializer.data)

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
        return  Response(serializer.data)

    def post(self, request):
        serializer = TaskHelpArtistPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskHelpArtistData(APIView):

    def get(self, request,artistId, format=None):
        mytask = TaskHelp_Artist.objects.select_related('assigned_by','shot__task_type','shot__sequence__project','shot__status','status','assigned_to','shot__sequence','shot__sequence__project__client').filter(assigned_to=artistId).all()
        serializer = TaskHelpArtistSerializer(mytask, many=True)
        return Response(serializer.data)

class TaskHelpArtistDetail(APIView):

    def get(self, request, taskId, format=None):
        task = TaskHelp_Artist.objects.select_related('assigned_to','status','shot','assigned_by').get(id=taskId)
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
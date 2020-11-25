from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from production.models import Clients, Projects, ShotStatus, Shots, Complexity, Sequence, MyTask, Assignments, Channels, \
    Groups, Qc_Assignment, HeadQc_Assignment, Folder_Permissions, Permission_Groups, HeadQCTeam
from production.serializers import ClientSerializer, ProjectSerializer, StatusSerializer, ShotsSerializer, \
    ShotsPostSerializer, ComplexitySerializer, SequenceSerializer, SequencePostSerializer, MyTaskSerializer, \
    MyTaskPostSerializer, MyTaskShotSerializer, AssignmentSerializer, AssignmentPostSerializer, MyTaskArtistSerializer, \
    ChannelsSerializer, ChannelsPostSerializer, GroupsSerializer, QCSerializer, TeamQCSerializer, \
    MyTaskUpdateSerializer, HeadQCSerializer, HQCSerializer, PGSerializer, HQTSerializer

class StatusInfo(APIView):
    """
    This is for getting the Status info
    """

    def get(self, request, format=None):
        status = ShotStatus.objects.all()
        serializer = StatusSerializer(status, many=True, context={"request":request} )
        return Response(serializer.data)

class ComplexityInfo(APIView):
    """
    This is for getting the Complexity info
    """

    def get(self, request, format=None):
        complexity = Complexity.objects.all()
        serializer = ComplexitySerializer(complexity, many=True, context={"request":request} )
        return Response(serializer.data)

class ClientDetail(APIView):
    """
    This is for get and post client detail
    """

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
    """
    This is for edit employee detail
    """

    def get(self, request, format=None):
        project = Projects.objects.all()
        serializer = ProjectSerializer(project, many=True, context={"request":request})
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SequenceDetail(APIView):
    """
    This is for get and post sequence detail
    """

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
    """
    This is for edit employee detail
    """
    def get(self, request, format=None):
        shot = Shots.objects.select_related('sequence','task_type','sequence__project','sequence__project__client','status','complexity').all()
        serializer = ShotsSerializer(shot, many=True, context={"request":request})
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ShotsPostSerializer(data=request.data)
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
        shot = Shots.objects.get(id=shotId)
        serializer = ShotsSerializer(shot)
        return Response(serializer.data)

    def put(self, request, shotId):
        shot = Shots.objects.get(id=shotId)
        serializer = ShotsPostSerializer(shot, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, shotId, format=None):
        model_object = Shots.objects.get(id=shotId)
        model_object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class MyTaskData(APIView):
    """
    This is for edit employee detail
    """
    def get(self, request, format=None):
        mytask = MyTask.objects.all()
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
    """
    This is for edit employee detail
    """
    def get(self, request,shotId, format=None):
        mytask = MyTask.objects.all().filter(shot=shotId)
        serializer = MyTaskShotSerializer(mytask, many=True)
        return Response(serializer.data)

class MyTaskDetail(APIView):

    def get(self, request, taskId, format=None):
        task = MyTask.objects.get(id=taskId)
        serializer = MyTaskSerializer(task)
        return Response(serializer.data)

    def put(self, request, taskId):
        task = MyTask.objects.get(id=taskId)
        serializer = MyTaskUpdateSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, shotId, format=None):
        model_object = Shots.objects.get(id=shotId)
        model_object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class MyTaskArtistData(APIView):
    """
    This is for edit employee detail
    """
    def get(self, request,artistId, format=None):
        mytask = MyTask.objects.filter(artist=artistId).all()
        serializer = MyTaskArtistSerializer(mytask, many=True)
        return Response(serializer.data)

class ShotAssignment(APIView):
    """
    This is for edit employee detail
    """
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

    def get(self, request, leadId, format=None):
        lead = Assignments.objects.filter(lead=leadId)
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

class Head_QC_Team(APIView):

    def get(self, request):
        data = HeadQCTeam.objects.all()
        serializer = HQTSerializer(data, many=True, context={"request": request})
        return Response(serializer.data)

class HeadQCData(APIView):

    def get(self, request):
        data = HeadQc_Assignment.objects.all()
        serializer = HQCSerializer(data, many=True,context={"request": request})
        return Response(serializer.data)

    def post(self, request):
        serializer = HQCSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class HeadQCDataById(APIView):

    def get(self, request,hqcId):
        print("Head Qc:",hqcId)
        data = HeadQc_Assignment.objects.get(id=hqcId)
        serializer = HeadQCSerializer(data, context={"request": request})
        return Response(serializer.data)

    def put(self, request, hqcId):
        hqc_task = HeadQc_Assignment.objects.get(id=hqcId)
        serializer = HeadQCSerializer(hqc_task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class QCDataByHQCId(APIView):

    def get(self, request,hqcId):
        data = HeadQc_Assignment.objects.select_related('qc_task__task__shot__sequence__project','qc_task__task__shot__sequence__project__client','qc_task__task__shot__sequence','qc_task__task__shot__task_type','qc_task__task__shot__status','qc_task__task__task_status','hqc_status').filter(hqc__hqc__id=hqcId)
        serializer = HeadQCSerializer(data, many=True, context={"request": request})
        return Response(serializer.data)

class Perm_Groups(APIView):

    def get(self, request):
        data = Permission_Groups.objects.all()
        serializer = PGSerializer(data, many=True,context={"request": request})
        return Response(serializer.data)
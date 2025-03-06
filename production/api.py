#  Copyright (c) 2023.
#  Designed & Developed by Narendar Reddy G, OscarFX Private Limited
#  All rights reserved.

import datetime, json
import logging
from csv import excel_tab
from itertools import groupby
from operator import itemgetter
from django.http import Http404
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination

from history.models import historyMaping, ClientsHistory, ProjectsHistory, SequenceHistory, ShotsHistory, \
    AssignmentsHistory, MyTaskHistory, DayLogsHistory, TaskDayLogsHistory
from OFX_API import  apiRequestManager
from rest_framework import status, generics
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from hrm.models import Employee
from ofx_statistics.models import EmployeeDailyStatistics
from ofx_statistics.serializers import EmployeeDailyStatisticserializer
from production.models import Clients, Projects, ShotStatus, Shots, Complexity, Sequence, MyTask, Assignments, Channels, \
    Groups, Qc_Assignment, Permission_Groups, ShotVersions, TaskHelp_Main, TaskHelp_Lead, \
    TaskHelp_Artist, ShotLogs, Locality, DayLogs, TeamLead_Week_Reports, QCVersions, ClientVersions, TimeLogs, \
    TaskDayLogs, Elements, Task_Type, EstimationId
from production.pagination import OFXPagination
from production.reports.custom_artist_id_report import calculate_artist_id_data
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
    ClientVersionsSerializer, AllShotClientVersionsSerializer, TimeLogsSerializer, TimeLogsPostSerializer, \
    TimeCardSerializer, LightDataSerializer, ShotTimeLogSerializer, ShotTimeCardSerializer, TaskDayLogsSerializer, \
    TaskDayLogsPostSerializer, ElementsSerializer, TaskDayLogsPUTSerializer, Task_TypeSerializer, EstimationSerializer


class EstimationData(APIView):
    """
    API to fetch data from Shots model and store it in the EstimationId model.
    """

    def post(self, request, format=None):
        # Calculate the time window for recent shots (e.g., last 24 hours)
        last_processed_time = timezone.now() - timedelta(days=1)

        # Filter Shots to only include those created or modified after the last processed time
        recent_shots = Shots.objects.filter(modified_date__gte=last_processed_time)

        estimation_data = []

        for shot in recent_shots:
            if not shot.estimate_id:
                # Skip shots without an estimate_id
                continue

            # Fetch client from related models, e.g., through sequence
            client = None
            if shot.sequence and shot.sequence.project:
                client = shot.sequence.project.client  # Adjust to match your model structure

            # Check if an EstimationId with the same estimationId already exists
            if EstimationId.objects.filter(estimationId=shot.estimate_id).exists():
                # Skip duplicates
                continue

            # Create EstimationId object
            estimation_obj = EstimationId(
                estimationId=shot.estimate_id,
                client=client,  # Assign client
                zohoId=" ",
                status="NOT SENT"
            )
            estimation_obj.save()
            estimation_data.append(estimation_obj)

        # Serialize and return response
        serializer = EstimationSerializer(estimation_data, many=True, context={"request": request})

        response_data = {
            "message": "Estimation data refreshed successfully.",
            "data": serializer.data
        }

        return Response(response_data, status=status.HTTP_200_OK)

class Estimation(APIView):
    def get(self, request, format=None):
        pk_id = request.query_params.get('pk_id', None)
        zoho_id = request.query_params.get('zohoId', None)

        estimation = EstimationId.objects.all()

        if pk_id:
            estimation = estimation.filter(estimationId__icontains=pk_id)
        if zoho_id:
            estimation = estimation.filter(zohoId=zoho_id)
        serializer = EstimationSerializer(estimation, many=True, context={"request": request})
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = EstimationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Update an existing estimation
    def put(self, request, format=None):
        query_params = self.request.query_params
        estimation_id = query_params.get("pk_id", None)

        if not estimation_id:
            return Response({"error": "pk_id query parameter is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            estimation = EstimationId.objects.get(estimationId=estimation_id)
        except EstimationId.DoesNotExist:
            raise Http404(f"Estimation with estimationId {estimation_id} does not exist.")

        serializer = EstimationSerializer(estimation, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Delete an estimation
    def delete(self, request, format=None):
        query_params = self.request.query_params
        pk_id = query_params.get("pk_id", None)
        if pk_id:
            estimation = EstimationId.objects.get(pk=pk_id)
            estimation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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

class TaskTypeInfo(APIView):

    def get(self, request, format=None):
        complexity = Task_Type.objects.all()
        serializer = Task_TypeSerializer(complexity, many=True, context={"request": request})
        return Response(serializer.data)

class TypeInfo(APIView):

    def get(self, request, format=None):
        choices = []
        choice_dict = dict(Shots.Types)

        for k, v in choice_dict.items():
            value = {'key': k, 'name': v}
            choices.append(value)
        return Response(choices, status=status.HTTP_200_OK)

class ClientDetail(APIView, apiRequestManager):
    def get(self, request, format=None):
        query_params = self.request.query_params
        logging.error("Quering:{query_params}")
        if query_params:
            locality = query_params.get('locality', None)
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
            _cdata = json.loads(json.dumps(serializer.data))
            self.createHistoryLog(model=ClientsHistory, targetModel=Clients, parentModel=None, parentField=None, query={'pk': _cdata['id']}, data={'name': _cdata['name']}, request=request, requestType='POST', defaultMsgMap=historyMaping['ClientsHistory']['POST'], customizedMsgMap={}, employeeModel=Employee)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ClientUpdate(APIView, apiRequestManager):

    def get(self, request, client_id, format=None):
        '''
        Pass the clientid to update the client
        '''
        client = Clients.objects.get(pk=client_id)
        serializer = ClientSerializer(client)
        return Response(serializer.data)

    def put(self, request, client_id):
        client = Clients.objects.get(pk=client_id)
        self.prepareHistoryLog(model=ClientsHistory,targetModel=Clients,parentField=None,query={'pk':client_id},data=request.data,request=request,requestType='PUT',defaultMsgMap=historyMaping['ClientsHistory']['PUT'],customizedMsgMap={})
        serializer = ClientSerializer(client, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            self.createHistoryLog(model=ClientsHistory,targetModel=Clients,parentModel=None,parentField=None,query={'pk':client_id},data=request.data,request=request,requestType='PUT',defaultMsgMap=historyMaping['ClientsHistory']['PUT'],customizedMsgMap={},employeeModel=Employee)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, client_id, format=None):
        model_object = Clients.objects.get(pk=client_id)
        _bojName = str(model_object.name)
        self.prepareHistoryLog(model=ClientsHistory,targetModel=Clients,parentField=None,query={'pk':client_id},data={'name':_bojName},request=request,requestType='DELETE',defaultMsgMap=historyMaping['ClientsHistory']['DELETE'],customizedMsgMap={})
        if model_object.delete():
            self.createHistoryLog(model=ClientsHistory,targetModel=Clients,parentModel=None,parentField=None,query={'pk':client_id},data={'name':_bojName},request=request,requestType='DELETE',defaultMsgMap=historyMaping['ClientsHistory']['DELETE'],customizedMsgMap={},employeeModel=Employee)
        return Response(status=status.HTTP_204_NO_CONTENT)

class ProjectDetail(APIView, apiRequestManager):

    def get(self, request, format=None):
        query_params = self.request.query_params
        if query_params:
            status = query_params.get('status', "ARCHIVED")
        else:
            status = "ARCHIVED"
        if query_params.get('client'):
            clients = query_params.get('client')
            if clients:
                clients_list = clients.split(',')
            project = Projects.objects.filter(client__name__in=clients_list).select_related('client', 'org_status').exclude(status=status)
        else:
            project = Projects.objects.all().select_related('client', 'org_status').exclude(status=status)
        serializer = ProjectSerializer(project, many=True, context={"request": request})
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ProjectPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            _pdata = json.loads(json.dumps(serializer.data))
            self.createHistoryLog(model=ProjectsHistory, targetModel=Projects, parentModel=Clients, parentField='client', query={'pk': _pdata['id']}, data={'name': _pdata['name']}, request=request,requestType='POST', defaultMsgMap=historyMaping['ProjectsHistory']['POST'],customizedMsgMap={}, employeeModel=Employee)
            return Response(_pdata, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProjectByClient(APIView):

    def get(self, request, client_id, format=None):
        project = Projects.objects.filter(client__pk=client_id).select_related('client', 'org_status').exclude(
            status="ARCHIVED")
        serializer = ProjectClientSerializer(project, many=True, context={"request": request})
        return Response(serializer.data)

class SequenceDetail(APIView, apiRequestManager):

    def get(self, request, format=None):
        sequence = Sequence.objects.select_related('project', 'project__client').all()
        serializer = SequenceSerializer(sequence, many=True, context={"request": request})
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = SequencePostSerializer(data=request.data)
        if serializer.is_valid():
           serializer.save()
           _sqdata = json.loads(json.dumps(serializer.data))
           self.createHistoryLog(model=SequenceHistory, targetModel=Sequence, parentModel=Projects,parentField='project', query={'pk': _sqdata['id']}, data={'name': _sqdata['name']}, request=request, requestType='POST', defaultMsgMap=historyMaping['SequenceHistory']['POST'], customizedMsgMap={}, employeeModel=Employee)
           return Response(_sqdata, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProjectUpdate(APIView, apiRequestManager):

    def get(self, request, projectId, format=None):
        project = Projects.objects.get(pk=projectId)
        serializer = ProjectSerializer(project)
        return Response(serializer.data)

    def put(self, request, projectId):
        project = Projects.objects.get(pk=projectId)
        self.prepareHistoryLog(model=ProjectsHistory,targetModel=Projects,parentField=None,query={'pk':projectId},data=request.data,request=request,requestType='PUT',defaultMsgMap=historyMaping['ProjectsHistory']['PUT'],customizedMsgMap={})
        serializer = ProjectSerializer(project, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            self.createHistoryLog(model=ProjectsHistory, targetModel=Projects, parentModel=Clients,parentField='client', query={'pk': projectId}, data=request.data, request=request, requestType='PUT', defaultMsgMap=historyMaping['ProjectsHistory']['PUT'],customizedMsgMap={}, employeeModel=Employee)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, projectId, format=None):
        model_object = Projects.objects.get(pk=projectId)
        prjectname = str(model_object.name)
        self.prepareHistoryLog(model=ProjectsHistory, targetModel=Projects, parentField=None, query={'pk': projectId}, data={'name': prjectname}, request=request, requestType='DELETE',defaultMsgMap=historyMaping['ProjectsHistory']['DELETE'], customizedMsgMap={})
        model_object.delete()
        self.createHistoryLog(model=ProjectsHistory, targetModel=Projects, parentModel=Clients, parentField='client', query={'pk': projectId}, data={'name': prjectname}, request=request, requestType='DELETE', defaultMsgMap=historyMaping['ProjectsHistory']['DELETE'],customizedMsgMap={}, employeeModel=Employee)
        return Response(status=status.HTTP_204_NO_CONTENT)

class ShotsData(APIView, apiRequestManager):
    """
    The ShotsData class is a subclass of APIView and apiRequestManager. It handles the GET and POST requests for retrieving and creating Shot objects.

    Attributes:
        None

    Methods:
        - get(self, request, format=None):
            This method handles the GET request to retrieve Shots objects based on the provided query parameters. It returns a Response object with serialized Shot data.

            Parameters:
                - request: The HTTP request object.
                - format (optional): The data format requested (e.g. JSON, XML).

        - post(self, request, format=None):
            This method handles the POST request to create a new Shot object. It saves the serialized data, creates a history log, and returns a Response object with the created Shot data
    *.

            Parameters:
                - request: The HTTP request object.
                - format (optional): The data format requested (e.g. JSON, XML).

    """
    def get(self, request, format=None):
        query_params = self.request.query_params

        if query_params:
            project_id = query_params.get('project_id', None)
            client_id = query_params.get('client_id', None)
            estimate_id = query_params.get('estimate_id', None)

            if project_id:
                shot = Shots.objects.select_related('sequence', 'task_type', 'sequence__project',
                                                    'sequence__project__client', 'status', 'complexity', 'team_lead',
                                                    'artist', 'location', 'sequence__project__client__locality','supervisor','hod').filter(
                    sequence__project__pk=project_id)
            elif client_id:
                shot = Shots.objects.select_related('sequence', 'task_type', 'sequence__project',
                                                    'sequence__project__client', 'status', 'complexity', 'team_lead',
                                                    'artist', 'location', 'sequence__project__client__locality','supervisor','hod').filter(
                    sequence__project__client__pk=client_id).exclude(sequence__project__status="ARCHIVED")

            elif estimate_id:
                shot = Shots.objects.select_related(
                     'sequence__project',
                     'status'
                ).filter(estimate_id=estimate_id).exclude(sequence__project__status="ARCHIVED")

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
                                                        'team_lead', 'artist', 'location',
                                                        'sequence__project__client__locality','supervisor','hod').filter(
                        status__code__in=status, task_type__name=dept).exclude(sequence__project__status="ARCHIVED")
                else:
                    shot = Shots.objects.select_related('sequence', 'task_type', 'sequence__project',
                                                        'sequence__project__client', 'status', 'complexity',
                                                        'team_lead', 'artist', 'location',
                                                        'sequence__project__client__locality','supervisor','hod').filter(
                        status__code__in=status).exclude(sequence__project__status="ARCHIVED")
        else:
            shot = Shots.objects.select_related('sequence', 'task_type', 'sequence__project',
                                                'sequence__project__client', 'status', 'complexity', 'team_lead',
                                                'artist', 'location',
                                                'sequence__project__client__locality','supervisor','hod').all().exclude(
                sequence__project__status="ARCHIVED")

        serializer = ShotsSerializer(shot, many=True, context={"request": request})
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ShotsPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            _shotdata = json.loads(json.dumps(serializer.data))
            self.createHistoryLog(model=ShotsHistory, targetModel=Shots, parentModel=Sequence, parentField='sequence', query={'pk': _shotdata['id']}, data={'name': _shotdata['name']}, request=request, requestType='POST', defaultMsgMap=historyMaping['ShotsHistory']['POST'], customizedMsgMap={}, employeeModel=Employee)
            return Response(_shotdata, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductSheet(APIView):
    """
    Class: ProductSheet

    This class is used to generate a product sheet based on the given query parameters. It retrieves data from the Shots model and prepares the data to be serialized using the ShotTimeLog
    *Serializer. The final product sheet data is returned as a response.

    Methods:
    - get(request, format=None): This method handles the HTTP GET request and generates the product sheet based on the query parameters provided. It retrieves the query parameters, processes
    * them, filters the Shots model accordingly, and calculates the total spent time for each shot. The product sheet data is then returned as a Response.

    Usage:
    1. Create an instance of the ProductSheet class.
    2. Make a GET request to the instance to generate the product sheet.

    Example:
    product_sheet = ProductSheet()
    response = product_sheet.get(request)

    Params:
    - request: The HTTP GET request object.
    - format (optional): The format in which the product sheet data should be returned. Defaults to None.

    Returns:
    - shots_data: The product sheet data in the form of a Response object.

    Note: The example code and author details should not be included in the documentation.
    """

    def get(self, request, format=None):
        query_params = self.request.query_params
        argumentos = {}
        if query_params.get('shot_id'):
            argumentos['pk'] = query_params.get('shot_id')

        if query_params.get('client_id'):
            clients = []
            for client in query_params.get('client_id').split('|'):
                clients.append(client)
            argumentos['sequence__project__client__pk__in'] = clients
        if query_params.get('project_id'):
            projects = []
            for project in query_params.get('project_id').split('|'):
                projects.append(project)
            argumentos['sequence__project__pk__in'] = projects
        if query_params.get('status'):
            status = []
            for stat in query_params.get('status').split('|'):
                status.append(stat)
            argumentos['status__code__in'] = status
        if query_params.get('dept'):
            depts = []
            for dept in query_params.get('dept').split('|'):
                depts.append(dept)
            argumentos['task_type__name__in'] = depts
        if query_params.get('shot_ids'):
            shot_ids = []
            for shot_id in query_params.get('shot_ids').split('|'):
                shot_ids.append(shot_id)
            argumentos['pk__in'] = shot_ids

        if query_params.get('isSubShot'):
            argumentos['isSubShot'] = query_params.get('isSubShot')

        if query_params.get('isSplitShot'):
            argumentos['isSplitShot'] = query_params.get('isSplitShot')

            queryset = Shots.objects.prefetch_related('timelogs', 'artists', 'artists__role', 'artists__department',
                                                      'artists__role__permissions').select_related('sequence',
                                                                                                   'task_type',
                                                                                                   'sequence__project',
                                                                                                   'sequence__project__client',
                                                                                                   'status',
                                                                                                   'complexity',
                                                                                                   'team_lead',
                                                                                                   'artist', 'location',
                                                                                                   'sequence__project__client__locality',
                                                                                                   'status__status_segregation',
                                                                                                   'supervisor',
                                                                                                   'hod').filter(
                **argumentos)
        elif len(argumentos) > 0:
            queryset = Shots.objects.prefetch_related('timelogs', 'artists', 'artists__role', 'artists__department',
                                                      'artists__role__permissions',
                                                      'artist__role__permissions').select_related('sequence',
                                                                                                  'task_type',
                                                                                                  'sequence__project',
                                                                                                  'sequence__project__client',
                                                                                                  'status',
                                                                                                  'complexity',
                                                                                                  'team_lead', 'artist',
                                                                                                  'location',
                                                                                                  'artist__role',
                                                                                                  'artist__department',
                                                                                                  'sequence__project__client__locality',
                                                                                                  'status__status_segregation',
                                                                                                  'supervisor',
                                                                                                  'hod').filter(
                **argumentos).exclude(sequence__project__status="ARCHIVED")
        else:
            # queryset = Shots.objects.all()
            queryset = Shots.objects.prefetch_related('timelogs', 'artists', 'artists__role', 'artists__department',
                                                      'artists__role__permissions').select_related('sequence',
                                                                                                   'task_type',
                                                                                                   'sequence__project',
                                                                                                   'sequence__project__client',
                                                                                                   'status',
                                                                                                   'complexity',
                                                                                                   'team_lead',
                                                                                                   'artist', 'location',
                                                                                                   'artist__role',
                                                                                                   'team_lead__role',
                                                                                                   'sequence__project__client__locality',
                                                                                                   'status__status_segregation',
                                                                                                   'supervisor',
                                                                                                   'hod').all().exclude(
                sequence__project__status="ARCHIVED")

        serializer = ShotTimeLogSerializer(instance=queryset, many=True)
        shots_data = []
        for _shotdata in serializer.data:
            total_spent = 0
            for spent in _shotdata['timelogs']:
                total_spent += spent['spent_hours']
            _tim = {
                'total_spent': total_spent / 8
            }
            _shotdata.update(_tim)
            shots_data.append(_shotdata)

        return Response(shots_data)

class ShotsApi(APIView):
    def get(self, request, format=None):
        query_params = self.request.query_params
        argumentos = {}
        order_fields = ['id']

        if query_params.get('shot_id'):
            argumentos['pk'] = query_params.get('shot_id')
        # Handle search query
        search_query = self.request.query_params.get('search', None)
        if query_params.get('search'):
            argumentos['name__icontains'] = query_params.get('search')
        if query_params.get('client_id'):
            clients = []
            for client in query_params.get('client_id').split('|'):
                clients.append(client)
            argumentos['sequence__project__client__pk__in'] = clients
        if query_params.get('client'):
            clients = query_params.get('client')
            if clients:
                clients_list = clients.split(',')
                argumentos['sequence__project__client__name__in'] = clients_list
        if query_params.get('project'):
            projects = query_params.get('project')
            if projects:
                projects_list = projects.split(',')
                argumentos['sequence__project__name__in'] = projects_list
        if query_params.get('project_id'):
            projects = []
            for project in query_params.get('project_id').split('|'):
                projects.append(project)
            argumentos['sequence__project__pk__in'] = projects
        if query_params.get('status'):
            status_codes = query_params.get('status')
            if status_codes:
                # Split the string into a list of values
                status_code_list = status_codes.split(',')
                argumentos['status__code__in'] = status_code_list
        if query_params.get('task type'):
            task_types = query_params.get('task type')
            if task_types:
                # Split the string into a list of values
                task_type_list = task_types.split(',')
                argumentos['task_type__name__in'] = task_type_list
        if query_params.get('type'):
            types = query_params.get('type')
            if types:
                # Split the string into a list of values
                type_list = types.split(',')
                argumentos['type__in'] = type_list
        if query_params.get('complexity'):
            complexity = query_params.get('complexity')
            if complexity:
                # Split the string into a list of values
                complexity_list = complexity.split(',')
                argumentos['complexity__name__in'] = complexity_list
        if query_params.get('location'):
            location = query_params.get('location')
            if location:
                # Split the string into a list of values
                location_list = location.split(',')
                argumentos['location__name__in'] = location_list

        if query_params.get('supervisor'):
            supervisor = query_params.get('supervisor')
            if supervisor:
                supervisor_list = supervisor.split(',')
                print("Supervisor data:", supervisor_list)
                argumentos['supervisor__fullName__in'] = supervisor_list

        if query_params.get('team lead'):
            team_lead = query_params.get('team lead')
            if team_lead:
                teamlead_list = team_lead.split(',')
                argumentos['team_lead__fullName__in'] = teamlead_list

        if query_params.get('captain'):
            captain = query_params.get('captain')
            if captain:
                captain_list = captain.split(',')
                argumentos['artist__fullName__in'] = captain_list

        if query_params.get('dept'):
            depts = []
            for dept in query_params.get('dept').split('|'):
                depts.append(dept)
            argumentos['task_type__name__in'] = depts
        if query_params.get('shot_ids'):
            shot_ids = []
            for shot_id in query_params.get('shot_ids').split('|'):
                shot_ids.append(shot_id)
            argumentos['pk__in'] = shot_ids

        if query_params.get('isSubShot'):
            argumentos['isSubShot'] = query_params.get('isSubShot')

        if query_params.get('isSplitShot'):
            argumentos['isSplitShot'] = query_params.get('isSplitShot')

            queryset = Shots.objects.prefetch_related('timelogs','artists','artists__role','artists__department','artists__role__permissions').select_related('sequence', 'task_type',
                                                                                 'sequence__project',
                                                                                 'sequence__project__client', 'status',
                                                                                 'complexity',
                                                                                 'team_lead', 'artist', 'location',
                                                                                 'sequence__project__client__locality','status__status_segregation','supervisor','hod').filter(**argumentos)
        elif len(argumentos) > 0:
            queryset = Shots.objects.prefetch_related('timelogs','artists','artists__role','artists__department','artists__role__permissions','artist__role__permissions').select_related('sequence', 'task_type',
                                                                                 'sequence__project',
                                                                                 'sequence__project__client', 'status',
                                                                                 'complexity',
                                                                                 'team_lead', 'artist', 'location','artist__role','artist__department',
                                                                                 'sequence__project__client__locality','status__status_segregation','supervisor','hod').filter(
                **argumentos).order_by(*order_fields).exclude(sequence__project__status="ARCHIVED")
        else:
            # queryset = Shots.objects.all()
            queryset = Shots.objects.prefetch_related('timelogs','artists','artists__role','artists__department','artists__role__permissions').select_related('sequence', 'task_type',
                                                                                 'sequence__project',
                                                                                 'sequence__project__client', 'status',
                                                                                 'complexity', 'team_lead',
                                                                                 'artist', 'location','artist__role','team_lead__role',
                                                                                 'sequence__project__client__locality','status__status_segregation','supervisor','hod').all().order_by(*order_fields).exclude(
                sequence__project__status="ARCHIVED")
        paginator = OFXPagination()
        draw = query_params.get('draw',None)
        paginator.page_size = query_params.get('page_size',25)
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = ShotTimeLogSerializer(instance=result_page, many=True)
        # serializer = ShotTimeLogSerializer(instance=queryset, many=True)
        shots_data = []
        for _shotdata in serializer.data:
            total_spent = 0
            for spent in _shotdata['timelogs']:
                total_spent += spent['spent_hours']
            _tim = {
                'total_spent': total_spent / 8
            }
            _shotdata.update(_tim)
            shots_data.append(_shotdata)

        return paginator.get_paginated_response(draw,shots_data)
        # return Response(shots_data)

    def get_queryset(self):
        queryset = super().get_queryset()

        # Get ordering information from the DataTables parameters
        ordering = self.request.GET.get('ordering', None)

        if ordering:
            # Split the ordering string and apply to the queryset
            ordering_params = ordering.split(',')
            queryset = queryset.order_by(*ordering_params)
        return queryset

class ShotsDataFilter(APIView):

    def get(self, request, format=None):
        query_params = self.request.query_params
        from_date = query_params.get('eta_from_date', None)
        to_date = query_params.get('eta_to_date', None)
        argumentos = {}
        if query_params.get('client_id'):
            clients = []
            for client in query_params.get('client_id').split('|'):
                clients.append(client)
            argumentos['sequence__project__client__pk__in'] = clients
        if query_params.get('project_id'):
            projects = []
            for project in query_params.get('project_id').split('|'):
                projects.append(project)
            argumentos['sequence__project__pk__in'] = projects
        if query_params.get('status'):
            status = []
            for stat in query_params.get('status').split('|'):
                status.append(stat)
            argumentos['status__pk__in'] = status
        if query_params.get('dept'):
            depts = []
            for dept in query_params.get('dept').split('|'):
                depts.append(dept)
            argumentos['task_type__name__in'] = depts
        if from_date is not None and to_date is not None:
            argumentos['eta__range'] = [from_date, to_date]
        if len(argumentos) > 0:
            shot = Shots.objects.select_related('sequence', 'task_type', 'sequence__project',
                                                'sequence__project__client', 'status', 'complexity',
                                                'team_lead', 'artist', 'location',
                                                'sequence__project__client__locality','supervisor','hod').filter(
                **argumentos).all().exclude(sequence__project__status="ARCHIVED")
        else:
            shot = []
            # shot = Shots.objects.select_related('sequence', 'task_type', 'sequence__project',
            #                                     'sequence__project__client', 'status', 'complexity', 'team_lead',
            #                                     'artist', 'location').all()

        serializer = ShotsSerializer(shot, many=True, context={"request": request})
        return Response(serializer.data)

class ShotLogsData(APIView):

    def get(self, request, format=None):
        shotlogs = ShotLogs.objects.all().exclude(sequence__project__status="ARCHIVED")
        serializer = ShotLogsSerializer(shotlogs, many=True, context={"request": request})
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ShotLogsPostSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DayLogsData(APIView, apiRequestManager):

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
                daylogs = DayLogs.objects.filter(shot__pk=shot_id).select_related('shot', 'artist', 'updated_by')[::-1][
                          :2]
                serializer = DayLogsSerializer(daylogs, many=True, context={"request": request})
            elif log_id:
                daylogs = DayLogs.objects.get(pk=log_id).select_related('shot', 'artist', 'updated_by',
                                                                        'shot__sequence',
                                                                        'shot__sequence__project', 'shot__status',
                                                                        'shot__task_type', 'shot__location',
                                                                        'shot__team_lead', 'shot__artist',
                                                                        'shot__sequence__project__client',
                                                                        'shot__sequence__project__client__locality')
                serializer = DayLogsSerializer(daylogs, context={"request": request})
            elif start_date is not None and end_date is not None and lead_id is not None:
                daylogs = DayLogs.objects.filter(updated_date__range=[start_date, end_date],
                                                 shot__team_lead__profile_id=lead_id).select_related('shot', 'artist',
                                                                                                     'updated_by',
                                                                                                     'shot__sequence',
                                                                                                     'shot__sequence__project',
                                                                                                     'shot__status',
                                                                                                     'shot__task_type',
                                                                                                     'shot__location',
                                                                                                     'shot__team_lead',
                                                                                                     'shot__artist',
                                                                                                     'shot__sequence__project__client',
                                                                                                     'shot__sequence__project__client__locality')
                serializer = DayLogsSerializer(daylogs, many=True, context={"request": request})
        else:
            daylogs = DayLogs.objects.all().select_related('shot', 'artist', 'updated_by')
            serializer = DayLogsSerializer(daylogs, many=True, context={"request": request})

        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = DayLogsPostSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            _daylogData = json.loads(json.dumps(serializer.data))
            self.createHistoryLog(model=DayLogsHistory, targetModel=DayLogs, parentModel=Shots, parentField='shot',query={'id': _daylogData['id']}, data={'shot':_daylogData['shot']}, request=request,requestType='POST', defaultMsgMap=historyMaping['DayLogsHistory']['POST'],customizedMsgMap={}, employeeModel=Employee)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        query_params = self.request.query_params
        if query_params:
            log_id = query_params.get('log_id', None)
            if log_id:
                day_logs = DayLogs.objects.get(pk=log_id)
                serializer = DayLogsSerializer(day_logs, data=request.data, partial=True)
                self.prepareHistoryLog(model=DayLogsHistory, targetModel=DayLogs, parentField='shot', query={"id": log_id},data=request.data, request=request, requestType='PUT', defaultMsgMap=historyMaping['DayLogsHistory']['PUT'],customizedMsgMap={})
                if serializer.is_valid():
                    serializer.save()
                    self.createHistoryLog(model=DayLogsHistory, targetModel=DayLogs, parentModel=Shots, parentField='shot', query={"id": log_id}, data=request.data, request=request, requestType='PUT', defaultMsgMap=historyMaping['DayLogsHistory']['PUT'], customizedMsgMap={}, employeeModel=Employee)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskDayLogsData(APIView, apiRequestManager):

    def get(self, request, format=None):
        '''
        [::-1] reverse order
        [:2] last two records
        '''
        query_params = self.request.query_params
        if query_params:
            task_id = query_params.get('task_id', None)
            log_id = query_params.get('log_id', None)
            start_date = query_params.get('start_date', None)
            end_date = query_params.get('end_date', None)
            lead_id = query_params.get('lead_id', None)
            if task_id:
                taskdaylogs = TaskDayLogs.objects.filter(task__pk=task_id).select_related('task', 'artist',
                                                                                          'updated_by')[::-1][
                              :2]
                serializer = TaskDayLogsSerializer(taskdaylogs, many=True, context={"request": request})
            elif log_id:
                taskdaylogs = TaskDayLogs.objects.get(pk=log_id)
                serializer = TaskDayLogsSerializer(taskdaylogs, context={"request": request})
            elif start_date is not None and end_date is not None and lead_id is not None:
                taskdaylogs = TaskDayLogs.objects.filter(updated_date__range=[start_date, end_date],
                                                         task__shot__team_lead__profile_id=lead_id).select_related(
                    'task', 'artist', 'updated_by', 'task__shot__sequence',
                    'task__shot__sequence__project', 'task__shot__status',
                    'task__shot__task_type', 'task__shot__location', 'task__shot__team_lead', 'task__shot__artist',
                    'task__shot__sequence__project__client', 'task__shot__sequence__project__client__locality')
                serializer = TaskDayLogsSerializer(taskdaylogs, many=True, context={"request": request})
        else:
            taskdaylogs = TaskDayLogs.objects.select_related('task', 'artist', 'updated_by').all()
            serializer = TaskDayLogsSerializer(taskdaylogs, many=True, context={"request": request})

        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = TaskDayLogsPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            _daytasklogData = json.loads(json.dumps(serializer.data))
            self.createHistoryLog(model=TaskDayLogsHistory, targetModel=TaskDayLogs, parentModel=MyTask, parentField='task', query={'id': _daytasklogData['id']}, data={'artist': _daytasklogData['artist']}, request=request, requestType='POST', defaultMsgMap=historyMaping['TaskDayLogsHistory']['POST'],customizedMsgMap={}, employeeModel=Employee)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        query_params = self.request.query_params
        if query_params:
            log_id = query_params.get('log_id', None)
            if log_id:
                task_day_logs = TaskDayLogs.objects.get(pk=log_id)
                serializer = TaskDayLogsPUTSerializer(task_day_logs, data=request.data, partial=True)
                self.prepareHistoryLog(model=TaskDayLogsHistory, targetModel=TaskDayLogs, parentField='task', query={'pk': log_id}, data=request.data, request=request, requestType='PUT', defaultMsgMap=historyMaping['TaskDayLogsHistory']['PUT'], customizedMsgMap={})
                if serializer.is_valid():
                    serializer.save()
                    self.createHistoryLog(model=TaskDayLogsHistory, targetModel=TaskDayLogs, parentModel=MyTask, parentField='task',query={'pk': log_id}, data=request.data, request=request, requestType='PUT', defaultMsgMap=historyMaping['TaskDayLogsHistory']['PUT'], customizedMsgMap={}, employeeModel=Employee)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskdaylogsFilter(APIView):
    def get(self, request, format=None):
        query_params = self.request.query_params
        argumentos = {}
        if query_params:
            if query_params.get('artist_id'):
                argumentos['task__artist__id'] = query_params.get('artist_id')
            if query_params.get('from_date') and query_params.get('to_date'):
                argumentos['updated_date__range'] = [query_params.get('from_date'), query_params.get('to_date')]
        task = TaskDayLogs.objects.select_related('updated_by','artist', 'task').filter(**argumentos)
        if query_params.get('artist_id'):
            serializer = TaskDayLogsSerializer(task, many=True, context={"request": request})
        else:
            serializer = TaskDayLogsSerializer(task, many=True, context={"request": request})
        return Response(serializer.data)

class TimeLogsData(APIView, apiRequestManager):

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
                daylogs = DayLogs.objects.filter(shot__pk=shot_id).select_related('shot', 'approved_by', 'updated_by')[
                          ::-1][
                          :2]
                serializer = DayLogsSerializer(daylogs, many=True, context={"request": request})
            elif log_id:
                daylogs = DayLogs.objects.get(pk=log_id)
                serializer = DayLogsSerializer(daylogs, context={"request": request})
            elif start_date is not None and end_date is not None and lead_id is not None:
                daylogs = DayLogs.objects.filter(updated_date__range=[start_date, end_date],
                                                 shot__team_lead__profile_id=lead_id).select_related('shot', 'artist',
                                                                                                     'updated_by',
                                                                                                     'shot__sequence',
                                                                                                     'shot__sequence__project',
                                                                                                     'shot__status',
                                                                                                     'shot__task_type',
                                                                                                     'shot__location',
                                                                                                     'shot__team_lead',
                                                                                                     'shot__artist',
                                                                                                     'shot__sequence__project__client',
                                                                                                     'shot__sequence__project__client__locality')
                serializer = DayLogsSerializer(daylogs, many=True, context={"request": request})
        else:
            timelogs = TimeLogs.objects.all().select_related('shot', 'approved_by', 'updated_by')
            serializer = TimeLogsSerializer(timelogs, many=True, context={"request": request})

        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = TimeLogsPostSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            _daylogData = json.loads(json.dumps(serializer.data))
            return Response(_daylogData, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        query_params = self.request.query_params
        if query_params:
            log_id = query_params.get('log_id', None)
            if log_id:
                day_logs = DayLogs.objects.get(pk=log_id)
                serializer = DayLogsSerializer(day_logs, data=request.data, partial=True)
                self.prepareHistoryLog(model=DayLogsHistory, targetModel=DayLogs, parentField='shot',query={'pk': log_id}, data=request.data, request=request, requestType='PUT', defaultMsgMap=historyMaping['DayLogsHistory']['PUT'], customizedMsgMap={})
                if serializer.is_valid():
                    serializer.save()
                    _daylogData = json.loads(json.dumps(serializer.data))
                    self.createHistoryLog(model=DayLogsHistory, targetModel=DayLogs, parentModel=Shots, parentField='shot', query={'pk': _daylogData['shot']['id']}, data=request.data, request=request, requestType='PUT', defaultMsgMap=historyMaping['DayLogsHistory']['PUT'], customizedMsgMap={}, employeeModel=Employee)
                    return Response(_daylogData, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TimeCardData(APIView):

    def get(self, request, format=None):
        '''
        [::-1] reverse order
        [:2] last two records
        '''

        timelogs = TimeLogs.objects.all().select_related('shot', 'approved_by', 'updated_by')
        serializer = TimeCardSerializer(timelogs, many=True, context={"request": request})
        grouper = itemgetter("updated_by", "creation_date")
        result = []
        for key, grp in groupby(sorted(serializer.data, key=grouper), grouper):
            temp_dict = dict(zip(["updated_by", "creation_date"], key))
            temp_dict["total_hours"] = 0
            Approved = True
            for item in grp:
                temp_dict["total_hours"] += item["total_hours"]
                if item['approved'] and Approved:
                    Approved = True
                else:
                    Approved = False

            temp_dict['approved'] = Approved

            result.append(temp_dict)

        return Response(result)

    def put(self, request):
        _data = request.data
        _date = datetime.datetime.strptime(_data['date'], '%d-%m-%Y').date()
        filter_data = TimeLogs.objects.filter(updated_by=_data['employee_id'], creation_date__gte=_date)
        serializer = TimeCardSerializer(filter_data, many=True, context={"request": request})
        for _dat in serializer.data:
            approve_data = {
                'approved': True
            }
            timelog = TimeLogs.objects.get(pk=_dat['id'])
            _serializer = TimeCardSerializer(timelog, data=approve_data, partial=True)
            if _serializer.is_valid():
                _serializer.save()
        return Response(status=status.HTTP_201_CREATED)

class ShotTimeCardData(APIView):

    def get(self, request, shotId):
        '''
        [::-1] reverse order
        [:2] last two records
        '''

        timelogs = TimeLogs.objects.all().select_related('shot', 'approved_by', 'updated_by').filter(shot=shotId)
        serializer = ShotTimeCardSerializer(timelogs, many=True, context={"request": request})
        return Response(serializer.data)

class UpdateTimeCard(APIView):

    def get(self, request, format=None):
        '''
        [::-1] reverse order
        [:2] last two records
        '''

        timelogs = TimeLogs.objects.all().select_related('shot', 'approved_by', 'updated_by')
        serializer = TimeCardSerializer(timelogs, many=True, context={"request": request})
        grouper = itemgetter("updated_by", "creation_date")
        result = []
        for key, grp in groupby(sorted(serializer.data, key=grouper), grouper):
            temp_dict = dict(zip(["updated_by", "creation_date"], key))
            temp_dict["total_hours"] = 0
            Approved = True
            for item in grp:
                temp_dict["total_hours"] += item["total_hours"]
                if item['approved'] and Approved:
                    Approved = True
                else:
                    Approved = False

            temp_dict['approved'] = Approved

            result.append(temp_dict)

        return Response(result)

    def put(self, request, taskId):
        timelog = TimeLogs.objects.get(pk=taskId)
        serializer = TimeCardSerializer(timelog, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LightBoxData(APIView):
    def get(self, request):
        query_params = self.request.query_params
        _employee_id = query_params.get('employee_id', None)
        _creation_date = query_params.get('_date', None)
        _date = datetime.datetime.strptime(_creation_date, '%d-%m-%Y').date()
        filter_data = TimeLogs.objects.filter(updated_by=_employee_id, creation_date__date=_date)
        serializer = LightDataSerializer(filter_data, many=True, context={"request": request})
        return Response(serializer.data)

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

class ShotUpdate(APIView,apiRequestManager):

    def get(self, request, shotId, format=None):
        shot = Shots.objects.select_related('sequence__project', 'sequence', 'sequence__project__client', 'status',
                                            'task_type', 'complexity').prefetch_related('status', 'complexity',
                                                                                        'sequence').get(pk=shotId)
        serializer = ShotsSerializer(shot)
        return Response(serializer.data)

    def put(self, request, shotId):
        shot = Shots.objects.get(pk=shotId)
        self.prepareHistoryLog(model=ShotsHistory, targetModel=Shots, parentField='sequence', query={'pk': shotId},data=request.data, request=request, requestType='PUT',defaultMsgMap=historyMaping['ShotsHistory']['PUT'], customizedMsgMap={})
        serializer = ShotsPostSerializer(shot, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            self.createHistoryLog(model=ShotsHistory, targetModel=Shots, parentModel=Sequence, parentField='sequence', query={'pk': shotId}, data=request.data, request=request, requestType='PUT', defaultMsgMap=historyMaping['ShotsHistory']['PUT'], customizedMsgMap={}, employeeModel=Employee)
            if request.data.get('bid_days',None) is not None:
                usedBids = float(request.data['bid_days'])
                allSubShots = self.getDBData(model=Shots, queryFilter={'parentShot__id':shotId},queryPerams=['id','bid_days'])
                for x in allSubShots:
                    usedBids = usedBids + float(x['bid_days'])
                self.update(query={'id': shotId}, model=Shots, data={'actual_bid_days':usedBids})
                shot = Shots.objects.get(pk=shotId)
            serializer = ShotsSerializer(shot)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, shotId, format=None):
        model_object = Shots.objects.get(pk=shotId)
        _shotdata = str(model_object.name)
        self.prepareHistoryLog(model=ShotsHistory, targetModel=Shots, parentField='sequence', query={'pk': shotId}, data={'name': _shotdata}, request=request, requestType='DELETE', defaultMsgMap=historyMaping['ShotsHistory']['DELETE'], customizedMsgMap={})
        model_object.delete()
        self.createHistoryLog(model=ShotsHistory, targetModel=Shots, parentModel=Sequence, parentField='sequence', query={'pk': shotId}, data={'name': _shotdata},request=request, requestType='DELETE',  defaultMsgMap=historyMaping['ShotsHistory']['DELETE'], customizedMsgMap={}, employeeModel=Employee)
        return Response(status=status.HTTP_204_NO_CONTENT)

class MyTaskData(APIView, apiRequestManager):

    def get(self, request, format=None):
        mytask = MyTask.objects.select_related('shot__task_type', 'shot__sequence', 'shot__sequence__project', 'artist',
                                               'assigned_by', 'task_status').all()
        serializer = MyTaskSerializer(mytask, many=True, context={"request": request})
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = MyTaskPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            _mytaskdata = json.loads(json.dumps(serializer.data))
            self.createHistoryLog(model=MyTaskHistory, targetModel=MyTask, parentModel=Shots, parentField='shot',query={'pk': _mytaskdata['id']}, data={'artist': _mytaskdata['artist']}, request=request, requestType='POST',defaultMsgMap=historyMaping['MyTaskHistory']['POST'], customizedMsgMap={},employeeModel=Employee)
            return Response(_mytaskdata, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MyTaskShotData(APIView):

    def get(self, request, shotId, format=None):
        mytask = MyTask.objects.select_related('artist', 'assigned_by', 'task_status').filter(shot=shotId)
        serializer = MyTaskShotSerializer(mytask, many=True)
        return Response(serializer.data)

class MyTaskDetail(APIView, apiRequestManager):
    """

    Class MyTaskDetail

    This class is responsible for handling HTTP requests for a specific task in the MyTask model.

    Methods:
    - get(request, taskId, format=None): Retrieves the details of a specific task.
    - put(request, taskId): Updates the details of a specific task.
    - delete(request, taskId, format=None): Deletes a specific task.

    Attributes:
    - APIView: Inherits the APIView class to handle HTTP requests.
    - apiRequestManager: Inherits the apiRequestManager class.

    Example usage:
    task_detail = MyTaskDetail()
    task_detail.get(request, taskId)
    task_detail.put(request, taskId)
    task_detail.delete(request, taskId)
    """
    def get(self, request, taskId, format=None):
        task = MyTask.objects.get(pk=taskId)
        serializer = MyTaskSerializer(task)
        return Response(serializer.data)

    def put(self, request, taskId):
        task = MyTask.objects.get(pk=taskId)
        serializer = MyTaskUpdateSerializer(task, data=request.data, partial=True)
        self.prepareHistoryLog(model=MyTaskHistory, targetModel=MyTask, parentField=Shots, query={'pk': taskId},data=request.data, request=request, requestType='PUT', defaultMsgMap=historyMaping['MyTaskHistory']['PUT'], customizedMsgMap={})
        if serializer.is_valid():
            serializer.save()
            serializer = MyTaskStatusSerializer(task)
            self.createHistoryLog(model=MyTaskHistory, targetModel=MyTask, parentModel=Shots, parentField='shot',query={'pk': taskId}, data=request.data, request=request, requestType='PUT',defaultMsgMap=historyMaping['MyTaskHistory']['PUT'], customizedMsgMap={},employeeModel=Employee)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, taskId, format=None):
        model_object = MyTask.objects.get(pk=taskId)
        self.prepareHistoryLog(model=MyTaskHistory, targetModel=MyTask, parentField=Shots, query={'pk': taskId}, data={'artist':True}, request=request, requestType='DELETE',defaultMsgMap=historyMaping['MyTaskHistory']['DELETE'], customizedMsgMap={})
        model_object.delete()
        self.createHistoryLog(model=MyTaskHistory, targetModel=MyTask, parentModel=Shots, parentField='shot',query={'pk': taskId}, data={'artist':True}, request=request, requestType='DELETE',defaultMsgMap=historyMaping['MyTaskHistory']['DELETE'], customizedMsgMap={},employeeModel=Employee)
        return Response(status=status.HTTP_204_NO_CONTENT)

class MyTaskArtistData(APIView):
    """
    This class is a subclass of the APIView class from the Django REST Framework. It handles GET requests to retrieve task data for a given artist.

    Methods:
    --------------------------------------------------------------------
    get(request, artistid)
        Handles GET requests to retrieve task data for a given artist.

        Parameters:
            request (HttpRequest): The HTTP request object.
            artistid (int): The ID of the artist.

        Returns:
            A Response object containing serialized task data.
    --------------------------------------------------------------------
    """
    def get(self, request, artistid):
        query_params = self.request.query_params
        argumentos = {
            "artist": artistid
            }
        if query_params.get('project_id'):
            projects = []
            for project in query_params.get('project_id').split('|'):
                projects.append(project)
            argumentos['shot__sequence__project__pk__in'] = projects

        if query_params.get('status'):
            status = []
            for project in query_params.get('status').split('|'):
                status.append(project)
            argumentos['task_status__code__in'] = status

        mytask = MyTask.objects.prefetch_related('shot__artists', 'artist__employee_groups').select_related('assigned_by', 'shot', 'shot__task_type', 'shot__sequence__project',
                                               'shot__status', 'task_status', 'artist', 'shot__sequence',
                                               'shot__sequence__project__client__locality', 'shot__artist__location', 'artist__location', 'shot__team_lead__location','shot__complexity','shot__location','assigned_by__location').filter(**argumentos)
        serializer = MyTaskArtistSerializer(mytask, many=True)
        return Response(serializer.data)

class ShotAssignment(APIView, apiRequestManager):
    """
    Class representing the API endpoint for shot assignments.

    This class inherits from the APIView class and the apiRequestManager class.

    ...

    Methods
    -------
    get(request, format=None)
        Retrieves all shot assignments.

    post(request, format=None)
        Creates new shot assignments.

    Attributes
    ----------
    None
    """
    def get(self, request, format=None):
        """
        Retrieves a list of all assignments.

        Parameters:
            request (Request): The HTTP request object.
            format (str, optional): The format of the response. Defaults to None.

        Returns:
            Response: The HTTP response object containing a list of assignment objects serialized in the AssignmentSerializer format.
        """
        assignment = Assignments.objects.select_related('lead', 'shot', 'assigned_by', 'shot__sequence',
                                                        'shot__sequence__project', 'shot__sequence__project__client',
                                                        'shot__sequence__project__client__locality', 'shot__status',
                                                        'shot__task_type', 'shot__complexity',
                                                        'assigned_by__department', 'shot__artist',
                                                        'shot__team_lead__location', 'shot__artist__location',
                                                        'lead__location', 'assigned_by__location',
                                                        'shot__location').all()
        serializer = AssignmentSerializer(assignment, many=True, context={"request": request})
        return Response(serializer.data)

    def post(self, request, format=None):

        serializer = AssignmentPostSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            _Assdata = json.loads(json.dumps(list(serializer.data)))
            for x in _Assdata:
                self.createHistoryLog(model=AssignmentsHistory, targetModel=Assignments, parentModel=Shots, parentField='shot',query={'pk': x['id']}, data={'lead': x['lead']}, request=request, requestType='POST', defaultMsgMap=historyMaping['AssignmentsHistory']['POST'],customizedMsgMap={},employeeModel=Employee)
            return Response(_Assdata, status=status.HTTP_201_CREATED)
        else:
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
                    lead = Assignments.objects.filter(lead__pk=leadId, shot__status__code__in=status,
                                                      assigned_date__range=[start_date, end_date
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
                    lead = Assignments.objects.filter(lead=leadId, shot__status__code__in=status).select_related('lead',
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
                if start_date is not None and end_date is not None:
                    lead = Assignments.objects.filter(lead__pk=leadId,
                                                      assigned_date__range=[start_date, end_date]).select_related(
                        'lead',
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
        if query_params.get('id'):
            argumentos['pk'] = query_params.get('id')

        if query_params.get('client_id'):
            clients = []
            for client in query_params.get('client_id').split('|'):
                clients.append(client)
            argumentos['shot__sequence__project__client__pk__in'] = clients

        if query_params.get('client'):
            clients = query_params.get('client')
            if clients:
                clients_list = clients.split(',')
                argumentos['sequence__project__client__name__in'] = clients_list
        if query_params.get('project_id'):
            projects = []
            for project in query_params.get('project_id').split('|'):
                projects.append(project)
            argumentos['shot__sequence__project__pk__in'] = projects
        if query_params.get('status_codes'):
            status_codes = query_params.get('status_codes')
            if status_codes:
                # Split the string into a list of values
                status_code_list = status_codes.split(',')
                argumentos['shot__status__code__in'] = status_code_list
            # status_codes = []
            # for stat in query_params.get('status_codes').split(','):
            #     status_codes.append(stat)
            # argumentos['shot__status__code__in'] = status_codes

        if query_params.get('status'):
            status = []
            for stat in query_params.get('status').split('|'):
                status.append(stat)
            argumentos['shot__status__pk__in'] = status

        if query_params.get('dept'):
            depts = []
            for dept in query_params.get('dept').split('|'):
                depts.append(dept)
            argumentos['shot__task_type__name__in'] = depts
        if query_params.get('lead'):
            argumentos['lead__id'] = query_params.get('lead')

        if len(argumentos) > 0:


            lead_shot = Assignments.objects.select_related('lead',
                                                           'shot',
                                                           'shot__sequence',
                                                           'shot__sequence__project',
                                                           'shot__sequence__project__client',
                                                           'shot__status',
                                                           'shot__status__status_segregation',
                                                           'shot__task_type',
                                                           'assigned_by',
                                                           'shot__artist',
                                                           'shot__team_lead').filter(**argumentos).exclude(
                shot__sequence__project__status="ARCHIVED")

        else:
            lead_shot = []
        paginator = OFXPagination()
        draw = query_params.get('draw', None)
        paginator.page_size = query_params.get('page_size', 25)
        result_page = paginator.paginate_queryset(lead_shot, request)
        serializer = AssignmentSerializer(instance=result_page, many=True, context={"request": request})
        # return Response(serializer.data)

        return paginator.get_paginated_response(draw, serializer.data)

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
        data = Qc_Assignment.objects.get(pk=qcId)
        serializer = TeamQCSerializer(data, many=True, context={"request": request})
        return Response(serializer.data)

    def put(self, request, qcId):
        qc_task = Qc_Assignment.objects.get(pk=qcId)
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
        data = ShotVersions.objects.get(pk=verId)
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
        data = QCVersions.objects.get(pk=verId)
        serializer = QcVersionsSerializer(data, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ClientVersionsAPI(APIView):

    def get(self, request):
        query_params = self.request.query_params
        argumentos = {}
        if query_params:
            if query_params.get('from_date') and query_params.get('to_date'):
                argumentos['sent_date__range'] = [query_params.get('from_date'), query_params.get('to_date')]
            data = ClientVersions.objects.select_related('shot', 'sent_by', 'verified_by', 'status').order_by('version').filter(**argumentos)
        else:
            data = ClientVersions.objects.select_related('shot', 'sent_by', 'verified_by', 'status').order_by('version')
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
        data = ClientVersions.objects.get(pk=verId)
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
                                                                                            'sequence').get(pk=parentId)
        serializer = TaskHelpMainSerializer(taskhelp_main)
        return Response(serializer.data)

    def put(self, request, parentId):
        taskhelp_main = TaskHelp_Main.objects.get(pk=parentId)
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
        task = TaskHelp_Artist.objects.select_related('assigned_to', 'status', 'shot', 'assigned_by').get(pk=taskId)
        serializer = TaskHelpArtistSerializer(task)
        return Response(serializer.data)

    def put(self, request, taskId):
        task = TaskHelp_Artist.objects.get(pk=taskId)
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
                serializer = TeamReportSerializer(reports, many=True, context={"request": request})
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
        #         day_logs = DayLogs.objects.get(pk=log_id)
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
            dept = query_params.get('dept', None)
            if artist_id:
                returned_data = calculate_artist_data(artist__pk=artist_id, start_date=start_date, end_date=end_date)
            elif dept:
                returned_data = calculate_artist_data(dept=dept, start_date=start_date, end_date=end_date)
            else:
                returned_data = calculate_artist_data(start_date=start_date, end_date=end_date)
        return Response(returned_data)

class CustomArtistIdReports(APIView):

    def get(self, request):
        query_params = self.request.query_params
        returned_data = ""
        if query_params:
            artist_id = query_params.get('artist_id', None)
            start_date = query_params.get('start_date', None)
            end_date = query_params.get('end_date', None)
            dept = query_params.get('dept', None)
            returned_data = ""
            if artist_id:
                returned_data = calculate_artist_id_data(artist__pk=artist_id, start_date=start_date, end_date=end_date)
            elif dept:
                returned_data = calculate_artist_id_data(dept=dept, start_date=start_date, end_date=end_date)
            else:
                returned_data = calculate_artist_id_data(start_date=start_date, end_date=end_date)
        # print(returned_data)
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

class StatusCount(APIView):

    def get(self, request):
        query_params = self.request.query_params
        argumentos = {}
        if query_params.get('client_id'):
            clients = []
            for client in query_params.get('client_id').split('|'):
                clients.append(client)
            argumentos['sequence__project__client__pk__in'] = clients
        if query_params.get('project_id'):
            projects = []
            for project in query_params.get('project_id').split('|'):
                projects.append(project)
            argumentos['sequence__project__pk__in'] = projects
        if len(argumentos) > 0:
            yts_count = Shots.objects.select_related('sequence', 'task_type', 'sequence__project',
                                                     'sequence__project__client', 'status', 'complexity',
                                                     'team_lead', 'artist', 'location',
                                                     'sequence__project__client__locality').filter(
                **argumentos).filter(status__code__in=['ATL', 'YTS', 'YTA']).exclude(
                sequence__project__status="ARCHIVED").count()
            wip_count = Shots.objects.select_related('sequence', 'task_type', 'sequence__project',
                                                     'sequence__project__client', 'status', 'complexity',
                                                     'team_lead', 'artist', 'location',
                                                     'sequence__project__client__locality').filter(
                **argumentos).filter(status__code__in=['WIP', 'LAP', 'LRT', 'STQ', 'STC', 'IRT']).exclude(
                sequence__project__status="ARCHIVED").count()
            hold_count = Shots.objects.select_related('sequence', 'task_type', 'sequence__project',
                                                      'sequence__project__client', 'status', 'complexity',
                                                      'team_lead', 'artist', 'location',
                                                      'sequence__project__client__locality').filter(
                **argumentos).filter(status__code__in=['HLD']).exclude(sequence__project__status="ARCHIVED").count()
            omit_count = Shots.objects.select_related('sequence', 'task_type', 'sequence__project',
                                                      'sequence__project__client', 'status', 'complexity',
                                                      'team_lead', 'artist', 'location',
                                                      'sequence__project__client__locality').filter(
                **argumentos).filter(status__code__in=['OMT']).exclude(sequence__project__status="ARCHIVED").count()
            del_count = Shots.objects.select_related('sequence', 'task_type', 'sequence__project',
                                                     'sequence__project__client', 'status', 'complexity',
                                                     'team_lead', 'artist', 'location',
                                                     'sequence__project__client__locality').filter(
                **argumentos).filter(status__code__in=['DTC']).exclude(sequence__project__status="ARCHIVED").count()
            retake_count = Shots.objects.select_related('sequence', 'task_type', 'sequence__project',
                                                        'sequence__project__client', 'status', 'complexity',
                                                        'team_lead', 'artist', 'location',
                                                        'sequence__project__client__locality').filter(
                **argumentos).filter(type__in=['RETAKE']).exclude(sequence__project__status="ARCHIVED").count()
        else:
            yts_count = Shots.objects.filter(status__code__in=['ATL', 'YTS', 'YTA']).exclude(
                sequence__project__status="ARCHIVED").count()
            wip_count = Shots.objects.filter(status__code__in=['WIP', 'LAP', 'LRT', 'STQ', 'STC', 'IRT']).exclude(
                sequence__project__status="ARCHIVED").count()
            hold_count = Shots.objects.filter(status__code__in=['HLD']).exclude(
                sequence__project__status="ARCHIVED").count()
            omit_count = Shots.objects.filter(status__code__in=['OMT']).exclude(
                sequence__project__status="ARCHIVED").count()
            del_count = Shots.objects.filter(status__code__in=['DTC']).exclude(
                sequence__project__status="ARCHIVED").count()
            retake_count = Shots.objects.filter(type__in=['RETAKE']).exclude(
                sequence__project__status="ARCHIVED").count()
        _dat = {
            'yts_count': yts_count,
            'wip_count': wip_count,
            'hold_count': hold_count,
            'omit_count': omit_count,
            'del_count': del_count,
            'retake_count': retake_count
        }
        # serializer = TaskHelpArtistSerializer(task)
        return Response(_dat)

class ElementsData(APIView):

    def get(self, request, format=None):
        """
        Filter Arguments:
            'element_id',
            'project_id',
            'shot_id',
            'seq_id'.
        [ref]: /api/production/elements/?element_id=''&project_id=''&shot_id=''
        """
        query_params = self.request.query_params
        argumentos = {}
        if query_params.get('element_id'):
            argumentos['pk'] = query_params.get('element_id')
        if query_params.get('project_id'):
            argumentos['project_id'] = query_params.get('project_id')
        if query_params.get('seq_id'):
            argumentos['seq_id'] = query_params.get('seq_id')
        if query_params.get('shot_id'):
            argumentos['shot_id'] = query_params.get('shot_id')
        if len(argumentos) > 0:
            element = Elements.objects.select_related('shot_id__sequence', 'shot_id__task_type',
                                                      'shot_id__sequence__project',
                                                      'shot_id__sequence__project__client', 'status',
                                                      'shot_id__complexity', 'shot_id__team_lead',
                                                      'shot_id__artist', 'location',
                                                      'shot_id__sequence__project__client__locality').filter(
                **argumentos)

        else:
            element = Elements.objects.select_related('shot_id__sequence', 'shot_id__task_type',
                                                      'shot_id__sequence__project',
                                                      'shot_id__sequence__project__client', 'status',
                                                      'shot_id__complexity', 'shot_id__team_lead',
                                                      'shot_id__artist', 'location',
                                                      'shot_id__sequence__project__client__locality').all().exclude(
                shot_id__sequence__project__status="ARCHIVED")

        serializer = ElementsSerializer(element, many=True, context={"request": request})
        return Response(serializer.data)

    def post(self, request, format=None):
        """
        To Create a Elements object,
        Pass the parameters in the form of FormData.
        Following are the fields:
            name,
            project_id,
            seq_id,
            shot_id,
            status,
            location,
            vendor,
            creation_date,
            modified_date,
            frame_range,
            first_frame,
            last_frame,
            description,
            layer,
            type,
            _pass,
            version,
            filepath,
            src_path,
            tag
        """
        serializer = ElementsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        """
        To Update a particular object Primary Key is required
        [ref]: /api/production/elements/?element_id=''
        """
        query_params = self.request.query_params
        if query_params:
            element_id = query_params.get('element_id', None)
        element = Elements.objects.get(pk=element_id)
        serializer = ElementsSerializer(element, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        """
        To Delete a particular object Primary Key is required
        [ref]: /api/production/elements/?element_id=''
        """
        query_params = self.request.query_params

        if query_params:
            element_id = query_params.get('element_id', None)
        model_object = Elements.objects.get(pk=element_id)
        model_object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class TestShotsData(APIView):

    def get(self, request, format=None):
        query_params = self.request.query_params

        if query_params:
            project_id = query_params.get('project_id', None)
            client_id = query_params.get('client_id', None)
            if project_id:
                shot = Shots.objects.select_related().filter(
                    sequence__project__pk=project_id)
            elif client_id:
                shot = Shots.objects.select_related().filter(
                    sequence__project__client__pk=client_id).exclude(sequence__project__status="ARCHIVED")
            else:
                status_list = query_params.get('status', None)
                dept = query_params.get('dept', None)
                status = []
                if status_list is not None:
                    for stat in status_list.split('|'):
                        status.append(stat)
                if dept is not None:
                    shot = Shots.objects.select_related().filter(
                        status__code__in=status, task_type__name=dept).exclude(sequence__project__status="ARCHIVED")
                else:
                    shot = Shots.objects.select_related().filter(
                        status__code__in=status).exclude(sequence__project__status="ARCHIVED")
        else:
            shot = Shots.objects.select_related().all().exclude(
                sequence__project__status="ARCHIVED")

        serializer = ShotsSerializer(shot, many=True, context={"request": request})
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ShotsPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class employeeStatistics(APIView, apiRequestManager):

    """
    This for OFX Employee Daily Statistics
    """
    def get(self, request, format=None):
        query_params = self.request.query_params
        argumentos = {}
        if query_params:
            if query_params.get('profile_id'):
                argumentos['employee__profile__id'] = query_params.get('profile_id')
            if query_params.get('ofx_id'):
                argumentos['employee__employee_id'] = query_params.get('ofx_id')
            if query_params.get('from_date') and query_params.get('to_date'):
                argumentos['logDate__range'] = [query_params.get('from_date'), query_params.get('to_date')]
            if query_params.get('dept'):
                depts = []
                for dept in query_params.get('dept').split('|'):
                    depts.append(dept)
                argumentos['employee__department__name__in'] = depts
            ofxstat = EmployeeDailyStatistics.objects.select_related('employee','employee__department').filter(**argumentos)
        else:
            ofxstat = EmployeeDailyStatistics.objects.select_related('employee').all()
        serializer = EmployeeDailyStatisticserializer(ofxstat, many=True)
        return Response(serializer.data)

    def put(self, request):
        """
        To Update a particular object Primary Key is required
        [ref]: /api/production/employeedailystatistics/?object_id=''
        """
        query_params = self.request.query_params
        if query_params:
            object_id = query_params.get('object_id', None)
        element = EmployeeDailyStatistics.objects.get(pk=object_id)
        serializer = EmployeeDailyStatisticserializer(element, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        """
                To Delete a particular object Primary Key is required
                [ref]: /api/production/employeedailystatistics/?object_id=''
                """
        query_params = self.request.query_params

        if query_params:
            object_id = query_params.get('object_id', None)
            model_object = EmployeeDailyStatistics.objects.get(pk=object_id)
            model_object.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
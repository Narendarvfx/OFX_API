#  Copyright (c) 2023.
#  Designed & Developed by Narendar Reddy G, OscarFX Private Limited
#  All rights reserved.
from django.http import JsonResponse
import datetime
from datetime import timedelta
import json
import logging
from itertools import groupby
from operator import itemgetter
from OFX_API import apiRequestManager
from history.models import historyMaping
# from OFX_API import readArguments, magicSerializer
from django.db.models import Count

from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import EmployeeDailyStatisticserializer
from ofx_statistics.models import EmployeeDailyStatistics, TLDailyStatistics, LeadDailyStatistics, ClientStatistics
from history.models import ShotsHistory, MyTaskHistory, TaskDayLogsHistory, DayLogsHistory
from hrm.models import Employee, EmployeeRoleBinding, Role, Leaves, Attendance, Location
from hrm.serializers import RoleSerializer
from production.models import ShotStatus, Shots, ShotVersions, QCVersions, MyTask, RolePipelineSteps, TaskDayLogs, DayLogs, Assignments, ClientVersions, Sequence, Task_Type, Complexity, Location, Clients
from production.serializers import ShotTimeLogSerializer, TaskDayLogsSerializer, DayLogsSerializer
from shotassignments.models import ShotAssignmentsOrder
from ..email import EmailBuild


def loadDateTime(dt = None, reLoadTo='%Y-%m-%dT%H:%M:%S.%f'):
    dt = datetime.datetime.today().strftime('%Y-%m-%dT%H:%M:%S.%f') if dt is None else dt
    inTF = '%Y-%m-%dT%H:%M:%S.%f' if len(dt.split('.'))>1 else '%Y-%m-%dT%H:%M:%S' if len(dt.split('Z'))>1 else '%Y-%m-%dT%H:%M:%S' if len(dt.split('T'))>1 else '%Y-%m-%d'
    return datetime.datetime.strptime(datetime.datetime.strptime(dt,inTF).strftime(reLoadTo),reLoadTo)

class employee_role_binding(APIView, apiRequestManager):
    
    select_related = ['employee', 'employee__role','employee__department','department', 'role', 'bindWith', 'created_by', 'updated_by']

    model = EmployeeRoleBinding

    def get(self, request, format=None):
        collectArguments = {"id": True, "id__in": 'split', "employee__role__name": True, "employee__department__name__in": 'split', "employee__employee_id__in": 'split', "employee__id__in": 'split', "bindWith__id__in": 'split',  "bindWith__employee_id__in": 'split', "department__name__in": 'split', "role__name__in": 'split'}
        return Response(
            self.read(
                request=request,
                model=self.model,
                select_related=self.select_related,
                collectArguments=collectArguments
            ))

class teamLeaadstatistics(APIView, apiRequestManager):
    
    select_related = ['tl','artists']

    model = TLDailyStatistics

    def get(self, request, format=None):
        collectArguments = {"id": True, "id__in": 'split', "tl__id":True, "tl__id__in":'split', "logDate__range": 'split'}
        return Response(
            self.read(
                request=request,
                model=self.model,
                select_related=self.select_related,
                collectArguments=collectArguments
            ))

class leadstatistics(APIView, apiRequestManager):
    
    select_related = ['lead','artists']

    model = LeadDailyStatistics

    def get(self, request, format=None):
        collectArguments = {"id": True, "id__in": 'split', "role__name__in": 'split', "lead__id":True, "lead__id__in":'split', "logDate__range": 'split'}
        return Response(
            self.read(
                request=request,
                model=self.model,
                select_related=self.select_related,
                collectArguments=collectArguments
            ))

class clientversion(APIView, apiRequestManager):
    
    select_related = []

    model = ClientVersions

    def get(self, request, format=None):
        collectArguments = {"id": True, "id__in": 'split', "shot__id":True}
        return Response(
            self.read(
                request=request,
                model=self.model,
                select_related=self.select_related,
                collectArguments=collectArguments
            ))

    def put(self, request, format=None):
        requestData = self.getRequestdData(request=request, model=self.model)
        updated = False
        for x in requestData:
            if len(x['query']) > 0 and self.update(query=x['query'], model=self.model, select_related=self.select_related, data=x['data']):
                cli_ver_data = self.getDBData(model=self.model,
                                          queryFilter={"pk": x['query']['id']},
                                          select_related=['verified_by', 'shot', 'status','sent_by'], queryPerams=["id", 'version', 'shot__id','shot__name', 'shot__sequence__id','shot__sequence__name', 'shot__team_lead__id', 'shot__team_lead__email', 'shot__supervisor__id', 'shot__supervisor__email','shot__sequence__project__id','shot__sequence__project__name', 'shot__task_type__id','shot__task_type__name', 'shot__sequence__project__client__id','shot__sequence__project__client__name', 'shot__naming_check','output_path', 'submission_notes', 'sent_by__id','sent_by__fullName','sent_by__email', 'sent_date','shot__location__name'])
                EmailBuild.on_approve_email_build(version_data=cli_ver_data)
                updated = True
        return Response(data={}, status=status.HTTP_201_CREATED if updated else status.HTTP_404_NOT_FOUND)

class shotAssignments(APIView, apiRequestManager):
    
    select_related = ['lead','shot']

    model = Assignments

    def get(self, request, format=None):
        collectArguments = {"id": True, "id__in": 'split', "lead__id":True, "lead__id__in":'split', "shot__id":True, "shot__id__in":'split' }
        return Response(
            self.read(
                request=request,
                model=self.model,
                select_related=self.select_related,
                collectArguments=collectArguments
            ))
    
    def post(self, request, format=None):
        collectArguments = {"id": True, "id__in": 'split', "lead__id":True, "lead__id__in":'split', "shot__id":True, "shot__id__in":'split' }
        return Response(
            self.read(
                request=request,
                model=self.model,
                select_related=self.select_related,
                collectArguments=collectArguments,
                isGet=False
            ))

class shotLeadsFilter(APIView, apiRequestManager):

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

        if query_params.get('lead'):
            artistsX = self.getDBData(model=EmployeeRoleBinding, queryFilter={"bindWith__id":query_params.get('lead'),"employee__role__name":"VFX ARTIST"}, select_related=['employee'], queryPerams=["id", "employee__id"])
            artis = []
            for x in artistsX:
                artis.append(x['employee']['id'])
            tasks = self.getDBData(model=MyTask, queryFilter={"artist__id__in":artis}, select_related=['shot__task_type', 'shot__sequence','shot__sequence__project', 'artist', 'assigned_by', 'task_status','shot__status__status_segregation'], queryPerams=["id", "shot__id"])
            argumentos['pk__in'] = []
            for x in tasks:
                if x['shot']['id'] not in argumentos['pk__in']:
                    argumentos['pk__in'].append(x['shot']['id'])
        if len(argumentos) > 0:
            queryset = Shots.objects.prefetch_related('timelogs','artists').select_related('sequence', 'task_type',
                                                                                 'sequence__project',
                                                                                 'sequence__project__client', 'status',
                                                                                 'complexity',
                                                                                 'team_lead', 'artist', 'location',
                                                                                 'sequence__project__client__locality','status__status_segregation', 'supervisor').filter(
                **argumentos).exclude(sequence__project__status="ARCHIVED")
        else:
            # queryset = Shots.objects.all()
            queryset = Shots.objects.prefetch_related('timelogs','artists').select_related('sequence', 'task_type',
                                                                                 'sequence__project',
                                                                                 'sequence__project__client', 'status',
                                                                                 'complexity', 'team_lead',
                                                                                 'artist', 'location',
                                                                                 'sequence__project__client__locality','status__status_segregation','supervisor').all().exclude(
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

class tasktype(APIView, apiRequestManager):
    select_related = []
    model = Task_Type
    def get(self, request, format=None):
        collectArguments = {"id": True}
        return Response(self.read(
            request=request,
            model=self.model,
            select_related=self.select_related,
            collectArguments=collectArguments
        ))

class shotsAPI_v2(APIView, apiRequestManager):

    select_related = ['sequence', 'task_type',
                      'sequence__project',
                      'sequence__project__client', 'status',
                      'complexity', 'team_lead',
                      'artist', 'location',
                      'sequence__project__client__locality', 'status__status_segregation']
    model = Shots

    def detectStatusChange(self, request=None, query={}, data={}):
        existingData = self.getDBData(model=self.model, queryFilter=query, select_related=self.select_related, queryPerams=[
                                      "id", "status__id", "status__name", "status__code","bid_days","progress", "artist__id"])
        if len(existingData) == 1 and data.get('status', None) is not None:
            if data['status'] != existingData[0]['status']['id']:
                newStatus = self.getDBData(model=ShotStatus, queryFilter={
                                           'id': data['status']}, select_related=[], queryPerams=["id", "code"])
                if len(newStatus) > 0:
                    shot_id = existingData[0]['id']
                    newShotStatus = ShotStatus.objects.get(pk=newStatus[0]['id'])
                    if newStatus[0]['code'] in ['STQ', 'LAP', 'LRT', 'IAP', 'IRT','DTC','CAP','OMT','HLD','CRT']:
                        if newStatus[0]['code'] in ['CRT']:
                            self.update(query={'id': shot_id}, model=self.model, select_related=[], data={
                                "internal_eta": None,
                                "type": "RETAKE"
                                })
                        if newStatus[0]['code'] in ['IAP','DTC','CAP']:
                            if existingData[0]["progress"] < 100:
                                self.update(query={'id': shot_id}, model=self.model, select_related=[], data={
                                    "progress": 100,
                                    "achieved_mandays": existingData[0]["bid_days"]
                                    })
                                shotDLogs = DayLogsSerializer(DayLogs.objects.filter(shot__pk=shot_id).select_related('shot','artist', 'updated_by')[::-1][:2], many=True, context={"request": request}).data
                                sdLogId = None
                                lastShotLog = None
                                shotLogUpdate = {
                                    "percentage": 100,
                                    "updated_by": Employee.objects.get(email='robot@oscarfx.com'),
                                    "day_percentage": 100,
                                    "shot_biddays": existingData[0]["bid_days"],
                                    "updated_shot_biddays": existingData[0]["bid_days"],
                                    "consumed_man_day": existingData[0]["bid_days"]
                                    }
                                for sdLog in shotDLogs:
                                    if loadDateTime(dt=sdLog["updated_date"], reLoadTo='%Y-%m-%d').date()!=loadDateTime(reLoadTo='%Y-%m-%d').date():
                                        if lastShotLog is None or loadDateTime(dt=sdLog["updated_date"], reLoadTo='%Y-%m-%d').date()>loadDateTime(dt=lastShotLog["updated_date"],reLoadTo='%Y-%m-%d').date():
                                            lastShotLog = sdLog
                                    else:
                                        sdLogId = sdLog
                                        if lastShotLog is None:
                                            lastShotLog = sdLog
                                                
                                if sdLogId is not None:
                                    if lastShotLog["percentage"] != 100:
                                        shotLogUpdate["day_percentage"] = lastShotLog["day_percentage"] + (100 - lastShotLog["percentage"])
                                        shotLogUpdate["consumed_man_day"] = float("%.2f" % ((existingData[0]["bid_days"]/100)*shotLogUpdate["day_percentage"]))
                                        self.update(query={'id': sdLogId['id']}, model=DayLogs, select_related=[], data=shotLogUpdate)
                                elif lastShotLog is None or lastShotLog["percentage"] != 100:
                                    if lastShotLog is not None:
                                        shotLogUpdate["day_percentage"] = 100 - lastShotLog["percentage"]
                                        shotLogUpdate["consumed_man_day"] = float("%.2f" % ((existingData[0]["bid_days"]/100)*shotLogUpdate["day_percentage"]))
                                    if existingData[0]["artist"] is not None:
                                        shotLogUpdate["artist"] = Employee.objects.get(pk=existingData[0]["artist"]["id"])
                                    else:
                                        shotLogUpdate["artist"] = Employee.objects.get(email='robot@oscarfx.com')
                                    shotLogUpdate["shot"] = Shots.objects.get(pk=shot_id)
                                    self.insert(model=DayLogs, data=shotLogUpdate)
                        shotDInfo = self.getDBData(model=Shots, queryFilter={ 'id': shot_id}, select_related=[], queryPerams=["id", "type"])
                        allTasks = self.getDBData(model=MyTask, queryFilter={ 'shot__id': shot_id}, select_related=[], queryPerams=["id", "artist__id", "art_percentage","assigned_bids","type"])
                        for task in allTasks:
                            updateTasksData = {}
                            if newStatus[0]['code'] not in ['CRT'] and shotDInfo[0]["type"] == task["type"]:
                                updateTasksData["task_status"] =  newShotStatus
                            if newStatus[0]['code'] in ['IAP'] and task["art_percentage"] < 100:
                                updateTasksData["art_percentage"] = 100
                            self.update(query={'id': task['id']}, model=MyTask, select_related=[], data=updateTasksData)
                            if newStatus[0]['code'] in ['IAP'] and task["art_percentage"] < 100:
                                taskDLogs = TaskDayLogsSerializer(TaskDayLogs.objects.filter(task__pk=task['id']).select_related('task', 'artist', 'updated_by')[::-1][:2], many=True, context={"request": request}).data
                                tdLogId = None
                                lastTaskLog = None
                                taskLogUpdate = {
                                    "percentage": 100,
                                    "updated_by": Employee.objects.get(email='robot@oscarfx.com'),
                                    "day_percentage": 100,
                                    "consumed_man_day": task["assigned_bids"],
                                    "task_biddays": task["assigned_bids"],
                                    "updated_task_biddays": task["assigned_bids"]
                                    }
                                for tdLog in taskDLogs:
                                    if loadDateTime(dt=tdLog["updated_date"], reLoadTo='%Y-%m-%d').date()!=loadDateTime(reLoadTo='%Y-%m-%d').date():
                                        if lastTaskLog is None or loadDateTime(dt=tdLog["updated_date"], reLoadTo='%Y-%m-%d').date()>loadDateTime(dt=lastTaskLog["updated_date"],reLoadTo='%Y-%m-%d').date():
                                            lastTaskLog = tdLog
                                    else:
                                        tdLogId = tdLog
                                        if lastTaskLog is None:
                                            lastTaskLog = tdLog
                                             
                                if tdLogId is not None:
                                    if lastTaskLog["percentage"] != 100:
                                        taskLogUpdate["day_percentage"] = lastTaskLog["day_percentage"] + (100 - lastTaskLog["percentage"])
                                        taskLogUpdate["consumed_man_day"] = float("%.2f" % ((task["assigned_bids"]/100)*(100 - lastTaskLog["percentage"])))
                                        self.update(query={'id': tdLogId['id']}, model=TaskDayLogs, select_related=[], data=taskLogUpdate)
                                elif lastTaskLog is None or lastTaskLog["percentage"] != 100:
                                    if lastTaskLog is not None:
                                        taskLogUpdate["day_percentage"] = 100 - lastTaskLog["percentage"]
                                        taskLogUpdate["consumed_man_day"] = float("%.2f" % ((task["assigned_bids"]/100)*taskLogUpdate["day_percentage"]))
                                    taskLogUpdate["artist"] = Employee.objects.get(pk=task["artist"]["id"])
                                    taskLogUpdate["task"] = MyTask.objects.get(pk=task['id'])
                                    self.insert(model=TaskDayLogs, data=taskLogUpdate)
                        
                        if newStatus[0]['code'] == 'STQ':
                            existingVersion = self.getDBData(model=ShotVersions, queryFilter={
                                                             'shot__id': shot_id}, select_related=[], queryPerams=["id", "version"])
                            self.insert(model=ShotVersions, data={
                                "shot": Shots.objects.get(pk=shot_id),
                                "version": 'V%03d' % (len(existingVersion)+1),
                                "sent_by": Employee.objects.get(pk=request.user.employee.id),
                                "status": newShotStatus,
                            })
                        elif newStatus[0]['code'] in ['LAP', 'LRT']:
                            lastVersion = self.getLastObject(model=ShotVersions, queryFilter={
                                                             'shot__id': shot_id}, select_related=[], queryPerams=["id", "version"])
                            if lastVersion.get('id', None) is not None:
                                self.update(query={'id': lastVersion['id']}, model=ShotVersions, select_related=[], data={
                                    "verified_by": Employee.objects.get(pk=request.user.employee.id),
                                    "verified_date": datetime.datetime.now(),
                                    "status": newShotStatus,
                                })
                            if newStatus[0]['code'] == 'LAP':
                                existingVersion = self.getDBData(model=QCVersions, queryFilter={
                                    'shot__id': shot_id}, select_related=[], queryPerams=["id", "version"])
                                self.insert(model=QCVersions, data={
                                    "shot": Shots.objects.get(pk=shot_id),
                                    "version": 'V%03d' % (len(existingVersion)+1),
                                    "sent_by": Employee.objects.get(pk=request.user.employee.id),
                                    "status": newShotStatus,
                                })
                        elif newStatus[0]['code'] in ['IAP', 'IRT']:
                            lastVersion = self.getLastObject(model=QCVersions, queryFilter={
                                                             'shot__id': shot_id}, select_related=[], queryPerams=["id", "version"])
                            if lastVersion.get('id', None) is not None:
                                self.update(query={'id': lastVersion['id']}, model=QCVersions, select_related=[], data={
                                    "verified_by": Employee.objects.get(pk=request.user.employee.id),
                                    "verified_date": datetime.datetime.now(),
                                    "status": newShotStatus,
                                })
                            if newStatus[0]['code'] == 'IAP':
                                existingVersion = self.getDBData(model=ClientVersions, queryFilter={
                                    'shot__id': shot_id}, select_related=[], queryPerams=["id", "version"])
                                self.insert(model=ClientVersions, data={
                                    "shot": Shots.objects.get(pk=shot_id),
                                    "version": 'V%03d' % (len(existingVersion)+1),
                                    "sent_by": Employee.objects.get(pk=request.user.employee.id),
                                    "status": newShotStatus,
                                })
                        if newStatus[0]['code'] in ['CRT']:
                            shotDInfo = self.getDBData(model=Shots, queryFilter={ 'id': shot_id}, select_related=[], queryPerams=["id", "type"])
                            compilerTask = self.getDBData(model=MyTask, queryFilter={ 'shot__id': shot_id, 'compiler':2}, select_related=[], queryPerams=["id", "artist__id"])
                            lastVersion = self.getLastObject(model=ClientVersions, queryFilter={
                                'shot__id': shot_id}, select_related=[], queryPerams=["id", "version"])
                            if lastVersion.get('id', None) is not None:
                                self.update(query={'id': lastVersion['id']}, model=ClientVersions, select_related=[], data={
                                    "verified_by": Employee.objects.get(pk=request.user.employee.id),
                                    "verified_date": datetime.datetime.now(),
                                    "status": newShotStatus,
                                })
                            if len(compilerTask)>0:
                                self.insert(model=MyTask, data={
                                    "artist": Employee.objects.get(pk=compilerTask[0]["artist"]["id"]),
                                    "assigned_by": Employee.objects.get(email='robot@oscarfx.com'),
                                    "shot": Shots.objects.get(pk=shot_id),
                                    "type": shotDInfo[0]["type"],
                                    "task_status": ShotStatus.objects.get(code='YTS'),
                                    "compiler": 2,
                                    })
                                self.update(query={'id': compilerTask[0]["id"]}, model=MyTask, data={ "compiler": 1 })
                    elif request.user.employee.role.name=='VFX ARTIST':
                        allTasks = self.getDBData(model=MyTask, queryFilter={'shot__id': shot_id}, select_related=[], queryPerams=["id", "artist__id","compiler"])
                        for x in allTasks:
                            if x["artist"]["id"]==request.user.employee.id and x["compiler"] == 2:
                                self.update(query={'id': x['id']}, model=MyTask, select_related=[], data={
                                    "task_status": newShotStatus,
                                    })                  

    def get(self, request, format=None):
        collectArguments = {
            "id": True,
            "status__code__in": "split",
            'isSubShot':True,
            'isSplitShot':True,
            'sequence__project__client__id':True,
            'sequence__project__client__name':True,
            'sequence__project__id':True,
            'sequence__project__name':True,
            'task_type__id':True,
            'task_type__name':True
            }
        return Response(self.read(
            request=request,
            model=self.model,
            select_related=self.select_related,
            collectArguments=collectArguments
        ))
    
    def post(self, request, format=None):
        if request.data.get('shot_ids', None) is not None:
            argumentos = {}
            shot_ids = []
            for rid in str(request.data['shot_ids']).split('|'):
                shot_ids.append(rid)
            argumentos['pk__in'] = shot_ids
            queryset = Shots.objects.prefetch_related('timelogs','artists').select_related('sequence', 'task_type', 'sequence__project', 'sequence__project__client', 'status', 'complexity', 'team_lead', 'artist', 'location', 'sequence__project__client__locality','status__status_segregation', 'supervisor').filter(**argumentos)
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
        else:
            collectArguments = {"id": True, "id__in": "split"}
            return Response(self.read(
                request=request,
                model=self.model,
                select_related=self.select_related,
                collectArguments=collectArguments,
                isGet=False
            ))

    def put(self, request, format=None):
        requestData = self.getRequestdData(request=request, model=self.model)
        updated = False
        for x in requestData:
            if len(x['query']) > 0:
                self.detectStatusChange(request=request, query=x['query'], data=x['data'])
                self.prepareHistoryLog(model=ShotsHistory,targetModel=Shots,parentField='sequence',query=x['query'],data=x['data'],request=request,requestType='PUT',defaultMsgMap=historyMaping['ShotsHistory']['PUT'],customizedMsgMap=x['customizedHistory'])
                if self.update(query=x['query'], model=self.model, select_related=self.select_related, data=x['data']):
                    self.createHistoryLog(model=ShotsHistory,targetModel=Shots,parentModel=Sequence,parentField='sequence',query=x['query'],data=x['data'],request=request,requestType='PUT',defaultMsgMap=historyMaping['ShotsHistory']['PUT'],customizedMsgMap=x['customizedHistory'],employeeModel=Employee)
                    updated = True
                    if x['data'].get('bid_days',None) is not None:
                        usedBids = float(x['data']['bid_days'])
                        allSubShots = self.getDBData(model=Shots, queryFilter={'parentShot__id': Shots.objects.get(**x['query']).pk},queryPerams=['id','bid_days'])
                        for x in allSubShots:
                            usedBids = usedBids + float(x['bid_days'])
                        self.update(query={'id': Shots.objects.get(**x['query']).pk}, model=Shots, data={'actual_bid_days':usedBids})
        return Response(data={}, status=status.HTTP_201_CREATED if updated else status.HTTP_404_NOT_FOUND)

    def delete(self, request, format=None):
        collectArguments = {"id": True}
        self.prepareHistoryLog(model=ShotsHistory,targetModel=Shots,parentField='sequence',query={'pk':request.GET['id']},data={'name': True},request=request,requestType='DELETE',defaultMsgMap=historyMaping['ShotsHistory']['DELETE'],customizedMsgMap={})
        isDone = self.delete_row( request=request, model=self.model, useArguments=collectArguments)
        if isDone:
            self.createHistoryLog(model=ShotsHistory,targetModel=Shots,parentModel=Sequence,parentField='sequence',query={'pk':request.GET['id']},data={'name': True},request=request,requestType='DELETE',defaultMsgMap=historyMaping['ShotsHistory']['DELETE'],customizedMsgMap={},employeeModel=Employee)
        return Response(status=status.HTTP_204_NO_CONTENT if isDone else status.HTTP_404_NOT_FOUND)

class helpShots(APIView, apiRequestManager):

    select_related = []
    model = Shots

    def get(self, request, format=None):
        if  request.query_params.get('parent_shot_id', None) is not None:
            argumentos = {'parentShot__id':request.query_params['parent_shot_id']}
            queryset = Shots.objects.prefetch_related('timelogs','artists').select_related('sequence', 'task_type', 'sequence__project', 'sequence__project__client', 'status', 'complexity', 'team_lead', 'artist', 'location', 'sequence__project__client__locality','status__status_segregation', 'supervisor').filter(**argumentos)
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
        else:
            return Response([])

    def put(self, request, format=None):
        requestData = self.getRequestdData(request=request, model=self.model)
        for x in requestData:
            mainShotId = None
            if len(x['query']) > 0:
                if x['isNew'] is not None:
                    _mainShot = self.getDBData(model=Shots, queryFilter={'pk':x['data']['parentShot']},queryPerams=list(self.getModelFields(model=Shots).keys()))
                    if len(_mainShot)>0:
                        mainShotId = x['data']['parentShot']
                        data = {
                            "status": ShotStatus.objects.get(code='YTA'),
                            # "parentShot": Shots.objects.get(pk=x['data']['parentShot']),
                            "parentShot": x['data']['parentShot'],
                            # "task_type": Task_Type.objects.get(pk=x['data']['task_type']),
                            # "task_type": int(x['data']['task_type']),
                            "isSubShot":True
                            }
                        for y,_x in _mainShot[0].items():
                            if isinstance(_x,type(None)) is False and y not in list(data.keys()) and y in ["name","sequence","type","actual_start_frame","actual_end_frame","work_start_frame","work_end_frame","start_date","end_date","description","complexity","duplicate","package_id","estimate_id","estimate_date","location","input_path"]:
                            # if isinstance(_x,type(None)) is False and y not in ['id','isSubShot','timelogs','shotshistory','status','task_type','eta','bid_days','internal_bid_days','actual_bid_days', 'progress','supervisor','team_lead','artist','artists','scope_of_work','qc_name','pending_mandays','achieved_mandays','retake_path','output_path','comments','version','submitted_date']:
                                data[y] = _x
                        for y,_x in x['data'].items():
                            if data.get(y,'__BLANK__')=='__BLANK__':
                                data[y] = _x
                        data['internal_eta']=data['eta']
                        data['internal_bid_days']=data['bid_days']
                        data['actual_bid_days']=data['bid_days']
                        _thisSubShot = self.getDBData(model=Shots, queryFilter={'parentShot__id': x['data']['parentShot'],'task_type__pk': data['task_type']},queryPerams=list(self.getModelFields(model=Shots).keys()))
                        if len(_thisSubShot)>0:
                            self.prepareHistoryLog(model=ShotsHistory,targetModel=Shots,parentField='sequence',query={"pk": _thisSubShot[0]["id"]},data=x['data'],request=request,requestType='PUT',defaultMsgMap=historyMaping['ShotsHelpHistory']['PUT'],customizedMsgMap=x['customizedHistory'])
                            self.update(query={"pk": _thisSubShot[0]["id"]}, model=Shots, data=x['data'])
                            self.createHistoryLog(model=ShotsHistory,targetModel=Shots,parentModel=Sequence,parentField='sequence',query={"pk": _thisSubShot[0]["id"]},data=x['data'],request=request,requestType='PUT',defaultMsgMap=historyMaping['ShotsHelpHistory']['PUT'],customizedMsgMap=x['customizedHistory'],employeeModel=Employee)
                        else:
                            data["task_type"] = Task_Type.objects.get(pk=x['data']['task_type'])
                            self.insert(model=self.model, data=data)
                            self.createHistoryLog(model=ShotsHistory,targetModel=Shots,parentModel=Sequence,parentField='sequence',query={'parentShot__id':x['data']['parentShot'],'task_type__pk':x['data']['task_type']},data={ "task_type": True },request=request,requestType='POST',defaultMsgMap=historyMaping['ShotsHelpHistory']['POST'],customizedMsgMap=x['customizedHistory'],employeeModel=Employee)
                else:
                    if x['data'].get('bid_days',None) is not None: #this not real "bid_days" its actually "actual_bid_days"
                        # Below 7 lines are feature use if the sub shot having again subshot
                        cSubShot = list(Shots.objects.filter(**x['query']).values('id','bid_days','actual_bid_days'))[0]
                        reSubShot = list(Shots.objects.filter(parentShot__id=cSubShot['id']).values('id','actual_bid_days'))
                        allSubShots = self.getDBData(model=Shots, queryFilter={'id': cSubShot['id']},queryPerams=['id','bid_days'])
                        _reuserdBids = 0
                        for resub in reSubShot:
                            _reuserdBids += resub['actual_bid_days']
                        x['data']['actual_bid_days'] = x['data']['bid_days']
                        x['data']['bid_days'] = x['data']['actual_bid_days'] - _reuserdBids
                    self.prepareHistoryLog(model=ShotsHistory,targetModel=Shots,parentField='sequence',query=x['query'],data=x['data'],request=request,requestType='PUT',defaultMsgMap=historyMaping['ShotsHelpHistory']['PUT'],customizedMsgMap=x['customizedHistory'])
                    self.update(query=x['query'], model=Shots, data=x['data'])
                    self.createHistoryLog(model=ShotsHistory,targetModel=Shots,parentModel=Sequence,parentField='sequence',query=x['query'],data=x['data'],request=request,requestType='PUT',defaultMsgMap=historyMaping['ShotsHelpHistory']['PUT'],customizedMsgMap=x['customizedHistory'],employeeModel=Employee)
                    _thisSubShot = self.getDBData(model=Shots, queryFilter=x['query'],queryPerams=['id','parentShot__id'])
                    mainShotId = _thisSubShot[0]['parentShot']['id']
                if mainShotId is not None:
                    mainShotObj = Shots.objects.get(id=mainShotId)
                    mainShotData = {
                        'id': mainShotObj.pk,
                        'eta': mainShotObj.eta,
                        'bid_days': mainShotObj.bid_days,
                        'actual_bid_days': mainShotObj.actual_bid_days,
                        'internal_bid_days': mainShotObj.internal_bid_days
                        }
                    usedBids = 0
                    allSubShots = list(Shots.objects.filter(parentShot__id=mainShotId).values('id','eta','bid_days','actual_bid_days'))
                    for _x in allSubShots:
                        usedBids = usedBids + _x['actual_bid_days']
                    mainBids = mainShotData['bid_days'] if mainShotData['actual_bid_days'] == 0 else mainShotData['actual_bid_days']
                    _updateShot = {}
                    if mainShotData['actual_bid_days'] == 0:
                        _updateShot['actual_bid_days'] = mainBids
                        mainShotData['actual_bid_days'] = mainBids
                    if mainShotData['internal_bid_days'] == 0:
                        _updateShot['internal_bid_days'] = mainShotData['bid_days']
                    if (mainShotData['actual_bid_days'] - usedBids)!=mainShotData['bid_days']:
                        _updateShot['bid_days'] = mainShotData['actual_bid_days'] - usedBids
                    if len(list(_updateShot.keys()))>0:
                        self.prepareHistoryLog(model=ShotsHistory,targetModel=Shots,parentField='sequence',query={'pk':mainShotId},data=_updateShot,request=request,requestType='PUT',defaultMsgMap=historyMaping['ShotsHistory']['PUT'])
                        self.update(query={'id':mainShotId}, model=Shots, data=_updateShot)
                        self.createHistoryLog(model=ShotsHistory,targetModel=Shots,parentModel=Sequence,parentField='sequence',query={'pk':mainShotId},data=_updateShot,request=request,requestType='PUT',defaultMsgMap=historyMaping['ShotsHistory']['PUT'],employeeModel=Employee)
        return Response(data={}, status=status.HTTP_201_CREATED)

    def delete(self, request, format=None):
        deleted = False
        collectArguments = {"id": True}
        thisShot = self.getDBData(model=self.model, queryFilter={"id": request.GET['id']}, select_related=self.select_related, queryPerams=["id", "parentShot__id",'bid_days','actual_bid_days'])
        if len(thisShot)>0:
            mainShotId = thisShot[0]["parentShot"]["id"]
            self.prepareHistoryLog(model=ShotsHistory,targetModel=Shots,parentField='sequence',query={'pk':request.GET['id']},data={'task_type':True},request=request,requestType='DELETE',defaultMsgMap=historyMaping['ShotsHelpHistory']['DELETE'])
            deleted = self.delete_row(request=request, model=self.model, useArguments=collectArguments )
            if deleted:
                self.createHistoryLog(model=ShotsHistory,targetModel=Shots,parentModel=Sequence,parentField='sequence',query={'pk':request.GET['id']},data={'task_type':True},request=request,requestType='DELETE',defaultMsgMap=historyMaping['ShotsHelpHistory']['DELETE'],employeeModel=Employee)
                mainShot = self.getDBData(model=Shots, queryFilter={'pk':mainShotId},queryPerams=['id','eta','bid_days','actual_bid_days','internal_bid_days'])
                # allMainShotTasks = self.getDBData(model=MyTask, queryFilter={'shot__id':mainShotId},queryPerams=['id','assigned_bids'])
                usedBids = 0
                # for x in allMainShotTasks:
                #     usedBids = usedBids + x['assigned_bids']
                allSubShots = self.getDBData(model=Shots, queryFilter={'parentShot__id':mainShotId},queryPerams=['id','eta','bid_days'])
                for x in allSubShots:
                    usedBids = usedBids + x['bid_days']
                mainBids = mainShot[0]['bid_days'] if mainShot[0]['actual_bid_days'] == 0 else mainShot[0]['actual_bid_days']
                _updateShot = {}
                if mainShot[0]['actual_bid_days'] == 0:
                    _updateShot['actual_bid_days'] = mainBids
                    mainShot[0]['actual_bid_days'] = mainBids
                if mainShot[0]['internal_bid_days'] == 0:
                    _updateShot['internal_bid_days'] = mainShot[0]['bid_days']
                if (mainShot[0]['actual_bid_days'] - usedBids)!=mainShot[0]['bid_days']:
                    _updateShot['bid_days'] = mainShot[0]['actual_bid_days'] - usedBids
                if len(list(_updateShot.keys()))>0:
                    self.prepareHistoryLog(model=ShotsHistory,targetModel=Shots,parentField='sequence',query={'pk':mainShotId},data=_updateShot,request=request,requestType='PUT',defaultMsgMap=historyMaping['ShotsHistory']['PUT'])
                    self.update(query={'pk':mainShotId}, model=Shots, data=_updateShot)
                    self.createHistoryLog(model=ShotsHistory,targetModel=Shots,parentModel=Sequence,parentField='sequence',query={'pk':mainShotId},data=_updateShot,request=request,requestType='PUT',defaultMsgMap=historyMaping['ShotsHistory']['PUT'],employeeModel=Employee)
        return Response(status=status.HTTP_204_NO_CONTENT if deleted else status.HTTP_404_NOT_FOUND)
    
class shotTasks(APIView, apiRequestManager):

    select_related = ['shot__task_type', 'shot__sequence',
                      'shot__sequence__project', 'artist', 'assigned_by', 'task_status','shot__status__status_segregation']

    model = MyTask

    def get(self, request, format=None):
        collectArguments = {"id": True, "shot__id": True,"artist__id": True,"eta__range": 'split',"creation_date__range": 'split'}
        return Response(
            self.read(
                request=request,
                model=self.model,
                select_related=self.select_related,
                collectArguments=collectArguments
            ))
    
    def put(self, request, format=None):
        requestData = self.getRequestdData(request=request, model=self.model)
        shot_id = None
        _permistions = json.loads(json.dumps(RoleSerializer(Role.objects.get(name=request.user.employee.role)).data, default=str))
        _permistions = [_per['permission_key'] for _per in _permistions['permissions']]
        _nowEmp = Employee.objects.get(pk=request.user.employee.id)
        for x in requestData:
            if len(x['query']) > 0:
                if x['isNew'] is not None:
                    data={art:x['data'][art] for art in ["art_percentage","assigned_bids","start_date","end_date","eta","compiler","version"] if x['data'].get(art,None) is not None}
                    data["artist"] = Employee.objects.get(pk=x['data']["artist"])
                    data["assigned_by"] = Employee.objects.get(pk=request.user.employee.id)
                    data["shot"] = Shots.objects.get(pk=x['data']["shot"])
                    data["task_status"] = ShotStatus.objects.get(code='YTS')
                    existingData = self.getDBData(model=self.model, queryFilter={"artist__id":x['data']["artist"],"shot__id":x['data']["shot"]}, select_related=self.select_related, queryPerams=[
                                      "id", "shot__id","compiler"])
                    shot_id = {"shot__id":x['data']["shot"]}
                    if len(existingData)==0:
                        self.insert(model=self.model, data=data)
                        _hData = self.getDBData(model=self.model, queryFilter={"artist__id":x['data']["artist"],"shot__id":x['data']["shot"]}, select_related=self.select_related, queryPerams=["id"])[0]
                        self.createHistoryLog(model=MyTaskHistory,targetModel=MyTask,parentModel=Shots,parentField='shot',query={'id':_hData['id']},data={'artist': x['data']["artist"]},request=request,requestType='POST',defaultMsgMap=historyMaping['MyTaskHistory']['POST'],customizedMsgMap={},employeeModel=Employee)
                        
                        shotInfoX = self.getDBData(model=Shots, queryFilter={"pk": shot_id["shot__id"]}, queryPerams=["id", "status__id", "status__name", "status__code","task_type__id","task_type__name","location__id","isSubShot"])[0]
                        assQ = {"isSubShot": shotInfoX["isSubShot"],"shotStatus__code": shotInfoX["status"]["code"]}
                        if shotInfoX['location'] is not None:
                            assQ["location__id"] = shotInfoX["location"]["id"]
                        assignmentSteps = self.getDBData(model=ShotAssignmentsOrder, queryFilter=assQ, queryPerams=["id", "department__id", "department__name", "isBeforeArtist"])
                        updateShotStatus = False
                        for asiX in assignmentSteps:
                            if asiX["isBeforeArtist"] is True and (asiX["department"]["name"] == 'PRODUCTION' or shotInfoX["task_type"]["name"] == asiX["department"]["name"]):
                                updateShotStatus = True
                        if updateShotStatus:
                            self.prepareHistoryLog(model=ShotsHistory,targetModel=Shots,parentField='sequence',query={"pk": shot_id["shot__id"]},data={ "status": True },request=request,requestType='PUT',defaultMsgMap=historyMaping['ShotsHistory']['PUT'],customizedMsgMap=x['customizedHistory'])
                            self.update(query={"pk": shot_id["shot__id"]}, model=Shots, data={ "status": data["task_status"] })
                            self.createHistoryLog(model=ShotsHistory,targetModel=Shots,parentModel=Sequence,parentField='sequence',query={"pk": shot_id["shot__id"]},data={ "status": True },request=request,requestType='PUT',defaultMsgMap=historyMaping['ShotsHistory']['PUT'],customizedMsgMap=x['customizedHistory'],employeeModel=Employee)
                    else:
                        self.prepareHistoryLog(model=MyTaskHistory,targetModel=MyTask,parentField='shot',query={"artist__id":x['data']["artist"],"shot__id":x['data']["shot"]},data=data,request=request,requestType='PUT',defaultMsgMap=historyMaping['MyTaskHistory']['PUT'],customizedMsgMap=x['customizedHistory'])
                        self.update(query={"artist__id":x['data']["artist"],"shot__id":x['data']["shot"]}, model=self.model, select_related=self.select_related, data=data)
                        self.createHistoryLog(model=MyTaskHistory,targetModel=MyTask,parentModel=Shots,parentField='shot',query={"pk": shot_id["shot__id"]},data=data,request=request,requestType='PUT',defaultMsgMap=historyMaping['MyTaskHistory']['PUT'],customizedMsgMap=x['customizedHistory'],employeeModel=Employee)
                else:
                    existingData = self.getDBData(model=self.model, queryFilter=x['query'], select_related=self.select_related, queryPerams=[ "id", "shot__id","assigned_bids"])
                    if len(existingData)>0:
                        if x['data'].get('assigned_bids',None) is not None and float(x['data']['assigned_bids']) > 0:
                            taskLogs = self.getDBData(model=TaskDayLogs, queryFilter={'task__id':x['query']['id']}, select_related=self.select_related, queryPerams=[ "id","task_biddays","updated_task_biddays","percentage","day_percentage","consumed_man_day"])
                            _taskBids = float(existingData[0]["assigned_bids"])
                            _newBids = float(x['data']['assigned_bids'])
                            for _task in taskLogs:
                                _new_log_update = {}
                                if _task["task_biddays"] is None:
                                    _task["task_biddays"] = _taskBids
                                    _new_log_update["task_biddays"] = _taskBids
                                if _task["updated_task_biddays"] is None:
                                    _task["updated_task_biddays"] = _taskBids
                                if float(_task["updated_task_biddays"]) != _newBids:
                                    if _newBids <= float(_task["consumed_man_day"]):
                                        _new_log_update["percentage"] = 100
                                    else:
                                        _new_log_update["percentage"] = int((100/_newBids)*float((_task["updated_task_biddays"]/100)*_task["percentage"]))
                                        if _new_log_update["percentage"]>100:
                                            _new_log_update["percentage"] = 100
                                    _new_log_update["day_percentage"] = int((100/_newBids)*float(_task["consumed_man_day"]))
                                    if _new_log_update["day_percentage"]>100:
                                        _new_log_update["day_percentage"] = 100
                                        _new_log_update["consumed_man_day"] = _newBids
                                    _new_log_update["updated_by"] = _nowEmp
                                    _new_log_update["updated_task_biddays"] = _newBids
                                if len(list(_new_log_update.keys()))>0:
                                    self.prepareHistoryLog(model=TaskDayLogsHistory,targetModel=TaskDayLogs,parentField='task',query={"id":_task["id"]},data=_new_log_update,request=request,requestType='PUT',defaultMsgMap=historyMaping['TaskDayLogsHistory']['PUT'],customizedMsgMap={})
                                    self.update(query={"id":_task["id"]}, model=TaskDayLogs, select_related=[], data=_new_log_update)
                                    self.createHistoryLog(model=TaskDayLogsHistory,targetModel=TaskDayLogs,parentModel=MyTask,parentField='task',query={"id":_task["id"]},data=_new_log_update,request=request,requestType='PUT',defaultMsgMap=historyMaping['TaskDayLogsHistory']['PUT'],customizedMsgMap={},employeeModel=Employee)
                                    if _new_log_update.get("percentage",None) is not None:
                                        x['data']["art_percentage"] = _new_log_update["percentage"]
                                else:
                                    x['data']["art_percentage"] = _task["percentage"]
                        self.prepareHistoryLog(model=MyTaskHistory,targetModel=MyTask,parentField='shot',query=x['query'],data=x['data'],request=request,requestType='PUT',defaultMsgMap=historyMaping['MyTaskHistory']['PUT'],customizedMsgMap=x['customizedHistory'])
                        self.update(query=x['query'], model=self.model, select_related=self.select_related, data=x['data'])
                        self.createHistoryLog(model=MyTaskHistory,targetModel=MyTask,parentModel=Shots,parentField='shot',query=x['query'],data=x['data'],request=request,requestType='PUT',defaultMsgMap=historyMaping['MyTaskHistory']['PUT'],customizedMsgMap=x['customizedHistory'],employeeModel=Employee)
                        shot_id = {"shot__id":existingData[0]["shot"]["id"]}
        if len(requestData)==0 and shot_id is None and request.query_params.get('shot_id',None) is not None:
            shot_id = {"shot__id": request.query_params.get('shot_id',None)}
        shot_compiler = None
        shotInfo = None
        if shot_id is not None:
            allTasks = self.getDBData(model=self.model, queryFilter=shot_id, select_related=self.select_related, queryPerams=["id", "shot__id","compiler", "task_status__id", "task_status__name", "task_status__code","artist__id"])
            if len(allTasks)>0:
                shotInfo = self.getDBData(model=Shots, queryFilter={"id":shot_id['shot__id']}, select_related=[], queryPerams=["id", "status__id","status__id", "status__name", "status__code","supervisor__id","team_lead__id","hod__id","artist__id","artists__id"])
                for x in allTasks:
                    if x['compiler']==2:
                        shot_compiler = x
                if shot_compiler is None:
                    shot_compiler = allTasks[0]
                    self.update(query={"id":shot_compiler["id"]}, model=self.model, select_related=self.select_related, data={"compiler":2})
                if len(shotInfo)>0:
                    shotInfo = shotInfo[0]
                    shotUpdate = {}
                    if shot_compiler['artist'] is not None and (shotInfo['artist'] is None or shot_compiler['artist']['id']!=shotInfo['artist']['id']):
                        shotUpdate = {
                            "artist": shot_compiler['artist']['id'],
                            }
                        if request.query_params.get('changeTLSUP',None) is not None or shotInfo['supervisor'] is None:
                            supervisor = self.getDBData(model=EmployeeRoleBinding, queryFilter={"role__name":'SUPERVISOR',"employee__role__name":"VFX ARTIST","employee__id":shot_compiler['artist']['id']}, select_related=[], queryPerams=["id", "bindWith__id"])
                            if len(supervisor)>0:
                                shotUpdate["supervisor"] = supervisor[0]["bindWith"]["id"]

                        if request.query_params.get('changeTLSUP',None) is not None or shotInfo['hod'] is None:
                            hod = self.getDBData(model=EmployeeRoleBinding, queryFilter={"role__name":'HEAD OF DEPARTMENT',"employee__role__name":"VFX ARTIST","employee__id":shot_compiler['artist']['id']}, select_related=[], queryPerams=["id", "bindWith__id"])
                            if len(hod)>0:
                                shotUpdate["hod"] = hod[0]["bindWith"]["id"]

                        if request.query_params.get('changeTLSUP',None) is not None or shotInfo['team_lead'] is None:
                            team_lead = self.getDBData(model=EmployeeRoleBinding, queryFilter={"role__name":'TEAM LEAD',"employee__role__name":"VFX ARTIST","employee__id":shot_compiler['artist']['id']}, select_related=[], queryPerams=["id", "bindWith__id"])
                            if len(team_lead)>0:
                                shotUpdate["team_lead"] = team_lead[0]["bindWith"]["id"]
                            
                    if request.user.employee.role.name == 'VFX ARTIST' and shot_compiler["task_status"]["id"]!=shotInfo["status"]["id"]:
                        shotUpdate["status"] = shot_compiler["task_status"]["id"]
                    if len(shotUpdate)>0:
                        shotApi = shotsAPI_v2()
                        shotApi.detectStatusChange(request=request, query={"id":shotInfo["id"]}, data=shotUpdate)
                        self.prepareHistoryLog(model=ShotsHistory,targetModel=Shots,parentField='sequence',query={"id":shotInfo["id"]},data=shotUpdate,request=request,requestType='PUT',defaultMsgMap=historyMaping['ShotsHistory']['PUT'],customizedMsgMap={})
                        self.update(query={"id":shotInfo["id"]}, model=Shots, select_related=[], data=shotUpdate)
                        self.createHistoryLog(model=ShotsHistory,targetModel=Shots,parentModel=Sequence,parentField='sequence',query={"id":shotInfo["id"]},data=shotUpdate,request=request,requestType='PUT',defaultMsgMap=historyMaping['ShotsHistory']['PUT'],customizedMsgMap={},employeeModel=Employee)
                        
                    if shotUpdate.get("artist",None) is not None:
                        shotsObj = Shots.objects.get(id=shotInfo["id"])
                        for ep in shotInfo["artists"]:
                            shotsObj.artists.remove(Employee.objects.get(pk=ep['id']))
                        for ep in allTasks:
                            shotsObj.artists.add(Employee.objects.get(pk=ep['artist']['id']))
        return Response(data={}, status=status.HTTP_201_CREATED)

    def delete(self, request, format=None):
        deleted = False
        collectArguments = {"id": True}
        thisTasks = self.getDBData(model=self.model, queryFilter={"id": request.GET['id']}, select_related=self.select_related, queryPerams=["id", "shot__id","artist__id"])
        if len(thisTasks)>0:
            shot_id = str(thisTasks[0]['shot']['id'])
            artist_id = str(thisTasks[0]['artist']["id"])
            self.prepareHistoryLog(model=MyTaskHistory,targetModel=MyTask,parentField='shot',query={'pk':request.GET['id']},data={'artist': artist_id},request=request,requestType='DELETE',defaultMsgMap=historyMaping['MyTaskHistory']['DELETE'],customizedMsgMap={})
            deleted = self.delete_row(request=request, model=self.model, useArguments=collectArguments )
            if deleted:
                self.createHistoryLog(model=MyTaskHistory,targetModel=MyTask,parentModel=Shots,parentField='shot',query={'pk':request.GET['id']},data={'artist': artist_id},request=request,requestType='DELETE',defaultMsgMap=historyMaping['MyTaskHistory']['DELETE'],customizedMsgMap={},employeeModel=Employee)    
                shotsObj = Shots.objects.get(id=shot_id)
                shotsObj.artists.remove(Employee.objects.get(pk=artist_id))
        return Response(status=status.HTTP_204_NO_CONTENT if deleted else status.HTTP_404_NOT_FOUND)


class rolePipelineSteps(APIView, apiRequestManager):

    select_related = []

    model = RolePipelineSteps

    def get(self, request, format=None):
        collectArguments = {"id": True}
        return Response(
            self.read(
                request=request,
                model=self.model,
                select_related=self.select_related,
                collectArguments=collectArguments
            ))

    def delete(self, request, format=None):
        collectArguments = {"id": True}
        return Response(status=status.HTTP_204_NO_CONTENT if self.delete_row(
            request=request,
            model=self.model,
            useArguments=collectArguments
        ) else status.HTTP_404_NOT_FOUND)


# class assignmentStepsOrders(APIView, apiRequestManager):

#     select_related = []

#     model = AssignmentStepsOrder

#     def get(self, request, format=None):
#         collectArguments = {"id": True, "department__id": True, "department__name": True, "shotStatus__id":True, "shotStatus__code":True,"authorised_roles__name__in":"split" }
#         return Response(
#             self.read(
#                 request=request,
#                 model=self.model,
#                 select_related=self.select_related,
#                 collectArguments=collectArguments
#             ))

#     def delete(self, request, format=None):
#         collectArguments = {"id": True}
#         return Response(status=status.HTTP_204_NO_CONTENT if self.delete_row(
#             request=request,
#             model=self.model,
#             useArguments=collectArguments
#         ) else status.HTTP_404_NOT_FOUND)

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

class mandaysavailability(APIView, apiRequestManager):

    """
    This for Mandays Availability
    """
    def get(self, request, format=None):
        query_params = self.request.query_params
        dateFormat='%Y-%m-%d'
        if  query_params.get('from_date') and query_params.get('to_date'):
            _range = self.weeksRange(from_date=query_params.get('from_date'),to_date=query_params.get('to_date'))
            weekRanges = {}
            weekRangesIndex = {}
            for day in range(0, _range):
                weekCount = 'week_'+str(len(list(weekRanges.values())))
                fromD = self.addDays(date=query_params.get('from_date'),days=(day*7)-datetime.datetime.strptime(query_params.get('from_date'), self.dateFormat).weekday())
                toD = self.addDays(date=query_params.get('from_date'),days=((day*7)+6)-datetime.datetime.strptime(query_params.get('from_date'), self.dateFormat).weekday())
                weekRanges[weekCount] = {
                        "range": {
                            "from": str(fromD.strftime('%Y-%m-%d')),
                            "to":str(toD.strftime('%Y-%m-%d'))
                            },
                        "tmd": 0,
                        "bid_days": 0,
                        "achieved_mandays": 0,
                        "pending_mandays": 0,
                        }
                _dRange = self.daysRange(from_date=str(fromD.strftime('%Y-%m-%d')),to_date=str(toD.strftime('%Y-%m-%d')))
                for day in range(0, _dRange):
                    thisDate = self.addDays(date=str(fromD.strftime('%Y-%m-%d')),days=day)
                    weekRangesIndex[str("date_"+thisDate.strftime('%Y_%m_%d'))] = str(weekCount)
            ShotsSelectRelated = ['sequence', 'task_type', 'sequence__project', 'sequence__project__client', 'status', 'complexity', 'team_lead', 'artist', 'location', 'sequence__project__client__locality', 'status__status_segregation']
            sotQ = {'eta__range':[query_params.get('from_date')+"T00:00:00.000000", query_params.get('to_date')+'T23:59:59.999999']}
            if  query_params.get('dept',None) is not None:
                sotQ['task_type__name'] = query_params.get('dept')
            shotsData = self.getDBData(model=Shots, queryFilter=sotQ, select_related=ShotsSelectRelated, queryPerams=["id", "task_type__id", "task_type__name", "bid_days","achieved_mandays","eta"])
            depData = {}
            listDep = []
            for x in shotsData:
                sKey = self.makeKey(strd=x["task_type"]["name"])
                if x["eta"] is not None:
                    thisData = str("date_"+datetime.datetime.strptime(x["eta"].split(' ')[0], dateFormat).strftime('%Y_%m_%d'))
                    if depData.get(sKey,None) is None:
                        listDep.append(x["task_type"]["name"])
                        depData[sKey] = {
                            "task_type": x["task_type"],
                            "data": {}
                            }
                    if depData[sKey]["data"].get(thisData,None) is None:
                        depData[sKey]["data"][thisData] = {
                                "date": str(datetime.datetime.strptime(x["eta"].split(' ')[0], dateFormat).strftime('%Y-%m-%d')),
                                "tmd": 0,
                                "bid_days": 0,
                                "achieved_mandays": 0,
                                "pending_mandays": 0,
                                }
                    depData[sKey]["data"][thisData]["bid_days"] = depData[sKey]["data"][thisData]["bid_days"] + x["bid_days"]
                    depData[sKey]["data"][thisData]["achieved_mandays"] = depData[sKey]["data"][thisData]["achieved_mandays"] + x["achieved_mandays"]
                    depData[sKey]["data"][thisData]["pending_mandays"] = depData[sKey]["data"][thisData]["bid_days"] - depData[sKey]["data"][thisData]["achieved_mandays"]
            
            if len(listDep) > 0:
                empDailyStatistics = self.getDBData(model=EmployeeDailyStatistics, queryFilter={'logDate__range':[datetime.datetime.now().strftime('%Y-%m-%d') if query_params.get('isCurrent',None) is not None else query_params.get('from_date'), query_params.get('to_date')],"employee__department__name__in":listDep, "employee__role__name":"VFX ARTIST"}, select_related=['employee','employee__department','employee__role'], queryPerams=["id", "tmd","employee__id","employee__department__id","employee__department__name","logDate"])
                for x in empDailyStatistics:
                    sKey = self.makeKey(strd=x["employee"]["department"]["name"])
                    thisData = str("date_"+datetime.datetime.strptime(x["logDate"], dateFormat).strftime('%Y_%m_%d'))
                    if depData[sKey]["data"].get(thisData,None) is None:
                        depData[sKey]["data"][thisData] = {
                            "date": str(datetime.datetime.strptime(x["logDate"], dateFormat).strftime('%Y-%m-%d')),
                            "tmd": 0,
                            "bid_days": 0,
                            "achieved_mandays": 0,
                            "pending_mandays": 0,
                            }
                    depData[sKey]["data"][thisData]["tmd"] = depData[sKey]["data"][thisData]["tmd"] + x["tmd"]
            rData = []
            for x in list(depData.values()):
                varX = {
                    "task_type": x["task_type"],
                    "data":{}
                    }
                for wk in list(weekRanges.keys()):
                    varX["data"][wk] = json.loads(json.dumps(weekRanges[wk]))
                for date in list(x["data"].values()):
                    thisData = datetime.datetime.strptime(date["date"], dateFormat)
                    if weekRangesIndex.get(str("date_"+thisData.strftime('%Y_%m_%d')),None) is not None:
                        weekX = weekRangesIndex[str("date_"+thisData.strftime('%Y_%m_%d'))]
                        varX["data"][weekX]["tmd"] = varX["data"][weekX]["tmd"] + date["tmd"]
                        varX["data"][weekX]["bid_days"] = varX["data"][weekX]["bid_days"] + date["bid_days"]
                        varX["data"][weekX]["achieved_mandays"] = varX["data"][weekX]["achieved_mandays"] + date["achieved_mandays"]
                        varX["data"][weekX]["pending_mandays"] = varX["data"][weekX]["pending_mandays"] + date["pending_mandays"]
                rData.append(varX) 
            return Response(rData)
        else:
            return Response([])

class taskdaylogsFilter(APIView, apiRequestManager):
    select_related = ['task', 'artist', 'updated_by', 'task__shot', 'task__artist']
    model = TaskDayLogs
    def get(self, request, format=None):
        collectArguments = {"id": True, "task__id":True, "task__shot__id":True, "artist__id": True, "updated_date__range": "split" }
        return Response(
            self.read(
                request=request,
                model=self.model,
                select_related=self.select_related,
                collectArguments=collectArguments
            ))
    
class shotdaylogsFilter(APIView, apiRequestManager):
    select_related = ['shot', 'artist', 'updated_by']
    model = DayLogs
    def get(self, request, format=None):
        collectArguments = {"id": True, "shot__id":True, "artist__id": True, "updated_date__range": "split", "shot__location__id__in": "split","shot__location__name__in": "split", "shot__task_type__id__in": "split","shot__task_type__name__in": "split" }
        return Response(
            self.read(
                request=request,
                model=self.model,
                select_related=self.select_related,
                collectArguments=collectArguments
            ))
    
class leaves(APIView, apiRequestManager):
    select_related = ['employee', 'sessionFrom', 'sessionFrom']
    model =Leaves
    def get(self, request, format=None):
        collectArguments = {"id": True, "employee__id":True, "employee__id__in":"split", "targetDate__range": "split" }
        return Response(
            self.read(
                request=request,
                model=self.model,
                select_related=self.select_related,
                collectArguments=collectArguments
            ))
    
class EmployeeDailyStatisticsLite(APIView, apiRequestManager):
    model =EmployeeDailyStatistics
    def get(self, request, format=None):
        collectArguments = {"id": True, "employee__id":True, "employee__role__name__in": 'split', 'employee__employement_status__name':True, "employee__department__name__in":"split", "logDate__range": "split" }
        return Response(
            self.read(
                request=request,
                model=self.model,
                collectArguments=collectArguments
                ))

class alllocations(APIView, apiRequestManager):
    select_related = []
    model =Location
    def get(self, request, format=None):
        collectArguments = {"id": True, "name": True, "id__in":"split", "name__in":"split" }
        return Response(
            self.read(
                request=request,
                model=self.model,
                select_related=self.select_related,
                collectArguments=collectArguments
            ))

class attendance(APIView, apiRequestManager):
    select_related = ['employee']
    model = Attendance
    def get(self, request, format=None):
        collectArguments = {"id": True,"employee__id__in": "split","employee__id": True, "attendanceDate__range": "split"}
        return Response(
            self.read(
                request=request,
                model=self.model,
                select_related=self.select_related,
                collectArguments=collectArguments
            ))

class shots_history(APIView, apiRequestManager):
    select_related = []
    model = ShotsHistory
    def get(self, request, format=None):
        collectArguments = {"id": True, "target__id":True}
        return Response(
            self.read(
                request=request,
                model=self.model,
                select_related=self.select_related,
                collectArguments=collectArguments
            ))
    
class shotsDayLogs_history(APIView, apiRequestManager):
    select_related = []
    model = DayLogsHistory
    def get(self, request, format=None):
        collectArguments = {"id": True, "target__shot__id":True}
        return Response(
            self.read(
                request=request,
                model=self.model,
                select_related=self.select_related,
                collectArguments=collectArguments
            ))
    
class mytask_history(APIView, apiRequestManager):
    select_related = []
    model = MyTaskHistory
    def get(self, request, format=None):
        collectArguments = {"id": True, "target__shot__id":True, "target__id":True}
        return Response(
            self.read(
                request=request,
                model=self.model,
                select_related=self.select_related,
                collectArguments=collectArguments
            ))
    
class taskdaylogs_history(APIView, apiRequestManager):
    select_related = []
    model = TaskDayLogsHistory
    def get(self, request, format=None):
        collectArguments = {"id": True, "target__task__shot__id":True, "target__task__id":True, "target__id":True}
        return Response(
            self.read(
                request=request,
                model=self.model,
                select_related=self.select_related,
                collectArguments=collectArguments
            ))

class recordsCount(APIView, apiRequestManager):

    def get(self, request, format=None):
        target = request.query_params.get("target",None)
        if target=="clients":
            return Response({
                "count": Clients.objects.filter(status="IN PROGRESS").count()
                })
        elif target=="departments":
            return Response({
                "count": Task_Type.objects.all().count()
                })
        elif target=="all_shots":
            shotCodes = self.getDBData(model=ShotStatus, queryFilter={}, select_related=[ ], queryPerams=["id","code"])
            return Response({
                "count": Shots.objects.filter(status__code__in=[x['code'] for x in shotCodes if x['code'] not in ['OMT','HLD']],isSubShot=False).count()
                })
        elif target=="all_active_shots":
            shotCodes = self.getDBData(model=ShotStatus, queryFilter={}, select_related=[ ], queryPerams=["id","code"])
            return Response({
                "count": Shots.objects.filter(status__code__in=[x['code'] for x in shotCodes if x['code'] not in ['OMT','HLD','IAP','DTC','CAP']]).count()
                })
        elif target in ["HEAD OF DEPARTMENT","SUPERVISOR","TEAM LEAD","VFX ARTIST"]:
            return Response({
                 "count": Employee.objects.filter(role__name=target,employement_status__name="Active").count()
                })
        return Response({})



class versionIndexCount(APIView, apiRequestManager):

    def get(self, request, format=None):
        exitingVersion = list(ClientVersions.objects.values('version').annotate(Count('id')).order_by('version'))
        return Response({'count':int(''.join(filter(str.isdigit,exitingVersion[-1]['version']))) if len(exitingVersion) > 0 else 0})

class versionReports(APIView, apiRequestManager):

    def post(self, request, format=None):
        collectArguments = {"id": True, "shot__isSubShot":True, "modified_date__range":"split", "version__in":"split", "shot__sequence__project__client__id":True,"shot__sequence__project__id":True,"shot__task_type__id":True}
        # collectArguments = {"id": True,"shot__sequence__project__client__id":True }
        return Response(
            self.read(
                request = request,
                model = ClientVersions,
                collectArguments = collectArguments,
                # exclude={"shot__isSubShot":False},
                isGet=False
                ))
class clientReports(APIView, apiRequestManager):
    select_related = []
    model = ClientStatistics
    def get(self, request, format=None):
        collectArguments = {"id": True, "client__id":True, "client__name":True, "project__id":True, "project__name":True, "dep__id":True, "dep__name":True, }
        return Response(
            self.read(
                request=request,
                model=self.model,
                select_related=self.select_related,
                collectArguments=collectArguments
            ))
    

class sanitizeshotsandtakslogsApi(APIView, apiRequestManager):
    
    select_related = ['shot', 'sent_by', 'status', 'verified_by']
    model = QCVersions
    def get(self, request, format=None):
        shotid = self.request.query_params.get("shotId",None)
        if shotid is None:
            allShots = self.getDBData(model=Shots, queryFilter={}, select_related=[ ], queryPerams=["id","name"])
            return Response(allShots)
        else:
            allShots = self.getDBData(model=Shots, queryFilter={"id":shotid}, select_related=[ ], queryPerams=["id","bid_days"])
            r = []
            for x in allShots:
                shotLogs = list(DayLogs.objects.filter(shot__id=x["id"]).order_by('updated_date').values("id","percentage","day_percentage","consumed_man_day","updated_date"))
                lastLog = None
                shoUpdates = []
                totalPercentage = 0
                for log in shotLogs:
                    log["percentage"] = 0 if log["percentage"] < 0 else 100 if log["percentage"] > 100 else log["percentage"]
                    totalPercentage = totalPercentage + (log["percentage"] - (0 if lastLog is None else lastLog["percentage"]))
                    if totalPercentage > 100:
                        log["percentage"] = 100
                    day_percentage = log["percentage"] - (0 if lastLog is None else lastLog["percentage"])
                    updateLog = {
                        "percentage": log["percentage"],
                        "day_percentage": day_percentage,
                        "consumed_man_day": (x["bid_days"]/100)*day_percentage
                        }
                    lastLog = log
                    DayLogs.objects.filter(id=log["id"]).update(**updateLog.copy())
                    updateLog["updated_date"] = log["updated_date"]
                    shoUpdates.append(updateLog)

                allTasks = self.getDBData(model=MyTask, queryFilter={"shot__id":x["id"]}, select_related=[], queryPerams=["id","assigned_bids"])
                tskLogs = []
                for task in allTasks:
                    taskLgs = list(TaskDayLogs.objects.filter(task__id=task["id"]).order_by('updated_date').values("id","percentage","day_percentage","consumed_man_day","updated_date"))
                    lastLog = None
                    taskUpdates = []
                    totalPercentage = 0
                    for log in taskLgs:
                        log["percentage"] = 0 if log["percentage"] < 0 else 100 if log["percentage"] > 100 else log["percentage"]
                        totalPercentage = totalPercentage + (log["percentage"] - (0 if lastLog is None else lastLog["percentage"]))
                        if totalPercentage > 100:
                            log["percentage"] = 100
                        day_percentage = log["percentage"] - (0 if lastLog is None else lastLog["percentage"])
                        updateLog = {
                            "percentage": log["percentage"],
                            "day_percentage": day_percentage,
                            "consumed_man_day": (task["assigned_bids"]/100)*day_percentage
                            }
                        lastLog = log
                        TaskDayLogs.objects.filter(id=log["id"]).update(**updateLog.copy())
                        updateLog["updated_date"] = log["updated_date"]
                        taskUpdates.append(updateLog)
                    tskLogs.append({
                        "id": task["id"],
                        "assigned_bids": task["assigned_bids"],
                        "logs": taskUpdates
                        })
                r.append({
                        "shotId": x["id"],
                        "bid_days": x["bid_days"],
                        "logs": shoUpdates,
                        "taks": tskLogs
                        })
            return Response(r)
        
class testApi(APIView, apiRequestManager):
    
    select_related = ['shot', 'sent_by', 'status', 'verified_by']
    model = QCVersions
    def get(self, request, format=None):
        collectArguments = {"id": True, "sent_by__id": True, "verified_by__role__name": True, }
        _rd = self.read(
                request=request,
                model=self.model,
                select_related=self.select_related,
                collectArguments=collectArguments
            )
        _emps = [x['verified_by'] for x in _rd ]
        emps = self.getDBData(model=Employee, queryFilter={"pk__in": _emps}, select_related=['profile', 'department', 'role'], queryPerams=['id','profile__id', 'profile__username', 'employee_id', 'first_name', 'last_name', 'fullName', 'department__id', 'department__name', 'role__id', 'role__name'])
        _tx = []
        _epr = {}
        for x in emps:
            if x["id"] not in _tx:
                _tx.append(x["id"])
                _epr['id_'+str(x["id"])] = x
                _epr['id_'+str(x["id"])]['TL'] = None
                _epr['id_'+str(x["id"])]['SP'] = None
        team_leads = self.getDBData(model=EmployeeRoleBinding, queryFilter={"role__name":'TEAM LEAD',"employee__id__in":_tx}, select_related=[], queryPerams=["id", "employee__id", "bindWith__id", "bindWith__fullName"])
        _txr = []
        _tl = []
        for x in team_leads:
            _epr['id_'+str(x["employee"]["id"])]['TL'] = x["bindWith"]
            if x["bindWith"]["id"] not in _txr:
                _txr.append(x["bindWith"]["id"])
                _tl.append(x["bindWith"])

        team_leadx = self.getDBData(model=EmployeeRoleBinding, queryFilter={"role__name":'SUPERVISOR',"employee__id__in":_tx}, select_related=[], queryPerams=["id", "employee__id", "bindWith__id", "bindWith__fullName"])
        _txr = []
        _sp = []
        for x in team_leadx:
            _epr['id_'+str(x["employee"]["id"])]['SP'] = x["bindWith"]
            if x["bindWith"]["id"] not in _txr:
                _txr.append(x["bindWith"]["id"])
                _sp.append(x["bindWith"])

        return Response({"TL": _tl,"SP": _sp, "EMP":list(_epr.values()), "OFX":[ x['employee_id'] for x in list(_epr.values())]})

from ofx_statistics.models import EmployeeDailyStatistics

class testApi2(APIView, apiRequestManager):

    def get(self, request, format=None):
        # a = list(EmployeeRoleBinding.objects.filter(employee__employement_status__name='Deactive').values('id','employee__employee_id'))
        # EmployeeRoleBinding.objects.filter(employee__employement_status__name='Deactive').delete() 
        # allVFARTISTS = self.getDBData(model=Employee, queryFilter={'role__name':"VFX ARTIST"}, select_related=[ ], queryPerams=["id","profile__id",'profile__date_joined'])
        # for empdata in allVFARTISTS:
        #     if empdata["profile"] is not None and empdata["profile"]["date_joined"] is not None:
        #         doj = datetime.datetime.strptime(empdata["profile"]["date_joined"].split(' ')[0],'%Y-%m-%d')
        #         # rd = self.getDBData(model=EmployeeDailyStatistics, queryFilter={'employee__id':empdata["id"],'logDate__lt':doj.strftime('%Y-%m-%d')}, select_related=[ ], queryPerams=["id","logDate"])
        #         # # rd = EmployeeDailyStatistics.objects.filter(logDate__lt=doj.strftime('%Y-%m-%d')).values("id","logDate")
        #         # print(rd)
        #         EmployeeDailyStatistics.objects.filter(employee__id=empdata["id"],logDate__lt=doj.strftime('%Y-%m-%d')).delete()
        return Response([] )

class testApi3(APIView, apiRequestManager):

    def get(self, request, format=None):
        leads = ['SUPERVISOR','TEAM LEAD','HEAD OF DEPARTMENT']
        apiRequestManagers = apiRequestManager()
        employeeRoleBinding_data = apiRequestManagers.getDBData(model=EmployeeRoleBinding, queryFilter={"role__name__in": leads,'employee__role__name':'VFX ARTIST', 'employee__employement_status__name':'Active', 'bindWith__employement_status__name':'Active' }, queryPerams=['id','employee__id','employee__employee_id','employee__fullName','department__id','department__name','employee__grade__id','employee__grade__name','employee__grade__a_man_day','role__id','role__name','bindWith__id','bindWith__employee_id','bindWith__fullName','bindWith__role__id','bindWith__role__name'])
        _rdata = {}
        for emp in employeeRoleBinding_data:
            key = 'id_{id}'.format(id=emp["employee"]["id"])
            if _rdata.get(key,None) is None:
                _rdata[key] = {
                    "id": emp["employee"]["id"],
                    "employee_id": emp["employee"]["employee_id"],
                    "fullName": emp["employee"]["fullName"],
                    "grade": emp["employee"]["grade"],
                    "department": emp["department"],
                    }
                for led in leads:
                    _rdata[key][apiRequestManagers.makeKey(led)] = None
            if emp["bindWith"] is not None and apiRequestManagers.makeKey(emp["role"]["name"])==apiRequestManagers.makeKey(emp["bindWith"]["role"]["name"]):
                _rdata[key][apiRequestManagers.makeKey(emp["role"]["name"])] = json.loads(json.dumps(emp["bindWith"]))


        # a = list(EmployeeRoleBinding.objects.filter(employee__employement_status__name='Deactive').values('id','employee__employee_id'))
        # EmployeeRoleBinding.objects.filter(employee__employement_status__name='Deactive').delete() 
        # allVFARTISTS = self.getDBData(model=Employee, queryFilter={'role__name':"VFX ARTIST"}, select_related=[ ], queryPerams=["id","profile__id",'profile__date_joined'])
        # for empdata in allVFARTISTS:
        #     if empdata["profile"] is not None and empdata["profile"]["date_joined"] is not None:
        #         doj = datetime.datetime.strptime(empdata["profile"]["date_joined"].split(' ')[0],'%Y-%m-%d')
        #         # rd = self.getDBData(model=EmployeeDailyStatistics, queryFilter={'employee__id':empdata["id"],'logDate__lt':doj.strftime('%Y-%m-%d')}, select_related=[ ], queryPerams=["id","logDate"])
        #         # # rd = EmployeeDailyStatistics.objects.filter(logDate__lt=doj.strftime('%Y-%m-%d')).values("id","logDate")
        #         # print(rd)
        #         EmployeeDailyStatistics.objects.filter(employee__id=empdata["id"],logDate__lt=doj.strftime('%Y-%m-%d')).delete()
        return Response(_rdata)
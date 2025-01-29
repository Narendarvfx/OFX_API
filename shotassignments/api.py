#  Copyright (c) 2023.
#  Designed & Developed by Narendar Reddy G, OscarFX Private Limited
#  All rights reserved.
import json
from OFX_API import  apiRequestManager
from hrm.models import Role, Location, Department, Employee
from production.models import Task_Type, ShotStatus
from rest_framework.response import Response
from rest_framework.views import APIView
from shotassignments.models import ShotAssignmentsOrder, AssignmentsRoles

class shotAssignmentsOrders(APIView, apiRequestManager):

    model = ShotAssignmentsOrder

    def get(self, request, format=None):
        collectArguments = {"id": True, 'id__in':'split', 'department__id': True, 'department__id__in':'split', 'department__name': True, 'department__id__name':'split', 'location__id': True, 'location__id__in':'split', 'location__name': True, 'location__name__in':'split', 'shotStatus__id': True, 'shotStatus__id__in':'split', 'shotStatus__code': True, 'shotStatus__code__in':'split','isSubShot':True}
        return Response(
            self.read(
                request=request,
                model=self.model,
                collectArguments=collectArguments
            ))
class setshotAssignmentsOrders(APIView, apiRequestManager):

    model = ShotAssignmentsOrder

    def post(self, request):
        postData = request.data
        location = postData['location']
        department = postData['department']
        isSubShot = postData['isSubShot']
        rqData = json.loads(postData['data'])
        oldQ = {
            "department__name":department,
            "isSubShot": isSubShot
            }
        if location is None:
            oldQ['location'] = None
        else:
            oldQ['location__name'] = location
        existingData = {x['id']:True for x in json.loads(json.dumps(self.getDBData(model=self.model, queryFilter=oldQ, select_related=[], queryPerams=["id"])))}
        _rqData = {}
        # return Response(rqData)
        for k,v in rqData.items():
            _rqData[k] = {
                'allowedSteps': {},
                'authorizedRoles': {},
                }
            for r1 in v['allowedSteps']:
                rqXY = {
                    'roleIndex': r1['roleIndex'],
                    'shotStatus__code': r1['shotStatus']
                    }
                if r1['employee'] is None:
                    rqXY['location__name'] = r1['location']
                    rqXY['role__name'] = r1['role']
                    rqXY['department__name'] = r1['department']
                else:
                    rqXY['employee__id'] = r1['employee']
                inRole = self.getDBData(model=AssignmentsRoles, queryFilter=rqXY, select_related=[], queryPerams=["id",'location__name','role__name','department__name','employee__id'])
                if len(inRole) == 0:
                    newdata = {
                        'roleIndex': r1['roleIndex'],
                        'shotStatus': ShotStatus.objects.get(code=r1['shotStatus'])
                        }
                    if r1['employee'] is None:
                        newdata['location'] = Location.objects.get(name=r1['location'])
                        newdata['role'] = Role.objects.get(name=r1['role'])
                        newdata['department'] = Department.objects.get(name=r1['department'])
                    else:
                        newdata['employee'] = Employee.objects.get(pk=r1['employee'])
                    self.insert(model=AssignmentsRoles,data=newdata)
                    inRole = self.getDBData(model=AssignmentsRoles, queryFilter=rqXY, select_related=[], queryPerams=["id",'location__name','role__name','department__name','employee__id'])
                rKey = 'emp_{emp}'.format(emp=inRole[0]['employee']['id']) if inRole[0]['employee'] is not None else self.makeKey('dep_{loc}_{dep}_{role}'.format(loc=inRole[0]['location']['name'],dep=inRole[0]['department']['name'],role=inRole[0]['role']['name']))
                _rqData[k]['allowedSteps'][rKey] = inRole[0]['id']
        for k,v in rqData.items():
            for r1 in v['authorizedRoles']:
                rKey = 'emp_{emp}'.format(emp=r1['employee']) if r1['employee'] is not None else self.makeKey('dep_{loc}_{dep}_{role}'.format(loc=r1['location'],dep=r1['department'],role=r1['role']))
                if _rqData[k]['allowedSteps'].get(rKey,None) is not None:
                    _rqData[k]['authorizedRoles'][rKey] = _rqData[k]['allowedSteps'][rKey]
                else:
                    rqXY = {}
                    if r1['employee'] is None:
                        rqXY['location__name'] = r1['location']
                        rqXY['role__name'] = r1['role']
                        rqXY['department__name'] = r1['department']
                    else:
                        rqXY['employee__id'] = r1['employee']
                    inRole = self.getDBData(model=AssignmentsRoles, queryFilter=rqXY, select_related=[], queryPerams=["id",'location__name','role__name','department__name','employee__id'])
                    if len(inRole) == 0:
                        newdata = {}
                        if r1['employee'] is None:
                            newdata['location'] = Location.objects.get(name=r1['location'])
                            newdata['role'] = Role.objects.get(name=r1['role'])
                            newdata['department'] = Department.objects.get(name=r1['department'])
                        else:
                            newdata['employee'] = Employee.objects.get(pk=r1['employee'])
                        self.insert(model=AssignmentsRoles,data=newdata)
                        inRole = self.getDBData(model=AssignmentsRoles, queryFilter=rqXY, select_related=[], queryPerams=["id",'location__name','role__name','department__name','employee__id'])
                    rKey = 'emp_{emp}'.format(emp=inRole[0]['employee']['id']) if inRole[0]['employee'] is not None else self.makeKey('dep_{loc}_{dep}_{role}'.format(loc=inRole[0]['location']['name'],dep=inRole[0]['department']['name'],role=inRole[0]['role']['name']))
                    _rqData[k]['authorizedRoles'][rKey] = inRole[0]['id']  
        inExisLog = []
        for k,v in rqData.items():
            rQx = {
                "department__name": v['department'],
                "isSubShot": v['isSubShot'],
                "shotStatus__code": v['shotStatus']
                }
            if v['location'] is None:
                rQx['location'] = None
            else:
                rQx['location__name'] = v['location']
            inLine = self.getDBData(model=ShotAssignmentsOrder, queryFilter=rQx, select_related=[], queryPerams=["id","authorizedRoles__id","allowedSteps__id"])
            if len(inLine) > 0:
                inExisLog.append(inLine[0]['id'])
            else:
                _Nex = {
                    "department": Task_Type.objects.get(name=v['department']),
                    "isSubShot": v['isSubShot'],
                    "shotStatus": ShotStatus.objects.get(code=v['shotStatus'])
                    }
                if v['location'] is not None:
                    _Nex['location'] = Location.objects.get(name=v['location'])
                self.insert(model=ShotAssignmentsOrder,data=_Nex)
                inLine = self.getDBData(model=ShotAssignmentsOrder, queryFilter=rQx, select_related=[], queryPerams=["id","authorizedRoles__id","allowedSteps__id"])
                inExisLog.append(inLine[0]['id'])
            
            shotsObj = ShotAssignmentsOrder.objects.get(id=inLine[0]['id'])
            
            for ep in inLine[0]["authorizedRoles"]:
                shotsObj.authorizedRoles.remove(AssignmentsRoles.objects.get(pk=ep['id']))
            for r1 in v['authorizedRoles']:
                rKey = 'emp_{emp}'.format(emp=r1['employee']) if r1['employee'] is not None else self.makeKey('dep_{loc}_{dep}_{role}'.format(loc=r1['location'],dep=r1['department'],role=r1['role']))
                shotsObj.authorizedRoles.add(AssignmentsRoles.objects.get(pk=_rqData[k]['authorizedRoles'][rKey]))
            
            for ep in inLine[0]["allowedSteps"]:
                shotsObj.allowedSteps.remove(AssignmentsRoles.objects.get(pk=ep['id']))
            for r1 in v['allowedSteps']:
                rKey = 'emp_{emp}'.format(emp=r1['employee']) if r1['employee'] is not None else self.makeKey('dep_{loc}_{dep}_{role}'.format(loc=r1['location'],dep=r1['department'],role=r1['role']))
                shotsObj.allowedSteps.add(AssignmentsRoles.objects.get(pk=_rqData[k]['allowedSteps'][rKey]))
            self.update(query={'id':inLine[0]['id']},model=ShotAssignmentsOrder,data={
                "isBeforeArtist": v['isBeforeArtist'],
                "isSubShot": v['isSubShot'],
                "statusIndex": v['statusIndex'],
                "rejectCase": ShotStatus.objects.get(code=v['rejectCase']) if v['rejectCase'] is not None else None,
                "acceptCase": ShotStatus.objects.get(code=v['acceptCase']) if v['acceptCase'] is not None else None
                })
        for xAR,yAR in existingData.items():
            if xAR not in inExisLog:
                ShotAssignmentsOrder.objects.get(pk=xAR).delete()
        inUsedRoles = []
        for xAR in json.loads(json.dumps(self.getDBData(model=ShotAssignmentsOrder, queryFilter={}, select_related=[], queryPerams=["id", "authorizedRoles__id","allowedSteps__id"]))):
            for yAR in xAR['authorizedRoles']:
                if yAR['id'] not in inUsedRoles:
                    inUsedRoles.append(yAR['id'])
            for yAR in xAR['allowedSteps']:
                if yAR['id'] not in inUsedRoles:
                    inUsedRoles.append(yAR['id'])
        for xAR in json.loads(json.dumps(self.getDBData(model=AssignmentsRoles, queryFilter={}, select_related=[], queryPerams=["id"]))):
            if xAR['id'] not in inUsedRoles:
                AssignmentsRoles.objects.get(pk=xAR['id']).delete()
        
        return Response(rqData)
from django.db.models import Q
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from hrm.models import Employee, ProductionTeam, Role_Permissions
from hrm.serializers import EmployeeSerializer, TeamSerializer, PermissionSerializer, EmployeePutSerializer


class EmployeeDetail(APIView):
    """
    This is for edit employee detail
    """
    def get(self, request, profile_id, format=None):
        employee = Employee.objects.select_related('department','grade','role','employement_status','team_lead','supervisor').get(profile=profile_id)
        serializer = EmployeeSerializer(employee, context={"request":request})
        return Response(serializer.data)

    def put(self, request, profile_id, format=None):
        permission_classes = (IsAuthenticated,)  # permission classes
        employee = Employee.objects.get(profile=profile_id)

        serializer = EmployeePutSerializer(employee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AllEmployeeDetail(APIView):
    """
    This is for edit employee detail
    """
    def get(self, request, format=None):
        employment_status = request.GET.get('status')
        department = request.GET.get('dept')
        role = request.GET.get('role')
        if employment_status is not None:
            employee = Employee.objects.select_related('department', 'role', 'employement_status', 'grade').filter(employement_status__name=employment_status)
        elif department and role is not None:
            employee = Employee.objects.select_related('department', 'role', 'employement_status', 'grade').filter(
                department__name=department, role__name=role, employement_status__name="Active")
        else:
            employee = Employee.objects.select_related('department', 'role', 'employement_status', 'grade')
        serializer = EmployeeSerializer(employee, many=True, context={"request":request})
        return Response(serializer.data)

class AllTeams(APIView):

    def get(self, request, format=None):
        team= ProductionTeam.objects.all()
        serializer = TeamSerializer(team, many=True, context={"request":request})
        return Response(serializer.data)

class TeamById(APIView):

    def get(self, request,id, format=None):
        team= ProductionTeam.objects.get(id=id)
        serializer = TeamSerializer(team, context={"request":request})
        return Response(serializer.data)

class AllPermissions(APIView):

    def get(self, request, format=None):
        permission= Role_Permissions.objects.select_related('role').all()
        serializer = PermissionSerializer(permission, many=True, context={"request":request})
        return Response(serializer.data)

class RolePermissions(APIView):
    """
    This is for edit employee detail
    """
    def get(self, request, role_id, format=None):
        rpermission = Role_Permissions.objects.select_related('role').get(role=role_id)
        serializer = PermissionSerializer(rpermission, context={"request":request})
        return Response(serializer.data)
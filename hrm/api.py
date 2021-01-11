from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from hrm.models import Employee, ProductionTeam
from hrm.serializers import EmployeeSerializer, TeamSerializer


class EmployeeDetail(APIView):
    """
    This is for edit employee detail
    """

    def get(self, request, profile_id, format=None):
        employee = Employee.objects.select_related('department','grade','role','employement_status').get(profile=profile_id)
        serializer = EmployeeSerializer(employee, context={"request":request})
        return Response(serializer.data)

    def put(self, request, profile_id, format=None):
        employee = Employee.objects.get(profile=profile_id)

        serializer = EmployeeSerializer(employee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AllEmployeeDetail(APIView):
    """
    This is for edit employee detail
    """

    def get(self, request, format=None):
        employee = Employee.objects.select_related('department','role','employement_status','grade').filter(Q(department__name="PAINT") | Q(department__name="ROTO") | Q(department__name="MATCH MOVE") , employement_status__name='Active')
        serializer = EmployeeSerializer(employee, many=True, context={"request":request})
        return Response(serializer.data)

class AllTeams(APIView):

    def get(self, request, format=None):
        team= ProductionTeam.objects.all()
        serializer = TeamSerializer(team, many=True, context={"request":request})
        return Response(serializer.data)
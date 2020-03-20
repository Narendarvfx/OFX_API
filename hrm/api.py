from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from hrm.models import Employee
from hrm.serializers import EmployeeSerializer


class EmployeeDetail(APIView):
    """
    This is for edit employee detail
    """

    def get(self, request, profile_id, format=None):
        employee = Employee.objects.get(profile=profile_id)
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data)

    def put(self, request, profile_id, format=None):
        employee = Employee.objects.get(profile=profile_id)

        serializer = EmployeeSerializer(employee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#  Copyright (c) 2023.
#  Designed & Developed by Narendar Reddy G, OscarFX Private Limited
#  All rights reserved.

from rest_framework import serializers

from hrm.models import Employee
from ofx_statistics.models import EmployeeDailyStatistics

class EmployeeCompactSerializer(serializers.ModelSerializer):

    class Meta:
        model = Employee
        fields = ('id','fullName','employee_id', 'department','role','grade')

class EmployeeDailyStatisticserializer(serializers.ModelSerializer):
    employee = EmployeeCompactSerializer(read_only=True)
    class Meta:
        model = EmployeeDailyStatistics
        fields = '__all__'

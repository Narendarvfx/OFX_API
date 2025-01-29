#  Copyright (c) 2023.
#  Designed & Developed by Narendar Reddy G, OscarFX Private Limited
#  All rights reserved.

from rest_framework import serializers

from hrm.models import Employee, Role
from hrm.serializers import EmployeeCompactSerializer
from ofx_statistics.models import EmployeeDailyStatistics, TLDailyStatistics, LeadDailyStatistics, ClientStatistics
from production.models import Task_Type


class EmployeeDailyStatisticserializer(serializers.ModelSerializer):
    employee = serializers.SlugRelatedField(queryset=Employee.objects.all(), slug_field='employee_id', required=False)
    class Meta:
        model = EmployeeDailyStatistics
        fields = '__all__'


class TLDailyStatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TLDailyStatistics
        fields = '__all__'

class LeadDailyStatisticsSerializer(serializers.ModelSerializer):
    role = serializers.SlugRelatedField(queryset=Role.objects.all(), slug_field='name', required=False)
    class Meta:
        model = LeadDailyStatistics
        fields = '__all__'

class ClientStatisticsSerializer(serializers.ModelSerializer):

    dep = serializers.SlugRelatedField(queryset=Task_Type.objects.all(), slug_field='name', required=False)
    class Meta:
        model = ClientStatistics
        fields = '__all__'
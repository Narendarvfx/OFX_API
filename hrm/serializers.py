from rest_framework import serializers

from hrm.models import Department, Location, Role, Designation, Level, EmployementStatus, Employee


class EmployeeSerializer(serializers.ModelSerializer):
    department = serializers.SlugRelatedField(queryset=Department.objects.all(), slug_field='name', required=False)
    designation = serializers.SlugRelatedField(queryset=Designation.objects.all(), slug_field='name', required=False)
    location = serializers.SlugRelatedField(queryset=Location.objects.all(), slug_field='name', required=False)
    role = serializers.SlugRelatedField(queryset=Role.objects.all(), slug_field='name', required=False)
    level = serializers.SlugRelatedField(queryset=Level.objects.all(), slug_field='name', required=False)
    employement_status = serializers.SlugRelatedField(queryset=EmployementStatus.objects.all(), slug_field='name',
                                                     required=False)

    class Meta:
        model = Employee
        fields = '__all__'
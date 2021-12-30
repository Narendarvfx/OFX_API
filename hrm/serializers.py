from rest_framework import serializers

from hrm.models import Department, Role, Grade, EmployementStatus, Employee, ProductionTeam, Role_Permissions
from profiles.models import Profile


class GradeCompactSerializer(serializers.ModelSerializer):

    class Meta:
        model = Grade
        fields = '__all__'

class EmployeeCompactSerializer(serializers.ModelSerializer):

    class Meta:
        model = Employee
        fields = ('id','fullName')

class EmployeeSerializer(serializers.ModelSerializer):

    department = serializers.SlugRelatedField(queryset=Department.objects.all(), slug_field='name', required=False)
    role = serializers.SlugRelatedField(queryset=Role.objects.all(), slug_field='name', required=False)
    grade = serializers.SlugRelatedField(queryset=Grade.objects.all(), slug_field='name',
                                                     required=False)
    employement_status = serializers.SlugRelatedField(queryset=EmployementStatus.objects.all(), slug_field='name',
                                                     required=False)
    photo = serializers.ImageField(max_length=None, use_url=True, allow_null=True, required=False)
    team_lead = EmployeeCompactSerializer(read_only=True)
    supervisor = EmployeeCompactSerializer(read_only=True)

    class Meta:
        model = Employee
        fields = '__all__'

class EmployeePutSerializer(serializers.ModelSerializer):

    department = serializers.SlugRelatedField(queryset=Department.objects.all(), slug_field='name', required=False)
    role = serializers.SlugRelatedField(queryset=Role.objects.all(), slug_field='name', required=False)
    grade = serializers.SlugRelatedField(queryset=Grade.objects.all(), slug_field='name',
                                                     required=False)
    employement_status = serializers.SlugRelatedField(queryset=EmployementStatus.objects.all(), slug_field='name',
                                                     required=False)
    photo = serializers.ImageField(max_length=None, use_url=True, allow_null=True, required=False)
    # team_lead = EmployeeCompactSerializer(read_only=True)
    # supervisor = EmployeeCompactSerializer(read_only=True)

    class Meta:
        model = Employee
        fields = '__all__'

class TeamSerializer(serializers.ModelSerializer):


    class Meta:
        model = ProductionTeam
        fields = '__all__'

class PermissionSerializer(serializers.ModelSerializer):


    class Meta:
        model = Role_Permissions
        fields = '__all__'
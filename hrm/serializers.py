#  Copyright (c) 2023.
#  Designed & Developed by Narendar Reddy G, OscarFX Private Limited
#  All rights reserved.
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from hrm.models import Department, Role, Grade, EmployementStatus, Employee, ProductionTeam, Permissions, Location, \
    EmployeeGroups, Leaves, Attendance, OrganizationHolidayTypes, OrganizationHolidays, DepartmentWorkingDays, \
    EmployeeWorkingDays, OrganizationWorkingDays, WorkingDayTypes, EmployeeRoleBinding, RoleRelationshipBinding


class GradeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Grade
        fields = '__all__'

class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Location
        fields = '__all__'

class DepartmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Department
        fields = ('id','name','color')

class EmployeeCompactSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(read_only=True)
    class Meta:
        model = Employee
        fields = ('id','fullName','apikey','photo','employee_id', 'department')

class EmployeeGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = EmployeeGroups
        fields = '__all__'

class EmployeeGroupCompactSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False)
    groupkey = serializers.CharField(required=False)
    class Meta:
        model= EmployeeGroups
        fields = '__all__'
        depth = 1

class PermissionSerializer(serializers.ModelSerializer):
    permission_key = serializers.CharField(required=False)
    name = serializers.CharField(required=False)

    class Meta:
        model = Permissions
        fields = '__all__'

class RoleSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False)
    permissions = PermissionSerializer(required=False, many=True)

    class Meta:
        model = Role
        fields = '__all__'

class LocationSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False)
    permissions = PermissionSerializer(required=False, many=True)

    class Meta:
        model = Location
        fields = '__all__'

class EmployeePostSerializer(serializers.ModelSerializer):
    department = serializers.SlugRelatedField(queryset=Department.objects.all(), slug_field='name', required=False)
    role = serializers.SlugRelatedField(queryset=Role.objects.all(), slug_field='name', required=False)
    # role = RoleSerializer(read_only=True)
    grade = serializers.SlugRelatedField(queryset=Grade.objects.all(), slug_field='name',
                                                     required=False)
    employement_status = serializers.SlugRelatedField(queryset=EmployementStatus.objects.all(), slug_field='name',
                                                     required=False)
    location = serializers.SlugRelatedField(queryset=Location.objects.all(), slug_field='name',
                                                     required=False)
    photo = serializers.ImageField(max_length=None, use_url=True, allow_null=True, required=False)
    team_lead = EmployeeCompactSerializer(read_only=True)
    supervisor = EmployeeCompactSerializer(read_only=True)
    # employee_groups = serializers.PrimaryKeyRelatedField(queryset=EmployeeGroups.objects.all(), many=True)

    employee_groups = EmployeeGroupCompactSerializer(read_only=True, many=True)
    # profile = UserProfileSerializer(read_only=True)
    # employee_groups = serializers.SlugRelatedField(
    #     many=True,
    #     read_only=True,
    #     slug_field='groupkey'
    # )

    class Meta:
        model = Employee
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    date_joined = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%S.%f')
    groups = serializers.SlugRelatedField(many=True, read_only=True, slug_field="name")
    class Meta:
        model = User
        fields = '__all__'

    # def create(self, validated_data):
    #     user = super(UserSerializer, self).create(validated_data)
    #     user.set_password(validated_data['password'])
    #     user.save()
    #     return user

class UserProfileSerializer(serializers.ModelSerializer):
    # user = UserSerializer(read_only=True)
    # password_changed = serializers.BooleanField(read_only=True)

    class Meta:
        model = User
        fields = '__all__'

class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    def validate_new_password(self, value):
        validate_password(value)
        return value

class EmployeeSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='fullName')
    department = serializers.SlugRelatedField(queryset=Department.objects.all(), slug_field='name', required=False)
    role = serializers.SlugRelatedField(queryset=Role.objects.all(), slug_field='name', required=False)
    # role = RoleSerializer(read_only=True)
    grade = serializers.SlugRelatedField(queryset=Grade.objects.all(), slug_field='name',
                                                     required=False)
    employement_status = serializers.SlugRelatedField(queryset=EmployementStatus.objects.all(), slug_field='name',
                                                     required=False)
    location = serializers.SlugRelatedField(queryset=Location.objects.all(), slug_field='name',
                                                     required=False)
    photo = serializers.ImageField(max_length=None, use_url=True, allow_null=True, required=False)
    team_lead = EmployeeCompactSerializer(read_only=True)
    supervisor = EmployeeCompactSerializer(read_only=True)
    # employee_groups = serializers.PrimaryKeyRelatedField(queryset=EmployeeGroups.objects.all(), many=True)

    employee_groups = EmployeeGroupCompactSerializer(read_only=True, many=True)
    permissions = PermissionSerializer(required=False, many=True)
    profile = UserSerializer(read_only=True)
    # employee_groups = serializers.SlugRelatedField(
    #     many=True,
    #     read_only=True,
    #     slug_field='groupkey'
    # )

    class Meta:
        model = Employee
        fields = '__all__'

class EmployeeRoleBindingSerializer(serializers.ModelSerializer):
    # bindWith = EmployeeSerializer(read_only=True)
    # department = DepartmentSerializer(read_only=True)
    # role = RoleSerializer(read_only=True)
    department = serializers.SlugRelatedField(queryset=Department.objects.all(), slug_field='name', required=False)
    role = serializers.SlugRelatedField(queryset=Role.objects.all(), slug_field='name', required=False)
    class Meta:
        model = EmployeeRoleBinding
        fields = '__all__'

class MyProfileSerializer(serializers.ModelSerializer):
    department = serializers.SlugRelatedField(queryset=Department.objects.all(), slug_field='name', required=False)
    # role = serializers.SlugRelatedField(queryset=Role.objects.all(), slug_field='name', required=False)
    role = RoleSerializer(read_only=True)
    grade = serializers.SlugRelatedField(queryset=Grade.objects.all(), slug_field='name',
                                                     required=False)
    employement_status = serializers.SlugRelatedField(queryset=EmployementStatus.objects.all(), slug_field='name',
                                                     required=False)
    photo = serializers.ImageField(max_length=None, use_url=True, allow_null=True, required=False)
    team_lead = EmployeeCompactSerializer(read_only=True)
    supervisor = EmployeeCompactSerializer(read_only=True)
    # employee_groups = serializers.PrimaryKeyRelatedField(queryset=EmployeeGroups.objects.all(), many=True)

    employee_groups = EmployeeGroupCompactSerializer(read_only=True, many=True)
    profile = UserProfileSerializer(read_only=True)
    # employee_groups = serializers.SlugRelatedField(
    #     many=True,
    #     read_only=True,
    #     slug_field='groupkey'
    # )

    class Meta:
        model = Employee
        fields = '__all__'
class LeavesSerializer(serializers.ModelSerializer):
    employee = serializers.SlugRelatedField(queryset=Employee.objects.all(), slug_field='employee_id', required=False)
    sessionFrom = serializers.SlugRelatedField(queryset=WorkingDayTypes.objects.all(), slug_field='sessionType', required=False)
    sessionTo = serializers.SlugRelatedField(queryset=WorkingDayTypes.objects.all(), slug_field='sessionType', required=False)
    class Meta:
        model = Leaves
        fields = '__all__'

class AttendanceSerializer(serializers.ModelSerializer):
    employee = serializers.SlugRelatedField(queryset=Employee.objects.all(), slug_field='employee_id', required=False)

    class Meta:
        model = Attendance
        fields = '__all__'

class OrganizationWorkingDaysSerializer(serializers.ModelSerializer):
    location = serializers.SlugRelatedField(queryset=Location.objects.all(), slug_field='name', required=False)
    # location = LocationSerializer(read_only=True)
    class Meta:
        model = OrganizationWorkingDays
        fields = ('name','code','isWorkingDay','workingHours','location')

class RoleRelationshipBindingSerializer(serializers.ModelSerializer):
    department = serializers.SlugRelatedField(queryset=Department.objects.all(), slug_field='name', required=False)
    role = serializers.SlugRelatedField(queryset=Role.objects.all(), slug_field='name', required=False)
    bindWithEmployee = EmployeeCompactSerializer(read_only=True)
    bindWithDepartment = DepartmentSerializer(read_only=True)
    bindWithRole = RoleSerializer(read_only=True)
    permissions = PermissionSerializer(required=False, many=True)
    class Meta:
        model = RoleRelationshipBinding
        fields = '__all__'

class OrganizationHolidayTypesSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrganizationHolidayTypes
        fields = '__all__'

class WorkingDayTypesSerializer(serializers.ModelSerializer):

    class Meta:
        model = WorkingDayTypes
        fields = '__all__'

class OrganizationHolidaysSerializer(serializers.ModelSerializer):
    location = serializers.SlugRelatedField(queryset=Location.objects.all(), slug_field='name', required=False)
    # location = LocationSerializer(read_only=True)
    createdBy = serializers.SlugRelatedField(queryset=Employee.objects.all(), slug_field='fullName', required=False)
    updatedBy = serializers.SlugRelatedField(queryset=Employee.objects.all(), slug_field='fullName', required=False)
    type = serializers.SlugRelatedField(queryset=OrganizationHolidayTypes.objects.all(), slug_field='name', required=False)
    sessionType = serializers.SlugRelatedField(queryset=WorkingDayTypes.objects.all(), slug_field='sessionType',
                                               required=False)

    class Meta:
        model = OrganizationHolidays
        fields = '__all__'
class OrganizationHolidaysPostSerializer(serializers.ModelSerializer):
    location = serializers.SlugRelatedField(queryset=Location.objects.all(), slug_field='name', required=False)
    # location = LocationSerializer(read_only=True)
    # createdBy = serializers.SlugRelatedField(queryset=Employee.objects.all(), slug_field='fullName', required=False)
    # updatedBy = serializers.SlugRelatedField(queryset=Employee.objects.all(), slug_field='fullName', required=False)
    # type = serializers.SlugRelatedField(queryset=OrganizationHolidayTypes.objects.all(), slug_field='name', required=False)

    class Meta:
        model = OrganizationHolidays
        fields = '__all__'

class EmpWorkingDaysSerializer(serializers.ModelSerializer):
    location = serializers.SlugRelatedField(queryset=Location.objects.all(), slug_field='name', required=False)
    # location = LocationSerializer(read_only=True)
    assignedBy = serializers.SlugRelatedField(queryset=Employee.objects.all(), slug_field='fullName', required=False)
    updatedBy = serializers.SlugRelatedField(queryset=Employee.objects.all(), slug_field='fullName', required=False)
    sessionType = serializers.SlugRelatedField(queryset=WorkingDayTypes.objects.all(), slug_field='sessionType',
                                               required=False)
    employee = EmployeeCompactSerializer(read_only=True)

    class Meta:
        model = EmployeeWorkingDays
        fields = '__all__'

class EmpWorkingDaysPostSerializer(serializers.ModelSerializer):
    location = serializers.SlugRelatedField(queryset=Location.objects.all(), slug_field='name', required=False)
    # location = LocationSerializer(read_only=True)
    # assignedBy = serializers.SlugRelatedField(queryset=Employee.objects.all(), slug_field='fullName', required=False)
    # updatedBy = serializers.SlugRelatedField(queryset=Employee.objects.all(), slug_field='fullName', required=False)
    # employee = serializers.SlugRelatedField(queryset=Employee.objects.all(), slug_field='fullName', required=False)

    class Meta:
        model = EmployeeWorkingDays
        fields = '__all__'

class DepartmentCompactSerializer(serializers.ModelSerializer):

    class Meta:
        model = Department
        fields = '__all__'

class DepartmentWorkingDaysSerializer(serializers.ModelSerializer):
    location = serializers.SlugRelatedField(queryset=Location.objects.all(), slug_field='name', required=False)
    # location = LocationSerializer(read_only=True)
    assignedBy = serializers.SlugRelatedField(queryset=Employee.objects.all(), slug_field='fullName', required=False)
    updatedBy = serializers.SlugRelatedField(queryset=Employee.objects.all(), slug_field='fullName', required=False)
    # department = serializers.SlugRelatedField(queryset=Department.objects.all(), slug_field='name', required=False)
    department = DepartmentCompactSerializer(read_only=True, many=True)
    sessionType = serializers.SlugRelatedField(queryset=WorkingDayTypes.objects.all(), slug_field='sessionType',
                                             required=False)

    class Meta:
        model = DepartmentWorkingDays
        fields = '__all__'

class DepartmentWorkingDaysPostSerializer(serializers.ModelSerializer):
    location = serializers.SlugRelatedField(queryset=Location.objects.all(), slug_field='name', required=False)
    # location = LocationSerializer(read_only=True)
    # assignedBy = serializers.SlugRelatedField(queryset=Employee.objects.all(), slug_field='fullName', required=False)
    # updatedBy = serializers.SlugRelatedField(queryset=Employee.objects.all(), slug_field='fullName', required=False)
    # department = serializers.SlugRelatedField(queryset=Department.objects.all(), slug_field='name', required=False)

    class Meta:
        model = DepartmentWorkingDays
        fields = '__all__'

class EmployeePutSerializer(serializers.ModelSerializer):

    department = serializers.SlugRelatedField(queryset=Department.objects.all(), slug_field='name', required=False)
    role = serializers.SlugRelatedField(queryset=Role.objects.all(), slug_field='name', required=False)
    grade = serializers.SlugRelatedField(queryset=Grade.objects.all(), slug_field='name',
                                                     required=False)
    employement_status = serializers.SlugRelatedField(queryset=EmployementStatus.objects.all(), slug_field='name',
                                                     required=False)
    location = serializers.SlugRelatedField(queryset=Location.objects.all(), slug_field='name',
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
        model = Permissions
        fields = '__all__'
class OrgWorkingDaysSerializer(serializers.ModelSerializer):
    location = serializers.SlugRelatedField(queryset=Location.objects.all(), slug_field='name', required=False)
    # location = LocationSerializer(read_only=True)
    updatedBy = serializers.SlugRelatedField(queryset=Employee.objects.all(), slug_field='fullName', required=False)
    class Meta:
        model = OrganizationWorkingDays
        fields = '__all__'

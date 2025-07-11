#  Copyright (c) 2023.
#  Designed & Developed by Narendar Reddy G, OscarFX Private Limited
#  All rights reserved.

from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.serializers import Serializer,CharField

from hrm.serializers import RoleSerializer, DepartmentSerializer
from hrm.models import Employee, Department, Location, Role
from production.models import Clients, Projects, ShotStatus, Complexity, Shots, Sequence, Task_Type, MyTask, \
    Assignments, Channels, Groups, Qc_Assignment, Folder_Permissions, Permission_Groups, \
    ShotVersions, TaskHelp_Main, TaskHelp_Lead, TaskHelp_Artist, ShotLogs, Locality, DayLogs, TeamLead_Week_Reports, \
    QCVersions, ClientVersions, TimeLogs, TaskDayLogs, Elements, RolePipelineSteps, AssignmentStepsOrder, StatusSegregation,EstimationId

class EstimationSerializer(serializers.ModelSerializer):
    clientName = serializers.CharField(source='client.name', read_only= True)
    class Meta:
        model = EstimationId
        fields = '__all__'

class StatusSerializer(serializers.ModelSerializer):
    status_segregation = serializers.SlugRelatedField(queryset=StatusSegregation.objects.all(), slug_field='code', required=False)
    class Meta:
        model = ShotStatus
        fields = '__all__'

class LocalitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Locality
        fields = '__all__'

class ComplexitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Complexity
        fields = '__all__'
class Task_TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task_Type
        fields = '__all__'


class ClientSerializer(serializers.ModelSerializer):
    locality = serializers.SlugRelatedField(queryset=Locality.objects.all(), slug_field='name', required=False)

    class Meta:
        model = Clients
        fields = ('id', 'name','country',
                  'locality', 'trigger', 'producer_email')

class ProjectSerializer(serializers.ModelSerializer):
    client = serializers.SlugRelatedField(queryset=Clients.objects.all(), slug_field='name', required=False)
    org_status = serializers.SlugRelatedField(queryset=ShotStatus.objects.all(), slug_field='name', required=False)
    imageSrc = serializers.ImageField(max_length=None, use_url=True, allow_null=True, required=False)

    class Meta:
        model = Projects
        fields = '__all__'

class ProjectPostSerializer(serializers.ModelSerializer):
    # client = serializers.SlugRelatedField(queryset=Clients.objects.all(), slug_field='name', required=False)
    org_status = serializers.SlugRelatedField(queryset=ShotStatus.objects.all(), slug_field='code', required=False)
    # imageSrc = serializers.ImageField(max_length=None, use_url=True, allow_null=True, required=False)

    class Meta:
        model = Projects
        fields = '__all__'

class ProjectClientSerializer(serializers.ModelSerializer):
    client = ClientSerializer(read_only=True)
    org_status = serializers.SlugRelatedField(queryset=ShotStatus.objects.all(), slug_field='code', required=False)
    imageSrc = serializers.ImageField(max_length=None, use_url=True, allow_null=True, required=False)

    class Meta:
        model = Projects
        fields = '__all__'

class ProjectCompactSerializer(serializers.ModelSerializer):
    client = ClientSerializer(read_only=True)

    class Meta:
        model = Projects
        fields = ('id',
                  'name',
                  'client','status')
        depth = 1

class SequenceCompactSerializer(serializers.ModelSerializer):
    project = ProjectCompactSerializer(read_only=True)

    class Meta:
        model = Sequence
        fields = ('id',
                  'name',
                  'project')
        depth = 1

class EmployeeCompactSerializer(serializers.ModelSerializer):
    # team_lead = serializers.SlugRelatedField(queryset=Employee.objects.select_related('role','team_lead','supervisor').all(), slug_field='fullName', required=False)
    class Meta:
        model = Employee
        fields = ('fullName','id','employee_id','department','role','photo')
        depth = 1

class ShotTaskCompactSerializer(serializers.ModelSerializer):
    shot = serializers.PrimaryKeyRelatedField(queryset=MyTask.objects.all(),source='shot.id')
    artist = serializers.SlugRelatedField(queryset=Employee.objects.all(), slug_field='fullName', required=False)
    # lead = serializers.SlugRelatedField(queryset=)

    class Meta:
        model = MyTask
        fields = ('shot','compiler', 'artist')
        depth = 0

class LeadCompactSerializer(serializers.ModelSerializer):
    shot = serializers.PrimaryKeyRelatedField(queryset=Assignments.objects.all(),source='shot.id')
    lead = serializers.SlugRelatedField(queryset=Employee.objects.prefetch_related('team_lead','supervisor'), slug_field='fullName', required=False)

    class Meta:
        model = Assignments
        fields = ('shot','lead')
        depth = 0

class ShotCompactSerializer(serializers.ModelSerializer):
    sequence = SequenceCompactSerializer(read_only=True)
    status = StatusSerializer(read_only=True)
    complexity = serializers.SlugRelatedField(queryset=Complexity.objects.all(), slug_field='name', required=False)
    task_type = serializers.SlugRelatedField(queryset=Task_Type.objects.all(), slug_field='name', required=False)
    imageSrc = serializers.ImageField(max_length=None, use_url=True, allow_null=True, required=False)
    task = ShotTaskCompactSerializer(many=True, read_only=True)
    supervisor = serializers.SlugRelatedField(queryset=Employee.objects.all(), slug_field='fullName', required=False)
    team_lead = serializers.SlugRelatedField(queryset=Employee.objects.select_related('location','department','role').all(), slug_field='fullName', required=False)
    hod = serializers.SlugRelatedField(queryset=Employee.objects.select_related('location','department','role').all(), slug_field='fullName', required=False)
    artist = serializers.SlugRelatedField(queryset=Employee.objects.select_related('location','department','role').all(), slug_field='fullName', required=False)
    class Meta:
        model = Shots
        fields = '__all__'
        depth = 1

class SequenceSerializer(serializers.ModelSerializer):
    project = ProjectCompactSerializer(read_only=True)

    class Meta:
        model = Sequence
        fields = '__all__'

class TaskTypeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Task_Type
        fields = '__all__'

class SequencePostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sequence
        fields = '__all__'

class ShotsPostSerializer(serializers.ModelSerializer):
    status = serializers.SlugRelatedField(queryset=ShotStatus.objects.all(), slug_field='code', required=False)
    complexity = serializers.SlugRelatedField(queryset=Complexity.objects.all(), slug_field='name', required=False)
    task_type = serializers.SlugRelatedField(queryset=Task_Type.objects.all(), slug_field='name', required=False)
    imageSrc = serializers.ImageField(max_length=None, use_url=True, allow_null=True, required=False)
    eta = serializers.DateTimeField(format=None,input_formats=['%Y-%m-%d',])
    internal_eta = serializers.DateTimeField(format=None,input_formats=['%Y-%m-%d',], required=False)

    class Meta:
        model = Shots
        fields = '__all__'

class ShotsSerializer(serializers.ModelSerializer):
    sequence = SequenceCompactSerializer(read_only=True)
    status = StatusSerializer(read_only=True)
    # status = serializers.SlugRelatedField(queryset=ShotStatus.objects.all(), slug_field='code', required=False)
    complexity = serializers.SlugRelatedField(queryset=Complexity.objects.all(), slug_field='name', required=False)
    task_type = serializers.SlugRelatedField(queryset=Task_Type.objects.all(), slug_field='name', required=False)
    imageSrc = serializers.ImageField(max_length=None, use_url=True, allow_null=True, required=False)
    supervisor = serializers.SlugRelatedField(queryset=Employee.objects.all(), slug_field='fullName', required=False)
    team_lead = serializers.SlugRelatedField(queryset=Employee.objects.all(), slug_field='fullName', required=False)
    hod = serializers.SlugRelatedField(queryset=Employee.objects.all(), slug_field='fullName', required=False)
    artist = serializers.SlugRelatedField(queryset=Employee.objects.all(), slug_field='fullName', required=False)
    # artists = serializers.SlugRelatedField(queryset=Employee.objects.all(), slug_field='fullName', required=False)
    artists = EmployeeCompactSerializer(read_only=True, many=True)
    qc_name = serializers.SlugRelatedField(queryset=Employee.objects.all(), slug_field='fullName', required=False)
    location = serializers.SlugRelatedField(queryset=Location.objects.all(), slug_field='name', required=False)

    class Meta:
        model = Shots
        fields = ('__all__')
        depth = 0
class ElementsSerializer(serializers.ModelSerializer):
    # sequence = SequenceCompactSerializer(read_only=True)
    # status = StatusSerializer(read_only=True)
    status = serializers.SlugRelatedField(queryset=ShotStatus.objects.all(), slug_field='code', required=False)
    # complexity = serializers.SlugRelatedField(queryset=Complexity.objects.all(), slug_field='name', required=False)
    # task_type = serializers.SlugRelatedField(queryset=Task_Type.objects.all(), slug_field='name', required=False)
    # team_lead = serializers.SlugRelatedField(queryset=Employee.objects.all(), slug_field='fullName', required=False)
    # artist = serializers.SlugRelatedField(queryset=Employee.objects.all(), slug_field='fullName', required=False)
    # qc_name = serializers.SlugRelatedField(queryset=Employee.objects.all(), slug_field='fullName', required=False)
    location = serializers.SlugRelatedField(queryset=Location.objects.all(), slug_field='name', required=False)

    class Meta:
        model = Elements
        fields = ('__all__')
        depth = 0

class PipelineStepsSerializer(serializers.ModelSerializer):

    status = serializers.SlugRelatedField(queryset=ShotStatus.objects.all(), slug_field='code', required=False)
    allowed_steps = serializers.SlugRelatedField(queryset=ShotStatus.objects.all(), slug_field='code', required=False, many=True)
    department = serializers.SlugRelatedField(queryset=Department.objects.all(), slug_field='name', required=False)
    role = serializers.SlugRelatedField(queryset=Role.objects.all(), slug_field='name', required=False)

    class Meta:
        model = RolePipelineSteps
        # fields = ('__all__')
        fields = ('department','role','status','allowed_steps')
        depth = 0

# class AssignmentStepsOrderSerializer(serializers.ModelSerializer):
#     # role = serializers.SlugRelatedField(queryset=Role.objects.all(), slug_field='name', required=False)
#     # acceptCase = serializers.SlugRelatedField(queryset=ShotStatus.objects.all(), slug_field='name', required=False)
#     # rejectCase = serializers.SlugRelatedField(queryset=ShotStatus.objects.all(), slug_field='name', required=False)
#     department = DepartmentSerializer(read_only=True)
#     role = RoleSerializer(read_only=True)
#     shotStatus = StatusSerializer(read_only=True)
#     authorised_roles = RoleSerializer(read_only=True,many=True)
#     allowed_steps = RoleSerializer(read_only=True,many=True)
#     acceptCase = StatusSerializer(read_only=True) 
#     rejectCase = StatusSerializer(read_only=True)
#     onRejectSendTo = RoleSerializer(read_only=True)
#     created_by = serializers.SlugRelatedField(queryset=Employee.objects.all(), slug_field='fullName', required=False)
#     updated_by = serializers.SlugRelatedField(queryset=Employee.objects.all(), slug_field='fullName', required=False)

#     class Meta:
#         model = AssignmentStepsOrder
#         fields = '__all__'


class ShotLogsSerializer(serializers.ModelSerializer):
    shot = serializers.SlugRelatedField(queryset=Shots.objects.all(), slug_field='name', required=False)
    updated_by = serializers.SlugRelatedField(queryset=Employee.objects.all(), slug_field='fullName', required=False)

    class Meta:
        model = ShotLogs
        fields = ('__all__')
        depth = 1

class ShotLogsPostSerializer(serializers.ModelSerializer):
    # shot = serializers.SlugRelatedField(queryset=Shots.objects.all(), slug_field='name', required=False)
    # updated_by = serializers.SlugRelatedField(queryset=Employee.objects.all(), slug_field='fullName', required=False)

    class Meta:
        model = ShotLogs
        fields = ('__all__')

class DayLogsSerializer(serializers.ModelSerializer):
    # shot = ShotCompactSerializer(read_only=True)
    artist = serializers.SlugRelatedField(queryset=Employee.objects.all(), slug_field='fullName', required=False)
    updated_by = serializers.SlugRelatedField(queryset=Employee.objects.all(), slug_field='fullName', required=False)

    class Meta:
        model = DayLogs
        fields = ('__all__')

class TaskDayLogsSerializer(serializers.ModelSerializer):
    # shot = ShotCompactSerializer(read_only=True)
    artist = serializers.SlugRelatedField(queryset=Employee.objects.all(), slug_field='fullName', required=False)
    updated_by = serializers.SlugRelatedField(queryset=Employee.objects.all(), slug_field='fullName', required=False)

    class Meta:
        model = TaskDayLogs
        fields = ('__all__')
        
class TaskDayLogsSerializer2(serializers.ModelSerializer):
    # shot = ShotCompactSerializer(read_only=True)
    artist = EmployeeCompactSerializer(read_only=True)
    updated_by = serializers.SlugRelatedField(queryset=Employee.objects.all(), slug_field='fullName', required=False)

    class Meta:
        model = TaskDayLogs
        fields = ('__all__')

class TaskDayLogsPUTSerializer(serializers.ModelSerializer):
    # shot = ShotCompactSerializer(read_only=True)
    # artist = EmployeeCompactSerializer(read_only=True)
    # updated_by = EmployeeCompactSerializer(read_only=True)

    class Meta:
        model = TaskDayLogs
        fields = ('__all__')

class TimeLogsSerializer(serializers.ModelSerializer):
    # shot = ShotCompactSerializer(read_only=True)
    approved_by = serializers.SlugRelatedField(queryset=Employee.objects.all(), slug_field='fullName', required=False)
    # updated_by = serializers.SlugRelatedField(queryset=Employee.objects.all(), slug_field='fullName', required=False)

    class Meta:
        model = TimeLogs
        fields = ('__all__')

class TimeCardSerializer(serializers.ModelSerializer):
    approved_by = serializers.SlugRelatedField(queryset=Employee.objects.all(), slug_field='fullName', required=False)
    creation_date = serializers.DateTimeField(read_only=True, format="%d-%m-%Y")

    class Meta:
        model = TimeLogs
        fields = ('__all__')

class ShotTimeCardSerializer(serializers.ModelSerializer):
    updated_by = serializers.SlugRelatedField(queryset=Employee.objects.all(), slug_field='fullName', required=False)
    approved_by = serializers.SlugRelatedField(queryset=Employee.objects.all(), slug_field='fullName', required=False)
    creation_date = serializers.DateTimeField(read_only=True, format="%d-%m-%Y")

    class Meta:
        model = TimeLogs
        fields = ('__all__')

class LightDataSerializer(serializers.ModelSerializer):
    shot = ShotCompactSerializer(read_only=True)
    approved_by = serializers.SlugRelatedField(queryset=Employee.objects.all(), slug_field='fullName', required=False)
    creation_date = serializers.DateTimeField(read_only=True, format="%d-%m-%Y")

    class Meta:
        model = TimeLogs
        fields = ('__all__')

class DayLogsPostSerializer(serializers.ModelSerializer):
    # shot = serializers.SlugRelatedField(queryset=Shots.objects.all(), slug_field='name', required=False)
    # updated_by = serializers.SlugRelatedField(queryset=Employee.objects.all(), slug_field='fullName', required=False)

    class Meta:
        model = DayLogs
        fields = ('__all__')

class TaskDayLogsPostSerializer(serializers.ModelSerializer):
    # shot = serializers.SlugRelatedField(queryset=Shots.objects.all(), slug_field='name', required=False)
    # updated_by = serializers.SlugRelatedField(queryset=Employee.objects.all(), slug_field='fullName', required=False)

    class Meta:
        model = TaskDayLogs
        fields = ('__all__')

class TimeLogsPostSerializer(serializers.ModelSerializer):
    # shot = serializers.SlugRelatedField(queryset=Shots.objects.all(), slug_field='name', required=False)
    # updated_by = serializers.SlugRelatedField(queryset=Employee.objects.all(), slug_field='fullName', required=False)

    class Meta:
        model = TimeLogs
        fields = ('__all__')

class TeamReportSerializer(serializers.ModelSerializer):
    # shot = serializers.SlugRelatedField(queryset=Shots.objects.all(), slug_field='name', required=False)
    # artist = serializers.SlugRelatedField(queryset=Employee.objects.all(), slug_field='fullName', required=False)
    # updated_by = serializers.SlugRelatedField(queryset=Employee.objects.all(), slug_field='fullName', required=False)
    team_lead = serializers.SlugRelatedField(queryset=Employee.objects.all(), slug_field='fullName', required=False)

    class Meta:
        model = TeamLead_Week_Reports
        fields = ('__all__')
        depth = 1

class MyTaskSerializer(serializers.ModelSerializer):
    shot = serializers.SlugRelatedField(queryset=Shots.objects.all(), slug_field='name', required=False)
    artist = serializers.SlugRelatedField(queryset=Employee.objects.all(), slug_field='fullName', required=False)
    assigned_by = serializers.SlugRelatedField(queryset=Employee.objects.all(), slug_field='fullName', required=False)
    # status = serializers.SlugRelatedField(queryset=ShotStatus.objects.all(), slug_field='name', required=False)
    task_status = StatusSerializer(read_only=True)

    class Meta:
        model = MyTask
        fields = '__all__'

class MyTaskShotSerializer(serializers.ModelSerializer):
    artist = serializers.SlugRelatedField(queryset=Employee.objects.all(), slug_field='fullName', required=False)
    assigned_by = serializers.SlugRelatedField(queryset=Employee.objects.all(), slug_field='fullName', required=False)
    # status = serializers.SlugRelatedField(queryset=ShotStatus.objects.all(), slug_field='name', required=False)
    task_status = StatusSerializer(read_only=True)
    class Meta:
        model = MyTask
        fields = '__all__'

class MyTaskUpdateSerializer(serializers.ModelSerializer):
    task_status = serializers.SlugRelatedField(queryset=ShotStatus.objects.all(), slug_field='code', required=False)
    # task_status = StatusSerializer()
    class Meta:
        model = MyTask
        fields = '__all__'

class MyTaskStatusSerializer(serializers.ModelSerializer):
    #task_status = serializers.SlugRelatedField(queryset=ShotStatus.objects.all(), slug_field='code', required=False)
    task_status = StatusSerializer()
    class Meta:
        model = MyTask
        fields = '__all__'

class MyTaskPostSerializer(serializers.ModelSerializer):
    task_status = serializers.SlugRelatedField(queryset=ShotStatus.objects.all(), slug_field='code', required=False)

    class Meta:
        model = MyTask
        fields = '__all__'

class MyTaskArtistSerializer(serializers.ModelSerializer):
    shot = ShotCompactSerializer(read_only=True)
    task_status = StatusSerializer(read_only=True)
    artist = serializers.SlugRelatedField(queryset=Employee.objects.all(), slug_field='fullName', required=False)
    assigned_by = serializers.SlugRelatedField(queryset=Employee.objects.all(), slug_field='fullName', required=False)

    class Meta:
        model = MyTask
        fields = '__all__'

class AssignmentSerializer(serializers.ModelSerializer):
    shot = ShotCompactSerializer(read_only=True)
    # shot = serializers.SlugRelatedField(queryset=Shots.objects.all(), slug_field='name', required=False)
    lead = serializers.SlugRelatedField(queryset=Employee.objects.select_related('location','department','role').all(), slug_field='fullName', required=False)
    assigned_by = serializers.SlugRelatedField(queryset=Employee.objects.select_related('location','department','role').all(), slug_field='fullName', required=False)
    # status = serializers.SlugRelatedField(queryset=ShotStatus.objects.all(), slug_field='name', required=False)

    class Meta:
        model = Assignments
        fields = '__all__'

class AssignmentPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Assignments
        fields = '__all__'

class ChannelsSerializer(serializers.ModelSerializer):
    shot = serializers.SlugRelatedField(queryset=Shots.objects.all(), slug_field='id', required=False)
    sender = serializers.SlugRelatedField(queryset=Employee.objects.all(), slug_field='fullName', required=False)
    class Meta:
        model = Channels
        fields = '__all__'

class ChannelsPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Channels
        fields = '__all__'

class GroupsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Groups
        fields = '__all__'

class QCSerializer(serializers.ModelSerializer):
    qc_status = serializers.SlugRelatedField(queryset=ShotStatus.objects.all(), slug_field='code', required=False)
    class Meta:
        model = Qc_Assignment
        fields = '__all__'

class TaskCompactSerializer(serializers.ModelSerializer):
    shot = ShotCompactSerializer(read_only=True)
    task_status = serializers.SlugRelatedField(queryset=ShotStatus.objects.all(), slug_field='code', required=False)

    class Meta:
        model = MyTask
        fields = '__all__'

class TeamQCSerializer(serializers.ModelSerializer):
    task = TaskCompactSerializer(read_only=True)
    qc_status = serializers.SlugRelatedField(queryset=ShotStatus.objects.all(), slug_field='code', required=False)

    class Meta:
        model = Qc_Assignment
        fields = '__all__'

class ShotVersionsSerializer(serializers.ModelSerializer):
    status = serializers.SlugRelatedField(queryset=ShotStatus.objects.all(), slug_field='code', required=True)
    class Meta:
        model = ShotVersions
        fields ='__all__'

class AllShotVersionsSerializer(serializers.ModelSerializer):
    sent_by = serializers.SlugRelatedField(queryset=Employee.objects.all(), slug_field='fullName', required=True)
    verified_by = serializers.SlugRelatedField(queryset=Employee.objects.all(), slug_field='fullName', required=True)
    status = serializers.SlugRelatedField(queryset=ShotStatus.objects.all(), slug_field='code', required=True)
    class Meta:
        model = ShotVersions
        fields ='__all__'

class QcVersionsSerializer(serializers.ModelSerializer):
    status = serializers.SlugRelatedField(queryset=ShotStatus.objects.all(), slug_field='code', required=True)
    class Meta:
        model = QCVersions
        fields ='__all__'

class AllShotQcVersionsSerializer(serializers.ModelSerializer):
    sent_by = serializers.SlugRelatedField(queryset=Employee.objects.all(), slug_field='fullName', required=True)
    verified_by = serializers.SlugRelatedField(queryset=Employee.objects.all(), slug_field='fullName', required=True)
    status = serializers.SlugRelatedField(queryset=ShotStatus.objects.all(), slug_field='code', required=True)
    class Meta:
        model = QCVersions
        fields ='__all__'

class ClientVersionsSerializer(serializers.ModelSerializer):
    status = serializers.SlugRelatedField(queryset=ShotStatus.objects.all(), slug_field='code', required=True)
    sent_by = serializers.SlugRelatedField(queryset=Employee.objects.all(), slug_field='fullName', required=True)
    class Meta:
        model = ClientVersions
        fields ='__all__'

class AllShotClientVersionsSerializer(serializers.ModelSerializer):
    sent_by = serializers.SlugRelatedField(queryset=Employee.objects.all(), slug_field='fullName', required=True)
    verified_by = serializers.SlugRelatedField(queryset=Employee.objects.all(), slug_field='fullName', required=True)
    status = serializers.SlugRelatedField(queryset=ShotStatus.objects.all(), slug_field='code', required=True)
    class Meta:
        model = ClientVersions
        fields ='__all__'

class PGSerializer(serializers.ModelSerializer):
    permitted_users = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username', required=False)
    department = serializers.SlugRelatedField(queryset=Department.objects.all(), slug_field='name', required=False)

    class Meta:
        model = Permission_Groups
        fields = '__all__'

#TaskHelpMain Serializers
class TaskHelpMainSerializer(serializers.ModelSerializer):
    shot = ShotCompactSerializer(read_only=True)
    status = StatusSerializer(read_only=True)
    complexity = serializers.SlugRelatedField(queryset=Complexity.objects.all(), slug_field='name', required=False)
    task_type = serializers.SlugRelatedField(queryset=Task_Type.objects.all(), slug_field='name', required=False)
    imageSrc = serializers.ImageField(max_length=None, use_url=True, allow_null=True, required=False)
    requested_by = serializers.SlugRelatedField(queryset=Employee.objects.all(), slug_field='fullName', required=True)

    class Meta:
        model = TaskHelp_Main
        fields ='__all__'
        depth = 1

class TaskHelpMainPostSerializer(serializers.ModelSerializer):
    status = serializers.SlugRelatedField(queryset=ShotStatus.objects.all(), slug_field='code', required=False)

    class Meta:
        model = TaskHelp_Main
        fields = '__all__'

class TaskHelpLeadSerializer(serializers.ModelSerializer):
    shot = serializers.SlugRelatedField(queryset=Shots.objects.all(), slug_field='name', required=True)
    # status = serializers.SlugRelatedField(queryset=ShotStatus.objects.all(), slug_field='code', required=True)
    task_type = serializers.SlugRelatedField(queryset=Task_Type.objects.all(), slug_field='name', required=True)
    assigned_by = serializers.SlugRelatedField(queryset=Employee.objects.all(), slug_field='fullName', required=True)
    assigned_to = serializers.SlugRelatedField(queryset=Employee.objects.all(), slug_field='fullName', required=True)

    class Meta:
        model = TaskHelp_Lead
        fields ='__all__'

class TaskHelpArtistSerializer(serializers.ModelSerializer):
    shot = ShotCompactSerializer(read_only=True)
    status = StatusSerializer(read_only=True)
    # task_type = serializers.SlugRelatedField(queryset=Task_Type.objects.all(), slug_field='name', required=True)
    assigned_by = serializers.SlugRelatedField(queryset=Employee.objects.all(), slug_field='fullName', required=True)
    assigned_to = serializers.SlugRelatedField(queryset=Employee.objects.all(), slug_field='fullName', required=True)

    class Meta:
        model = TaskHelp_Artist
        fields ='__all__'

class TaskHelpArtistPostSerializer(serializers.ModelSerializer):
    status = serializers.SlugRelatedField(queryset=ShotStatus.objects.all(), slug_field='code', required=False)

    class Meta:
        model = TaskHelp_Artist
        fields = '__all__'

class TaskHelpArtistUpdateSerializer(serializers.ModelSerializer):
    status = serializers.SlugRelatedField(queryset=ShotStatus.objects.all(), slug_field='code', required=False)
    # task_status = StatusSerializer()
    class Meta:
        model = TaskHelp_Artist
        fields = '__all__'

class TaskHelpArtistStatusSerializer(serializers.ModelSerializer):
    #task_status = serializers.SlugRelatedField(queryset=ShotStatus.objects.all(), slug_field='code', required=False)
    status = StatusSerializer()
    class Meta:
        model = TaskHelp_Artist
        fields = '__all__'

## Parent Child Process
class TimeLogSerializer(serializers.HyperlinkedModelSerializer):
    shot = serializers.PrimaryKeyRelatedField(queryset=Shots.objects.all(), source='shot.id')

    class Meta:
        model = TimeLogs
        fields = ('spent_hours', 'shot')

## Parent Child Process
class ShotTimeLogSerializer(serializers.ModelSerializer):
    timelogs = TimeLogSerializer(many=True, read_only=True)
    sequence = SequenceCompactSerializer(read_only=True)
    status = StatusSerializer(read_only=True)
    # status = serializers.SlugRelatedField(queryset=ShotStatus.objects.all(), slug_field='code', required=False)
    complexity = serializers.SlugRelatedField(queryset=Complexity.objects.all(), slug_field='name', required=False)
    task_type = serializers.SlugRelatedField(queryset=Task_Type.objects.all(), slug_field='name', required=False)
    imageSrc = serializers.ImageField(max_length=None, use_url=True, allow_null=True, required=False)
    supervisor = serializers.SlugRelatedField(queryset=Employee.objects.all(), slug_field='fullName', required=False)
    team_lead = serializers.SlugRelatedField(queryset=Employee.objects.all(), slug_field='fullName', required=False)
    hod = serializers.SlugRelatedField(queryset=Employee.objects.all(), slug_field='fullName', required=False)
    artist = serializers.SlugRelatedField(queryset=Employee.objects.all(), slug_field='fullName', required=False)
    # artist = EmployeeCompactSerializer(read_only=True)
    artists = EmployeeCompactSerializer(read_only=True, many=True)
    location = serializers.SlugRelatedField(queryset=Location.objects.all(), slug_field='name', required=False)

    class Meta:
        model = Shots
        fields = '__all__'
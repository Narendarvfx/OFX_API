from rest_framework import serializers

from hrm.models import Employee
from production.models import Clients, Projects, ShotStatus, Complexity, Shots, Sequence, Task_Type, MyTask, \
    Assignments, Channels, Groups, Qc_Assignment, HeadQc_Assignment, HeadQCTeam


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShotStatus
        fields = '__all__'


class ComplexitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Complexity
        fields = '__all__'


class ClientSerializer(serializers.ModelSerializer):
    imageSrc = serializers.ImageField(max_length=None, use_url=True, allow_null=True, required=False)
    # status = serializers.SlugRelatedField(queryset=ShotStatus.objects.all(), slug_field='name', required=False)

    class Meta:
        model = Clients
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    client = serializers.SlugRelatedField(queryset=Clients.objects.all(), slug_field='name', required=False)
    # status = serializers.SlugRelatedField(queryset=ShotStatus.objects.all(), slug_field='name', required=False)
    imageSrc = serializers.ImageField(max_length=None, use_url=True, allow_null=True, required=False)

    class Meta:
        model = Projects
        fields = '__all__'


class ProjectCompactSerializer(serializers.ModelSerializer):
    client = serializers.SlugRelatedField(queryset=Clients.objects.all(), slug_field='name', required=False)

    class Meta:
        model = Projects
        fields = ('id',
                  'name',
                  'client')
        depth = 1

class SequenceCompactSerializer(serializers.ModelSerializer):
    project = ProjectCompactSerializer(read_only=True)

    class Meta:
        model = Sequence
        fields = ('name',
                  'project')
        depth = 1

class ShotCompactSerializer(serializers.ModelSerializer):
    # client = serializers.SlugRelatedField(queryset=Clients.objects.all(), slug_field='name', required=False)
    sequence = SequenceCompactSerializer(read_only=True)
    status = StatusSerializer(read_only=True)
    # status = serializers.SlugRelatedField(queryset=ShotStatus.objects.all(), slug_field='name', required=False)
    complexity = serializers.SlugRelatedField(queryset=Complexity.objects.all(), slug_field='name', required=False)
    task_type = serializers.SlugRelatedField(queryset=Task_Type.objects.all(), slug_field='name', required=False)
    imageSrc = serializers.ImageField(max_length=None, use_url=True, allow_null=True, required=False)

    class Meta:
        model = Shots
        fields = '__all__'
        depth = 1

class SequenceSerializer(serializers.ModelSerializer):
    project = ProjectCompactSerializer(read_only=True)
    # status = serializers.SlugRelatedField(queryset=ShotStatus.objects.all(), slug_field='name', required=False)

    class Meta:
        model = Sequence
        fields = '__all__'

class SequencePostSerializer(serializers.ModelSerializer):
    # status = serializers.SlugRelatedField(queryset=ShotStatus.objects.all(), slug_field='name', required=False)

    class Meta:
        model = Sequence
        fields = '__all__'

class ShotsPostSerializer(serializers.ModelSerializer):
    status = serializers.SlugRelatedField(queryset=ShotStatus.objects.all(), slug_field='code', required=False)
    complexity = serializers.SlugRelatedField(queryset=Complexity.objects.all(), slug_field='name', required=False)
    task_type = serializers.SlugRelatedField(queryset=Task_Type.objects.all(), slug_field='name', required=False)
    imageSrc = serializers.ImageField(max_length=None, use_url=True, allow_null=True, required=False)

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

    class Meta:
        model = Shots
        fields = '__all__'

class MyTaskSerializer(serializers.ModelSerializer):
    shot = serializers.SlugRelatedField(queryset=Shots.objects.all(), slug_field='name', required=False)
    artist = serializers.SlugRelatedField(queryset=Employee.objects.all(), slug_field='fullName', required=False)
    assigned_by = serializers.SlugRelatedField(queryset=Employee.objects.all(), slug_field='fullName', required=False)
    # status = serializers.SlugRelatedField(queryset=ShotStatus.objects.all(), slug_field='name', required=False)

    class Meta:
        model = MyTask
        fields = '__all__'

class MyTaskShotSerializer(serializers.ModelSerializer):
    artist = serializers.SlugRelatedField(queryset=Employee.objects.all(), slug_field='fullName', required=False)
    assigned_by = serializers.SlugRelatedField(queryset=Employee.objects.all(), slug_field='fullName', required=False)
    # status = serializers.SlugRelatedField(queryset=ShotStatus.objects.all(), slug_field='name', required=False)

    class Meta:
        model = MyTask
        fields = '__all__'

class MyTaskUpdateSerializer(serializers.ModelSerializer):
    task_status = serializers.SlugRelatedField(queryset=ShotStatus.objects.all(), slug_field='code', required=False)

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
    task_status = serializers.SlugRelatedField(queryset=ShotStatus.objects.all(), slug_field='code', required=False)
    artist = serializers.SlugRelatedField(queryset=Employee.objects.all(), slug_field='fullName', required=False)
    assigned_by = serializers.SlugRelatedField(queryset=Employee.objects.all(), slug_field='fullName', required=False)

    class Meta:
        model = MyTask
        fields = '__all__'

class AssignmentSerializer(serializers.ModelSerializer):
    shot = ShotCompactSerializer(read_only=True)
    # shot = serializers.SlugRelatedField(queryset=Shots.objects.all(), slug_field='name', required=False)
    lead = serializers.SlugRelatedField(queryset=Employee.objects.all(), slug_field='fullName', required=False)
    assigned_by = serializers.SlugRelatedField(queryset=Employee.objects.all(), slug_field='fullName', required=False)
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

class HQCSerializer(serializers.ModelSerializer):
    hqc_status = serializers.SlugRelatedField(queryset=ShotStatus.objects.all(), slug_field='code', required=False)
    class Meta:
        model = HeadQc_Assignment
        fields = '__all__'

class HeadQCSerializer(serializers.ModelSerializer):
    qc_task = TeamQCSerializer(read_only=True)
    # hqc = serializers.SlugRelatedField(queryset=HeadQCTeam.objects.all(), slug_field='hqc__id', required=False)
    hqc_status = serializers.SlugRelatedField(queryset=ShotStatus.objects.all(), slug_field='code', required=False)

    class Meta:
        model = HeadQc_Assignment
        fields = '__all__'
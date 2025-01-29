from rest_framework import serializers

from hrm.models import Employee, Location
from pipeline_api.models import ShotConfig, Dependencies, AssetTypes, ProjectConfig, WinProjectConfig, \
    LinuxProjectConfig, SBDesktopVersion
from production.models import Shots, Complexity, Task_Type, Projects, Clients, Sequence
from production.serializers import SequenceCompactSerializer, StatusSerializer, EmployeeCompactSerializer

# class ProjectClientSerializer(serializers.ModelSerializer):
#     client = ClientSerializer(read_only=True)
#     org_status = serializers.SlugRelatedField(queryset=ShotStatus.objects.all(), slug_field='code', required=False)
#     imageSrc = serializers.ImageField(max_length=None, use_url=True, allow_null=True, required=False)
#
#     class Meta:
#         model = Projects
#         fields = '__all__'

class ClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Clients
        fields = ('name',)

class ProjectCompactSerializer(serializers.ModelSerializer):
    client = ClientSerializer(read_only=True)

    class Meta:
        model = Projects
        fields = ('id','name',
                  'client')
        depth = 0

class SequenceCompactSerializer(serializers.ModelSerializer):
    project = ProjectCompactSerializer(read_only=True)

    class Meta:
        model = Sequence
        fields = ('name','project','path','type',)
        depth = 1
class EpisodeCompactSerializer(serializers.ModelSerializer):
    # project = ProjectCompactSerializer(read_only=True)

    class Meta:
        model = Sequence
        fields = ('name','path','type',)
        depth = 1


class ShotCompactSerializer(serializers.ModelSerializer):
    sequence =SequenceCompactSerializer(read_only=True)
    episode =SequenceCompactSerializer(read_only=True)
    class Meta:
        model = Shots
        fields = ('name','sequence','episode',)
        depth = 1
class ShotsDependencySerializer(serializers.ModelSerializer):
    department = serializers.SlugRelatedField(queryset=Task_Type.objects.all(), slug_field='name', required=False)
    asset_type = serializers.SlugRelatedField(queryset=AssetTypes.objects.all(), slug_field='name', required=False)
    shot = ShotCompactSerializer(read_only=True)
    class Meta:
        model = Dependencies
        # fields = ('shot','depend_type','asset_type','asset_name','asset_path', 'department')
        fields = ('__all__')
        depth = 1

class ApiShotsSerializer(serializers.ModelSerializer):
    shot = ShotCompactSerializer(read_only=True)
    # sequence = SequenceCompactSerializer(read_only=True)
    # episode = EpisodeCompactSerializer(read_only=True)
    # status = StatusSerializer(read_only=True)
    # # status = serializers.SlugRelatedField(queryset=ShotStatus.objects.all(), slug_field='code', required=False)
    # complexity = serializers.SlugRelatedField(queryset=Complexity.objects.all(), slug_field='name', required=False)
    # task_type = serializers.SlugRelatedField(queryset=Task_Type.objects.all(), slug_field='name', required=False)
    # imageSrc = serializers.ImageField(max_length=None, use_url=True, allow_null=True, required=False)
    # supervisor = serializers.SlugRelatedField(queryset=Employee.objects.all(), slug_field='fullName', required=False)
    # team_lead = serializers.SlugRelatedField(queryset=Employee.objects.all(), slug_field='fullName', required=False)
    # hod = serializers.SlugRelatedField(queryset=Employee.objects.all(), slug_field='fullName', required=False)
    # artist = serializers.SlugRelatedField(queryset=Employee.objects.all(), slug_field='fullName', required=False)
    # artists = EmployeeCompactSerializer(read_only=True, many=True)
    # location = serializers.SlugRelatedField(queryset=Location.objects.all(), slug_field='name', required=False)

    class Meta:
        model = ShotConfig
        fields = ('__all__')

class WinConfigCompactSerializer(serializers.ModelSerializer):

    class Meta:
        model = WinProjectConfig
        fields = ('__all__')
class LinuxConfigCompactSerializer(serializers.ModelSerializer):

    class Meta:
        model = LinuxProjectConfig
        fields = ('__all__')
class ProjectConfigSerializer(serializers.ModelSerializer):
    project = ProjectCompactSerializer(read_only=True)
    win_config = WinConfigCompactSerializer(read_only=True)
    linux_config = LinuxConfigCompactSerializer(read_only=True)
    class Meta:
        model = ProjectConfig
        fields = ('__all__')
class SBDesktopVersionSerializer(serializers.ModelSerializer):

    class Meta:
        model = SBDesktopVersion
        fields = ('__all__')
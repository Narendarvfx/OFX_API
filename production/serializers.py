from rest_framework import serializers

from production.models import Clients, Projects, Status, Complexity, Shots, Sequence


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'


class ComplexitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Complexity
        fields = '__all__'


class ClientSerializer(serializers.ModelSerializer):
    imageSrc = serializers.ImageField(max_length=None, use_url=True, allow_null=True, required=False)
    status = serializers.SlugRelatedField(queryset=Status.objects.all(), slug_field='name', required=False)

    class Meta:
        model = Clients
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    client = serializers.SlugRelatedField(queryset=Clients.objects.all(), slug_field='name', required=False)
    status = serializers.SlugRelatedField(queryset=Status.objects.all(), slug_field='name', required=False)
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


class SequenceSerializer(serializers.ModelSerializer):
    project = ProjectCompactSerializer(read_only=True)
    status = serializers.SlugRelatedField(queryset=Status.objects.all(), slug_field='name', required=False)

    class Meta:
        model = Sequence
        fields = '__all__'

class SequencePostSerializer(serializers.ModelSerializer):
    status = serializers.SlugRelatedField(queryset=Status.objects.all(), slug_field='name', required=False)

    class Meta:
        model = Sequence
        fields = '__all__'

class ShotsPostSerializer(serializers.ModelSerializer):
    status = serializers.SlugRelatedField(queryset=Status.objects.all(), slug_field='name', required=False)
    complexity = serializers.SlugRelatedField(queryset=Complexity.objects.all(), slug_field='name', required=False)
    imageSrc = serializers.ImageField(max_length=None, use_url=True, allow_null=True, required=False)

    class Meta:
        model = Shots
        fields = '__all__'


class ShotsSerializer(serializers.ModelSerializer):
    sequence = SequenceCompactSerializer(read_only=True)
    status = serializers.SlugRelatedField(queryset=Status.objects.all(), slug_field='name', required=False)
    complexity = serializers.SlugRelatedField(queryset=Complexity.objects.all(), slug_field='name', required=False)
    imageSrc = serializers.ImageField(max_length=None, use_url=True, allow_null=True, required=False)

    class Meta:
        model = Shots
        fields = '__all__'

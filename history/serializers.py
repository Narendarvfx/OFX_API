from rest_framework import serializers

from history.models import ShotsHistory


class ShotsHistorySerializer(serializers.ModelSerializer):
    # status = serializers.SlugRelatedField(queryset=ShotStatus.objects.all(), slug_field='code', required=False)
    # complexity = serializers.SlugRelatedField(queryset=Complexity.objects.all(), slug_field='name', required=False)
    # task_type = serializers.SlugRelatedField(queryset=Task_Type.objects.all(), slug_field='name', required=False)
    # imageSrc = serializers.ImageField(max_length=None, use_url=True, allow_null=True, required=False)
    # supervisor = serializers.SlugRelatedField(queryset=Employee.objects.all(), slug_field='fullName', required=False)
    # team_lead = serializers.SlugRelatedField(queryset=Employee.objects.all(), slug_field='fullName', required=False)
    # hod = serializers.SlugRelatedField(queryset=Employee.objects.all(), slug_field='fullName', required=False)
    # artist = serializers.SlugRelatedField(queryset=Employee.objects.all(), slug_field='fullName', required=False)
    # # artists = serializers.SlugRelatedField(queryset=Employee.objects.all(), slug_field='fullName', required=False)
    # artists = EmployeeCompactSerializer(read_only=True, many=True)
    # qc_name = serializers.SlugRelatedField(queryset=Employee.objects.all(), slug_field='fullName', required=False)
    # location = serializers.SlugRelatedField(queryset=Location.objects.all(), slug_field='name', required=False)

    class Meta:
        model = ShotsHistory
        fields = ('__all__')
        depth = 0
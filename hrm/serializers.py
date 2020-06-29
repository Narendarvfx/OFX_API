from rest_framework import serializers

from hrm.models import Department, Role, Grade, EmployementStatus, Employee


class EmployeeSerializer(serializers.ModelSerializer):
    department = serializers.SlugRelatedField(queryset=Department.objects.all(), slug_field='name', required=False)
    role = serializers.SlugRelatedField(queryset=Role.objects.all(), slug_field='name', required=False)
    grade = serializers.SlugRelatedField(queryset=Grade.objects.all(), slug_field='name', required=False)
    employement_status = serializers.SlugRelatedField(queryset=EmployementStatus.objects.all(), slug_field='name',
                                                     required=False)
    photo = serializers.ImageField(max_length=None, use_url=True, allow_null=True, required=False)

    class Meta:
        model = Employee
        fields = '__all__'
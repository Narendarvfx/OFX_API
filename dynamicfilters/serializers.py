from rest_framework import serializers



# from .serializers import RoleSerializer, DepartmentSerializer
# from hrm.models import Employee, Department, Location, Role
# from production.models import Clients, Projects, ShotStatus, Complexity, Shots, Sequence, Task_Type, MyTask, \
#     Assignments, Channels, Groups, Qc_Assignment, Folder_Permissions, Permission_Groups, \
#     ShotVersions, TaskHelp_Main, TaskHelp_Lead, TaskHelp_Artist, ShotLogs, Locality, DayLogs, TeamLead_Week_Reports, \
#     QCVersions, ClientVersions, TimeLogs, TaskDayLogs, Elements, RolePipelineSteps, AssignmentStepsOrder



# #TaskHelpMain Serializers
# class TaskHelpMainSerializer(serializers.ModelSerializer):
#     shot = ShotCompactSerializer(read_only=True)
#     status = StatusSerializer(read_only=True)
#     complexity = serializers.SlugRelatedField(queryset=Complexity.objects.all(), slug_field='name', required=False)
#     task_type = serializers.SlugRelatedField(queryset=Task_Type.objects.all(), slug_field='name', required=False)
#     imageSrc = serializers.ImageField(max_length=None, use_url=True, allow_null=True, required=False)
#     requested_by = serializers.SlugRelatedField(queryset=Employee.objects.all(), slug_field='fullName', required=True)

#     class Meta:
#         model = TaskHelp_Main
#         fields ='__all__'
#         depth = 1
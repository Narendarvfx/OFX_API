import json
import datetime
import xlsxwriter
from django.db.models import Sum
from rest_framework import serializers
from hrm.models import Employee
from production.models import TaskDayLogs, MyTask, Shots, Sequence, Projects, Clients
from production.serializers import StatusSerializer

class ProjectCompactSerializer(serializers.ModelSerializer):
    client = serializers.SlugRelatedField(queryset=Clients.objects.all(), slug_field='name', required=False)

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

class ShotCompactSerializer(serializers.ModelSerializer):
    sequence = SequenceCompactSerializer(read_only=True)
    class Meta:
        model = Shots
        fields = ('sequence','name')
        depth = 1
class TaskDayLogsSerializer(serializers.ModelSerializer):
    # task = serializers.SlugRelatedField(queryset=MyTask.objects.all(), slug_field='fullName', required=False)
    artist = serializers.SlugRelatedField(queryset=Employee.objects.all(), slug_field='fullName', required=False)
    updated_by = serializers.SlugRelatedField(queryset=Employee.objects.all(), slug_field='fullName', required=False)

    class Meta:
        model = TaskDayLogs
        fields = ('__all__')


class MyTaskSerializer(serializers.ModelSerializer):
    shot = ShotCompactSerializer(read_only=True)
    artist = serializers.SlugRelatedField(queryset=Employee.objects.all(), slug_field='fullName', required=False)
    assigned_by = serializers.SlugRelatedField(queryset=Employee.objects.all(), slug_field='fullName', required=False)
    # status = serializers.SlugRelatedField(queryset=ShotStatus.objects.all(), slug_field='name', required=False)
    task_status = StatusSerializer(read_only=True)

    class Meta:
        model = MyTask
        fields = '__all__'




def tasklogs(taskdaylogs_ids=None):
    taskdaylogs = TaskDayLogs.objects.filter(pk__in=taskdaylogs_ids)
    taskdaylog_serializer = TaskDayLogsSerializer(taskdaylogs,many=True)
    taskdaylog_data = json.loads(json.dumps(taskdaylog_serializer.data))
    # print(taskdaylog_data)
    tasks = MyTask.objects.get(pk=taskdaylog_data[0]['task'])
    task_serializer = MyTaskSerializer(tasks)
    print()
    return {'shot_details':json.loads(json.dumps(task_serializer.data)), 'taskdaylog':taskdaylog_data}


def task_daylogs_download(buffer=None,taskdaylogs_ids = []):
    workbook = xlsxwriter.Workbook(buffer)
    worksheet = workbook.add_worksheet()
    bold = workbook.add_format({'bold': True, 'border': 1, 'border_color': 'black'})
    border = workbook.add_format({'border': 1, 'border_color': 'black'})

    if taskdaylogs_ids:
        get_task_data = tasklogs(taskdaylogs_ids)
        merge_format = workbook.add_format({
            'bold': 1,
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            'fg_color': 'yellow'})

        worksheet.merge_range("A1:B2", "Client:{}".format(str(get_task_data['shot_details']['shot']['sequence']['project']['client'])),merge_format)
        worksheet.merge_range("C1:D2", "Project:{}".format(str(get_task_data['shot_details']['shot']['sequence']['project']['name'])), merge_format)
        worksheet.merge_range("E1:H2", "Shot:{}".format(str(get_task_data['shot_details']['shot']['name'])), merge_format)
        worksheet.write('A3', 'DATE', bold)
        worksheet.write('B3', 'CREATED BY', bold)
        worksheet.write('C3','TASK BID DAYS', bold)
        worksheet.write('D3','CONSUMED MAN-DAYS', bold)
        worksheet.write('E3','ARTIST PERCENTAGE', bold)
        worksheet.write('F3','DAY PERCENTAGE', bold)
        worksheet.write('G3','UPDATED BY', bold)
        worksheet.write('H3','LAST UPDATE', bold)
        p=3
        for i,taskslog in enumerate(get_task_data['taskdaylog']):
            worksheet.write(i+p,0,datetime.datetime.strptime(str(taskslog['updated_date']), '%Y-%m-%dT%H:%M:%S.%f').strftime("%d-%m-%Y"),border)
            worksheet.write(i + p, 1, taskslog['artist'], border)
            worksheet.write(i + p, 2, taskslog['task_biddays'] if taskslog['task_biddays'] is not None else 'N/A', border)
            worksheet.write(i + p, 3, taskslog['consumed_man_day'] if taskslog['consumed_man_day'] is not None else 'N/A', border)
            worksheet.write(i + p, 4, taskslog['percentage'] if taskslog['percentage'] is not None else 'N/A', border)
            worksheet.write(i + p, 5, taskslog['day_percentage'] if taskslog['day_percentage'] is not None else 'N/A', border)
            worksheet.write(i + p, 6, taskslog['updated_by'], border)
            worksheet.write(i + p, 7, datetime.datetime.strptime(str(taskslog['last_updated_date']), '%Y-%m-%dT%H:%M:%S.%f').strftime("%d-%m-%Y"), border)

    workbook.close()
    return buffer
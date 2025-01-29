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
        fields = ('sequence','name','id')
        depth = 1

class MyTaskSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    # shot = ShotCompactSerializer(read_only=True)
    task_status = StatusSerializer(read_only=True)
    artist = serializers.SlugRelatedField(queryset=Employee.objects.all(), slug_field='fullName', required=False)
    assigned_by = serializers.SlugRelatedField(queryset=Employee.objects.all(), slug_field='fullName', required=False)

    class Meta:
        model = MyTask
        fields = '__all__'

def Mytask(shot_id=None):
    mytasks = MyTask.objects.filter(shot__pk=shot_id)
    mytask_serializer = MyTaskSerializer(mytasks, many=True)
    mytask_details= json.loads(json.dumps(mytask_serializer.data))
    shot_object = Shots.objects.get(pk=mytask_details[0]['shot'])
    shot_detils = ShotCompactSerializer(shot_object)
    return {'shot_details':json.loads(json.dumps(shot_detils.data, default=str)),'mytask':mytask_details}

def tasks_download(buffer=None,shot_id=None):
    workbook = xlsxwriter.Workbook(buffer)
    worksheet = workbook.add_worksheet()
    bold = workbook.add_format({'bold': True, 'border': 1, 'border_color': 'black'})
    border = workbook.add_format({'border': 1, 'border_color': 'black'})
    if shot_id:
        mytaskdata = Mytask(shot_id)
        merge_format = workbook.add_format({
            'bold': 1,
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            'fg_color': 'yellow'})

        worksheet.merge_range("A1:B2","Client:{}".format(str( mytaskdata['shot_details']['sequence']['project']['client'])), merge_format)
        worksheet.merge_range("C1:D2", "Project:{}".format(str( mytaskdata['shot_details']['sequence']['project']['name'])), merge_format)
        worksheet.merge_range("E1:H2", "Shot:{}".format(str( mytaskdata['shot_details']['name'])), merge_format)


        worksheet.write('A3', 'ARTIST', bold)
        worksheet.write('B3', 'STATUS', bold)
        worksheet.write('C3','BID DAYS', bold)
        worksheet.write('D3','PROGRESS', bold)
        worksheet.write('E3','CAPTAIN', bold)
        worksheet.write('F3','ETA', bold)
        worksheet.write('G3','ASSIGNED DATE', bold)
        p=3
        for i,mytask in enumerate(mytaskdata['mytask']):
            worksheet.write(i + p, 0, mytask['artist'], border)
            worksheet.write(i + p, 1, mytask['task_status']['code'], border)
            worksheet.write(i + p, 2, mytask['assigned_bids'], border)
            worksheet.write(i + p, 3, mytask['art_percentage'], border)
            worksheet.write(i + p, 4,'Yes' if mytask['compiler'] == 1 or 0 else "No", border)
            worksheet.write(i + p, 5, datetime.datetime.strptime(str(mytask['eta']),'%Y-%m-%dT%H:%M:%S').strftime("%d-%m-%Y"),border)
            worksheet.write(i + p, 6, datetime.datetime.strptime(str(mytask['creation_date']),'%Y-%m-%dT%H:%M:%S.%f').strftime("%d-%m-%Y"), border)

    workbook.close()
    return buffer
import json
import datetime

import xlsxwriter
from django.db.models import Sum
from rest_framework import serializers

from hrm.models import Employee
from production.models import ShotLogs, Shots, TaskDayLogs, MyTask, DayLogs, Sequence, Projects, Clients


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

class DayslogSerializer(serializers.ModelSerializer):
    artist =serializers.SlugRelatedField(queryset=Employee.objects.all(), slug_field='fullName', required=False)
    updated_by = serializers.SlugRelatedField(queryset=Employee.objects.all(), slug_field='fullName', required=False)

    class Meta:
        model = DayLogs
        fields = ('__all__')


def shotlogs(shotdaylogs_ids=None):
    dayshots = DayLogs.objects.filter(pk__in=shotdaylogs_ids)
    shotlog_serializer = DayslogSerializer(dayshots,many=True)
    shotlog_data = json.loads(json.dumps(shotlog_serializer.data,default=str))
    # print(shotlog_data)
    shot_object = Shots.objects.get(pk=shotlog_data[0]['shot'])
    shot_detils = ShotCompactSerializer(shot_object)

    return {'shot_details':json.loads(json.dumps(shot_detils.data, default=str)),'shotlogs':shotlog_data}



def shot_daylogs_download(buffer=None,shotdaylogs_ids=[]):
    workbook = xlsxwriter.Workbook(buffer)
    worksheet = workbook.add_worksheet()
    bold = workbook.add_format({'bold': True, 'border': 1, 'border_color': 'black'})
    border = workbook.add_format({'border': 1, 'border_color': 'black'})
    if shotdaylogs_ids:
        getshots = shotlogs(shotdaylogs_ids)
        merge_format = workbook.add_format({
            'bold': 1,
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            'fg_color': 'yellow'})

        worksheet.merge_range("A1:B2","Client:{}".format(str(getshots['shot_details']['sequence']['project']['client'])), merge_format)
        worksheet.merge_range("C1:D2", "Project:{}".format(str(getshots['shot_details']['sequence']['project']['name'])), merge_format)
        worksheet.merge_range("E1:H2", "Shot:{}".format(str(getshots['shot_details']['name'])), merge_format)

        worksheet.write('A3', 'DATE', bold)
        worksheet.write('B3', 'CREATED BY', bold)
        worksheet.write('C3','SHOT BID DAYS', bold)
        worksheet.write('D3','CONSUMED MAN-DAYS', bold)
        worksheet.write('E3','SHOT PERCENTAGE', bold)
        worksheet.write('F3','DAY PERCENTAGE', bold)
        worksheet.write('G3','UPDATED BY', bold)
        worksheet.write('H3','LAST UPDATE', bold)
        p=3
        for i, dayshot in enumerate (getshots['shotlogs']):
            worksheet.write(i+p,0, datetime.datetime.strptime(str(dayshot['updated_date']), '%Y-%m-%dT%H:%M:%S.%f').strftime("%d-%m-%Y"),border)
            worksheet.write(i+p,1, dayshot['artist'],border)
            worksheet.write(i+p,2, dayshot['shot_biddays']if dayshot['shot_biddays'] is not None else 'N/A', border)
            worksheet.write(i+p,3, dayshot['consumed_man_day']if dayshot['consumed_man_day'] is not None else 'N/A',border)
            worksheet.write(i+p,4, dayshot['percentage']if dayshot['percentage'] is not None else 'N/A',border)
            worksheet.write(i+p,5, dayshot['day_percentage']if  dayshot['day_percentage'] is not None else 'N/A',border)
            worksheet.write(i+p,6, dayshot['updated_by'],border)
            worksheet.write(i+p,7,datetime.datetime.strptime(str(dayshot[ 'last_updated_date']), '%Y-%m-%dT%H:%M:%S.%f').strftime("%d-%m-%Y"),border)




    workbook.close()
    return buffer

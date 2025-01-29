#  Copyright (c) 2022-2023.
#  Designed & Developed by Narendar Reddy G, OscarFX Private Limited
#  All rights reserved.
import datetime
import json

import xlsxwriter
from django.db.models import Sum
from xlsxwriter import workbook, Workbook

from OFX_API import apiRequestManager
from hrm.models import Employee, Department, Role, Grade, EmployementStatus, EmployeeRoleBinding, Location
from hrm.serializers import EmployeeSerializer, EmployeeCompactSerializer, UserSerializer
from ofx_statistics.models import EmployeeDailyStatistics
from production.models import DayLogs, Assignments, ClientVersions, MyTask, Shots, ShotVersions, QCVersions, TaskDayLogs
from production.serializers import DayLogsSerializer, AssignmentSerializer, ClientVersionsSerializer, MyTaskSerializer, \
    MyTaskArtistSerializer, ShotVersionsSerializer, QcVersionsSerializer, TaskDayLogsSerializer, StatusSerializer, \
    ShotCompactSerializer
from rest_framework import serializers

from production.v2.serializers import EmployeeDailyStatisticserializer


class GradeCompactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = '__all__'


class ArtistSerializer(serializers.ModelSerializer):
    department = serializers.SlugRelatedField(queryset=Department.objects.all(), slug_field='name', required=False)
    role = serializers.SlugRelatedField(queryset=Role.objects.all(), slug_field='name', required=False)
    grade = GradeCompactSerializer(read_only=True)
    employement_status = serializers.SlugRelatedField(queryset=EmployementStatus.objects.all(), slug_field='name', required=False)
    # photo = serializers.ImageField(max_length=None, use_url=True, allow_null=True, required=False)
    # team_lead = EmployeeCompactSerializer(read_only=True)
    # supervisor = EmployeeCompactSerializer(read_only=True)
    # creation_date = serializers.DateTimeField(format='%d-%m-%Y')
    profile = UserSerializer(read_only=True)

    class Meta:
        model = Employee
        fields = '__all__'

def get_artists_statistics(from_date=None, to_date=None, artist_ids=[]):
    statistics_data = EmployeeDailyStatistics.objects.select_related('employee','employee__department').filter(logDate__range=[str(from_date.strftime("%Y-%m-%d")), str(to_date.strftime("%Y-%m-%d"))], employee__id__in=artist_ids)
    statistic_serializer = EmployeeDailyStatisticserializer(statistics_data,many=True)
    return json.loads(json.dumps(statistic_serializer.data))

# def get_employee(artist_id):
#     artist = Employee.objects.get(pk=artist_id)
#     artist_serializer = ArtistSerializer(artist)
#     json_dump = json.dumps(artist_serializer.data)
#     artist_data = json.loads(json_dump)
#     print(artist_data)
#     return artist_data

def get_employees(ids=[]):
    artist = Employee.objects.filter(pk__in=ids)
    artist_serializer = ArtistSerializer(artist,many=True)
    artist_data = json.loads(json.dumps(artist_serializer.data))
    apiRequestManagers = apiRequestManager()
    locations = apiRequestManagers.getDBData(model=Location, queryFilter={}, queryPerams=["id", "name"])
    locations = {'id_{id}'.format(id=x['id']):x['name'] for x in locations}
    _Leadkeys = ['SUPERVISOR','TEAM LEAD',"HEAD OF DEPARTMENT"]
    art_bind = apiRequestManagers.getDBData(model=EmployeeRoleBinding, queryFilter={"employee__id__in":ids,"role__name__in":_Leadkeys}, select_related=['employee', 'employee__role','employee__department','department', 'role', 'bindWith', 'created_by', 'updated_by'], queryPerams=["id", "employee__id", "employee__employee_id", "role__id", "role__name", "bindWith__id", "bindWith__fullName"])
    _art_bind = {}
    for _i in art_bind:
        if _i["employee"]["employee_id"] is not None and _i["role"]["name"] is not None:
            if _art_bind.get(_i["employee"]["employee_id"],None) is None:
                _art_bind[_i["employee"]["employee_id"]] = {}
                for _led in _Leadkeys:
                    _art_bind[_i["employee"]["employee_id"]][apiRequestManagers.makeKey(_led).lower()] = None
            _art_bind[_i["employee"]["employee_id"]][apiRequestManagers.makeKey(_i["role"]["name"]).lower()] = _i["bindWith"]
    _artist_data = {}
    for _i in artist_data:
        if _i["employee_id"] is not None and len(_i["employee_id"]) > 0:
            _i["location"] = locations['id_{id}'.format(id=_i["location"])] if _i["location"] is not None else None
            _artist_data[_i["employee_id"]] = json.loads(json.dumps(_i))
            if _art_bind.get(_i["employee_id"], None) is not None:
                for _led in _Leadkeys:
                    _artist_data[_i["employee_id"]][apiRequestManagers.makeKey(_led).lower()] = _art_bind[_i["employee_id"]][apiRequestManagers.makeKey(_led).lower()]["fullName"] if _art_bind[_i["employee_id"]].get(apiRequestManagers.makeKey(_led).lower(), None) is not None else None
            else:
                for _led in _Leadkeys:
                    _artist_data[_i["employee_id"]][apiRequestManagers.makeKey(_led).lower()] = None
            

    return list(_artist_data.values())

def calculate_artist_id_data(artist_id=None, start_date=None, end_date=None, dept=None):
    if artist_id:
        tasks = MyTask.objects.filter(creation_date__range=[start_date.strftime('%Y-%m-%d')+'T00:00:00.000000', end_date.strftime('%Y-%m-%d')+'T23:59:59.999999'], artist=artist_id).select_related(
            'shot', 'artist',
            'shot__sequence',
            'shot__sequence__project',
            'shot__status',
            'shot__task_type',
            'shot__location',
            'shot__team_lead',
            'shot__artist',
            'shot__sequence__project__client').values_list('pk', flat=True)

    return list(tasks)


class TaskDayLogSerializer(serializers.ModelSerializer):
    # shot = ShotCompactSerializer(read_only=True)
    artist = serializers.SlugRelatedField(queryset=Employee.objects.all(), slug_field='fullName', required=False)
    updated_by = serializers.SlugRelatedField(queryset=Employee.objects.all(), slug_field='fullName', required=False)

    class Meta:
        model = TaskDayLogs
        fields = ('__all__')


def calculate_artist_task_day_logs(artist_id=None, start_date=None, end_date=None, dept=None):
    if artist_id:
        tasks = list(
            TaskDayLogs.objects.filter(updated_date__range=[start_date.strftime('%Y-%m-%d')+'T00:00:00.000000', end_date.strftime('%Y-%m-%d')+'T23:59:59.999999'], task__artist__id=artist_id).select_related(
                'task').values('task', 'task__shot__sequence__project__client__name',
                               'task__shot__sequence__project__name', 'task__shot__name',
                               'task__shot__actual_start_frame', 'task__shot__actual_end_frame',
                               'task__shot__task_type__name','task__shot__type', 'task__task_status__code', 'task__assigned_bids',
                               'task__art_percentage', 'task__eta__date','task__shot__eta__date', 'task__shot__team_lead__fullName','task__shot__version','task__shot__comments','task__shot__complexity__name','task__shot__bid_days').annotate(
                total_consumed=Sum('consumed_man_day')).order_by())

    return tasks




class TaskSerializer(serializers.ModelSerializer):
    shot = ShotCompactSerializer(read_only=True)
    artist = serializers.SlugRelatedField(queryset=Employee.objects.all(), slug_field='fullName', required=False)
    assigned_by = serializers.SlugRelatedField(queryset=Employee.objects.all(), slug_field='fullName', required=False)
    # status = serializers.SlugRelatedField(queryset=ShotStatus.objects.all(), slug_field='name', required=False)
    task_status = StatusSerializer(read_only=True)

    class Meta:
        model = MyTask
        fields = '__all__'

def get_task_data(id):
    tasks_data = MyTask.objects.get(id=id)
    task_serializer = TaskSerializer(tasks_data)
    json_dump = json.dumps(task_serializer.data)
    task_data = json.loads(json_dump)

    return task_data


def convert_date(conversion_date):
    '''
    Converts Date Time Object to date
    params: datetime
    returns: converted date
    '''

    try:
        _date = datetime.datetime.strptime(conversion_date, '%Y-%m-%dT%H:%M:%S.%f').strftime(
            "%d-%m-%Y")
    except:
        _date = datetime.datetime.strptime(conversion_date, '%Y-%m-%d.%f').strftime(
            "%d-%m-%Y")
    return _date

    datetime.strptime(dateformate(shot_data['eta']), '%Y-%m-%dT%H:%M:%S.%f')


# def getBgColor(range=100, valX=10):
#
#     value = (100 / range) * valX;
#     color = ['#f62d51', '#ffbc34', '#009efb', '#7460ee', '#55ce63'], status = parseInt(rDx);
#     return (`"text-`+lx[(status<25 ? 0 : (status<50 ? 1 : (status<75 ? 2 : (status<100 ? 3 : 4))))]+`" > ` + valX.toFixed(2) + ` < / div > `)
def getfontcolor(value_range=100, value=10):
    try:
        set_value =(100 / value_range) * value
        if set_value<25:
            fg_color = "#f62d51"
        elif set_value<50:
            fg_color = "#f57b17"
        elif set_value<75:
            fg_color = "#009efb"
        elif set_value<90:
            fg_color = "#7460ee"
        else:
            fg_color = "#55ce63"
    except:
        fg_color = "#f62d51"
    return fg_color
def diffcolor(value1 =10, value2=10):
    pmd = value1-value2
    if pmd<0:
        return "#EA5455"
    elif pmd ==0:
        return "#0854c2"
    else:
        return "#28C76F"

def artist_sheet_download(buffer=None, from_date=None, to_date=None, artist_ids=[]):
    workbook = xlsxwriter.Workbook(buffer)
    worksheet = workbook.add_worksheet()
    bold = workbook.add_format({'bold': True,  'border': 1, 'border_color': 'black','fg_color': '#3cb0f0'})
    # formate = workbook.add_format({'bold': True, 'bg_color': '#43d3f7', 'border': 1, 'border_color': 'red'})
    border = workbook.add_format({'border': 1, 'border_color': 'black'})
    date_format = workbook.add_format({'border': 1, 'border_color': 'black', 'num_format': 'dd/mm/yyyy'})
    format = '%Y-%m-%d'
    from_date = datetime.datetime.strptime(from_date,format)
    f_date = datetime.datetime.strptime(str(from_date), '%Y-%m-%d %H:%M:%S').strftime("%d-%m-%Y")
    to_date = datetime.datetime.strptime(to_date,format)
    t_date = datetime.datetime.strptime(str(to_date), '%Y-%m-%d %H:%M:%S').strftime("%d-%m-%Y")
    allEmployees = get_employees(artist_ids)
    artist_statistic_data = get_artists_statistics(from_date=from_date, to_date=to_date, artist_ids=artist_ids)
    _data = {}
    for i in allEmployees:
        tgd =i['grade']['a_man_day'] if i['grade'] is not None else 'N/A'
        _data[i['employee_id']] = {
            "employee_id": i['employee_id'],
            "name": i['fullName'],
            "dept": i['department'],
            "location": i['location'],
            "doj": convert_date(i['profile']['date_joined']),
            "doe": convert_date(i['doe']+"T00:00:00.000000") if i['doe'] is not None else None,
            "designation": i['role'],
            "level": i['grade']['name'] if i['grade'] is not None else 'N/A',
            "teamlead": i["teamlead"] if i["teamlead"] is not None else 'N/A',
            "supervisor": i["supervisor"] if i["supervisor"] is not None else 'N/A',
            "hod": i["headofdepartment"] if i["headofdepartment"] is not None else 'N/A',
            "targday": tgd,
            "tmd": 0,
            "amd": 0,
            "pmd": 0,
            "workingdays": 0,
            "leaves": 0,
            "presentdays": 0,
            "missETA": 0,
            "rwh": 0,
            "aeh": 0,
            "ash": 0,
            "comments": 'N/A'
            }
    for i in artist_statistic_data:
        if _data.get(i["employee"]['employee_id'],None) is not None:
            _data[i["employee"]['employee_id']]["tmd"] += i["tmd"]
            _data[i["employee"]['employee_id']]["amd"] += i["amd"]
            _data[i["employee"]['employee_id']]["leaves"] += i["leaves"]
            _data[i["employee"]['employee_id']]["rwh"] += i["rwh"]
            _data[i["employee"]['employee_id']]["aeh"] += i["aeh"]
            _data[i["employee"]['employee_id']]["ash"] += i["ash"]

    data = list(_data.values())
    # print(data)
    # dates = (from_date + datetime.timedelta(idx + 1)
    #          for idx in range((to_date - from_date).days))
    # print(dates)
    worksheet.write('A1', 'From Date', bold)
    worksheet.write('B1', 'To Date', bold)
    worksheet.write('C1', 'EMPLOYEE NUMBER', bold)
    worksheet.write('D1', 'EMPLOYEE NAME', bold)
    worksheet.write('E1', 'DEPARTMENT', bold)
    worksheet.write('F1', 'DOJ', bold)
    worksheet.write('G1', 'DOE', bold)
    worksheet.write('H1', 'DESIGNATION', bold)
    worksheet.write('I1', 'LEVEL', bold)
    worksheet.write('J1', 'TEAM LEAD', bold)
    worksheet.write('K1', 'HOD', bold)
    worksheet.write('L1', 'SUPERVISOR', bold)
    worksheet.write('M1', 'TARGET MANDAYS/DAY', bold)
    worksheet.write('N1', 'WORKING DAYS', bold)
    worksheet.write('O1', 'PRESENT DAYS', bold)
    worksheet.write('P1', 'LEAVES', bold)
    worksheet.write('Q1', 'TARGET MANDAYS ', bold)
    worksheet.write('R1', 'ACHIVED MANDAYS', bold)
    worksheet.write('S1', 'DIFFERENCE', bold)
    worksheet.write('T1', 'REQUIRED WORKING HOURS', bold)
    worksheet.write('U1', 'AVALIABLE HOURS', bold)
    worksheet.write('V1', 'ACTIVE HOURS', bold)
    worksheet.write('W1', 'COMMENTS', bold)
    worksheet.write('X1', 'LOCATION', bold)
    p = 1
    for j,d in enumerate(data):
        try:
            workingdays = (d['tmd'] / float(d['targday']))
        except Exception as e:
            workingdays = 0
        try:
            presentdays  = (d['tmd'] / float(d['targday']))-d['leaves']
        except Exception as e:
            presentdays = 0
        _missETA = "N/A"
        worksheet.write(p + j, 0, f_date, date_format)
        worksheet.write(p + j, 1, t_date, date_format)
        worksheet.write(p + j, 2, d['employee_id'], border)
        worksheet.write(p + j, 3, d['name'], border)
        worksheet.write(p + j, 4, d['dept'], border)
        worksheet.write(p + j, 5, str(d['doj']), date_format)
        worksheet.write(p + j, 6, str(d['doe']), date_format)
        worksheet.write(p + j, 7, d['designation'], border)
        worksheet.write(p + j, 8, d['level'], border)
        worksheet.write(p + j, 9, d['teamlead'], border)
        worksheet.write(p + j, 10, d['supervisor'], border)
        worksheet.write(p + j, 11, d['hod'], border)
        worksheet.write(p + j, 12, d['targday'], border)
        worksheet.write(p + j, 13, workingdays,border)
        worksheet.write(p + j, 14, presentdays, border)
        worksheet.write(p + j, 15, d['leaves'], border)
        worksheet.write(p + j, 16, d['tmd'], border)
        worksheet.write(p + j, 17, d['amd'], workbook.add_format({"font_color": getfontcolor(value_range=d['tmd'], value=d['amd']),'border': 1, 'border_color': 'black' }))
        worksheet.write(p + j, 18, (d['amd'] - d['tmd']),workbook.add_format({"font_color": diffcolor(value1=d['amd'],value2=d['tmd']),'border': 1, 'border_color': 'black'}))
        # worksheet.write(p + j, 17, _missETA,workbook.add_format({"font_color": '#ffbc34', 'border': 1, 'border_color': 'black'}))
        worksheet.write(p + j, 19, d['rwh'], border)
        worksheet.write(p + j, 20, d['aeh'], workbook.add_format({"font_color": getfontcolor(value_range=d['rwh'], value=d['aeh']),'border': 1, 'border_color': 'black' }))
        worksheet.write(p + j, 21, d['ash'], workbook.add_format({"font_color": getfontcolor(value_range=d['rwh'], value=d['ash']),'border': 1, 'border_color': 'black' }))
        worksheet.write(p + j, 22, d['comments'], workbook.add_format({"font_color":'#ffbc34','border': 1, 'border_color': 'black' }))
        worksheet.write(p + j, 23, d['location'] if d['location'] is not None else "GLOBAL", border)
    workbook.close()
    return buffer

def artist_individual_sheet_download(buffer=None, from_date=None, to_date=None, artist_id=None):
    workbook = xlsxwriter.Workbook(buffer)
    worksheet = workbook.add_worksheet()
    bold = workbook.add_format({'bold': True,  'border': 1, 'border_color': 'black'})
    # formate = workbook.add_format({'bold': True, 'bg_color': '#43d3f7', 'border': 1, 'border_color': 'red'})
    border = workbook.add_format({'border': 1, 'border_color': 'black'})
    format = '%Y-%m-%d'
    from_date = datetime.datetime.strptime(from_date,format)
    f_date = datetime.datetime.strptime(str(from_date), '%Y-%m-%d %H:%M:%S').strftime("%d-%m-%Y")
    to_date = datetime.datetime.strptime(to_date,format)
    t_date = datetime.datetime.strptime(str(to_date), '%Y-%m-%d %H:%M:%S').strftime("%d-%m-%Y")
    allEmployees = get_employees([artist_id])
    artist_statistic_data = get_artists_statistics(from_date=from_date, to_date=to_date, artist_ids=[artist_id])
    _data = {}
    for i in allEmployees:
        _data[i['employee_id']] = {
            "employee_id": i['employee_id'],
            "name": i['fullName'],
            "dept": i['department'],
            "doj": convert_date(i['profile']['date_joined']),
            "designation": i['role'],
            "employement_status": i['employement_status'],
            "level": i['grade']['name'] if i['grade'] is not None else 'N/A',
            "targday": i['grade']['a_man_day'] if i['grade'] is not None else 'N/A',
            "tmd": 0,
            "amd": 0,
            "missETA": 0,
            "leaves": 0,
            "rwh": 0,
            "aeh": 0,
            "ash": 0,
            "comments": 'N/A'
            }
    for i in artist_statistic_data:
        if _data.get(i["employee"]['employee_id'],None) is not None:
            _data[i["employee"]['employee_id']]["tmd"] += i["tmd"]
            _data[i["employee"]['employee_id']]["amd"] += i["amd"]
            _data[i["employee"]['employee_id']]["leaves"] += i["leaves"]
            _data[i["employee"]['employee_id']]["rwh"] += i["rwh"]
            _data[i["employee"]['employee_id']]["aeh"] += i["aeh"]
            _data[i["employee"]['employee_id']]["ash"] += i["ash"]
    artist_statistic = list(_data.values())
    artist_data = artist_statistic[0] if len(artist_statistic) > 0 else None

    data = calculate_artist_id_data(artist_id=artist_id, start_date=from_date, end_date=to_date)
    
    # gets the total consumed days and shot data from TaskDayLogs for selected artist and date range
    task_log_data = calculate_artist_task_day_logs(artist_id=artist_id, start_date=from_date, end_date=to_date)
    task_json_dump = json.dumps(task_log_data, indent=4, sort_keys=True, default=str)
    task_data_json = json.loads(task_json_dump)

    merge_format = workbook.add_format({
        'bold': 1,
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'fg_color': 'yellow'})
    
    summary_format = workbook.add_format({
        'bold': 1,
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'fg_color': '#3cb0f0'
    })
    wrap_format = workbook.add_format({'bold': 1,
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'fg_color': 'yellow',
        'text_wrap': True})
    lst = [artist_data["name"],artist_data["employee_id"]]
    worksheet.merge_range('A1:Q2', '\n'.join(lst), wrap_format)
    worksheet.merge_range('A3:Q3', str(convert_date(from_date.strftime('%Y-%m-%d.%f'))) + "  ---  " + str(convert_date(to_date.strftime('%Y-%m-%d.%f'))),merge_format)
    
    worksheet.merge_range('A4:B5', "Department: {}".format(str(artist_data["dept"])), summary_format)
    worksheet.merge_range('C4:D5', "Designation: {}".format(str(artist_data['designation'])), summary_format)
    worksheet.merge_range('E4:F5', "DOJ: {}".format(str(artist_data['doj'])), summary_format)
    worksheet.merge_range('G4:I5', "Artist Level: {}".format(str(artist_data['level'])), summary_format)
    worksheet.merge_range('J4:K5', "Status: {}".format(str(artist_data['employement_status'])), summary_format)
    worksheet.merge_range('L4:M5', "Target Mandays/Day: {}".format(str(round(artist_data['targday'],2)) if artist_data['targday'] != 'N/A' else 'N/A'), summary_format)
    worksheet.merge_range('N4:Q5', "Target Mandays for selected period: {}".format(str(round(artist_data["tmd"],2))), summary_format)
    worksheet.merge_range('A6:B7', "Missing ETA's: {}".format('N/A'), summary_format)
    worksheet.merge_range('C6:D7', "Leaves: {}".format(str(round(artist_data["leaves"],2))), summary_format)
    worksheet.merge_range('E6:F7', "Required Working Hours: {}".format(str(round(artist_data["rwh"],2))), summary_format)
    worksheet.merge_range('G6:I7', "Available/Essl Hours: {}".format(str(round(artist_data["aeh"],2))), summary_format)
    worksheet.merge_range('J6:K7', "Active/System Hours: {}".format(str(round(artist_data["ash"],2))), summary_format)
    worksheet.merge_range('L6:M7', "Achieved Mandays: {}".format(str(round(artist_data["amd"],2))), summary_format)  ## Empty cells
    worksheet.merge_range('N6:Q7', "Comments: {}".format(artist_data["comments"]), summary_format)  ## Empty cells

   
    # to get only task ids from a list of dicts
    my_list = map(lambda x: x["task"], task_log_data)
    li = list(my_list)
    
    # Identifies the task id's which are not exist in Task Day Logs
    new_list = list(set(data).difference(li))
 
    
    # Write some data headers.
    worksheet.write('A9', 'CLIENT', bold)
    worksheet.write('B9', 'PROJECT', bold)
    worksheet.write('C9', 'SHOT', bold)
    worksheet.write('D9', 'TOTAL FRAMES', bold)
    worksheet.write('E9', 'TASK', bold)
    worksheet.write('F9', 'TYPE', bold)
    worksheet.write('G9', 'STATUS', bold)
    worksheet.write('H9', 'COMPLEXITY', bold)
    worksheet.write('I9', 'SHOT BID DAYS', bold)
    worksheet.write('J9', 'WIP%', bold)
    worksheet.write('K9', 'ASSIGNED BID DAYS', bold)
    worksheet.write('L9', 'ACHIEVED MANDAYS', bold)
    worksheet.write('M9', 'SHOT ETA', bold)
    worksheet.write('N9', 'ASSIGNED ETA', bold)
    worksheet.write('O9', 'NOTES', bold)
    worksheet.write('P9','TEAM LEAD', bold)
    worksheet.write('Q9', 'CLIENT VERSION', bold)
    
    p = 9
    d = 0
    total_achieved = 0
    for c, shot_id in enumerate(task_data_json):
        # print(shot_id)
        total_frames = shot_id['task__shot__actual_end_frame'] - shot_id['task__shot__actual_start_frame'] + 1
        worksheet.write(c + p, 0, shot_id['task__shot__sequence__project__client__name'])
        worksheet.write(c + p, 1, shot_id['task__shot__sequence__project__name'])
        worksheet.write(c + p, 2, shot_id['task__shot__name'])
        worksheet.write(c + p, 3, total_frames)
        worksheet.write(c + p, 4, shot_id['task__shot__task_type__name'])
        worksheet.write(c + p, 5, shot_id['task__shot__type'])
        worksheet.write(c + p, 6, shot_id['task__task_status__code'])
        worksheet.write(c + p, 7, shot_id['task__shot__complexity__name'])
        worksheet.write(c + p, 8, shot_id['task__shot__bid_days'])
        worksheet.write(c + p, 9, str(round(shot_id['task__art_percentage'],2)) + "%")
        worksheet.write(c + p, 10, shot_id['task__assigned_bids'])
        worksheet.write(c + p, 11, str(round(shot_id['total_consumed'],2)))
        worksheet.write(c + p, 12, convert_date(datetime.datetime.strptime(shot_id['task__shot__eta__date'], '%Y-%m-%d').strftime('%Y-%m-%d.%f')) if shot_id.get('task__shot__eta__date',None) is not None else 'N/A')
        worksheet.write(c + p, 13, convert_date(datetime.datetime.strptime(shot_id['task__eta__date'], '%Y-%m-%d').strftime('%Y-%m-%d.%f')) if shot_id.get('task__eta__date',None) is not None else 'N/A')
        worksheet.write(c + p, 14, shot_id['task__shot__comments'])
        worksheet.write(c + p, 15, shot_id['task__shot__team_lead__fullName'])
        worksheet.write(c + p, 16, shot_id['task__shot__version'])
    
        total_achieved += shot_id['total_consumed']
        d = c+p +1
    # worksheet.merge_range('O4:P5', "Achieved Mandays: {}".format(total_achieved), summary_format)
    
    # Adding the shots which are not exist in TaskDay Log which may be RETAKE or YTS etc..
    if new_list:
        for listt in new_list:
            t_data = get_task_data(listt)
    
            # if t_data['shot']['type'] == "RETAKE":
            #     status = "RETAKE"
            #     bid_days = 0
            # else:
            #     status = t_data['shot']['status']['code']
            #     bid_days = t_data['assigned_bids']
            bid_days = t_data['assigned_bids']
            total_frames = t_data['shot']['actual_end_frame'] - t_data['shot']['actual_start_frame'] + 1
            worksheet.write(d, 0, t_data['shot']['sequence']['project']['client']['name'])
            worksheet.write(d, 1, t_data['shot']['sequence']['project']['name'])
            worksheet.write(d, 2, t_data['shot']['name'])
            worksheet.write(d, 3, total_frames)
            worksheet.write(d, 4, t_data['shot']['task_type'])
            worksheet.write(d, 5, t_data['shot']['type'])
            worksheet.write(d, 6, t_data['shot']['status']['code'])
            worksheet.write(d, 7, t_data['shot']['complexity'])
            worksheet.write(d, 8, t_data['shot']['bid_days'])
            worksheet.write(d, 9, str(t_data['art_percentage']) + "%")
            worksheet.write(d, 10, bid_days)
            worksheet.write(d, 11, str(round(t_data['shot']['achieved_mandays'],2))) # Achieved bid days
            worksheet.write(d, 12, convert_date(datetime.datetime.strptime(t_data['shot']['eta'], '%Y-%m-%dT%H:%M:%S').strftime('%Y-%m-%d.%f')) if t_data['shot'].get('eta',None) is not None else 'N/A')
            worksheet.write(d, 13, convert_date(datetime.datetime.strptime(t_data['eta'], '%Y-%m-%dT%H:%M:%S').strftime('%Y-%m-%d.%f')) if t_data.get('eta',None) is not None else 'N/A')
            worksheet.write(d, 14, t_data['shot']['comments'])
            worksheet.write(d, 15, t_data['shot']['team_lead'])
            worksheet.write(d, 16, t_data['shot']['version'])
    
            d += 1
    # worksheet.autofit()
    workbook.close()
    return buffer

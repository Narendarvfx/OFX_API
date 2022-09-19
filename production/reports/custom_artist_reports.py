import datetime
import json

import xlsxwriter

from hrm.models import Employee
from hrm.serializers import EmployeeSerializer
from production.models import DayLogs, Assignments, ClientVersions, MyTask, Shots, ShotVersions, QCVersions
from production.serializers import DayLogsSerializer, AssignmentSerializer, ClientVersionsSerializer, MyTaskSerializer, \
    MyTaskArtistSerializer, ShotVersionsSerializer, QcVersionsSerializer

def calculate_artist_data(artist_id=None, start_date=None, end_date=None, dept=None):
    if artist_id:
        tasks = MyTask.objects.filter(creation_date__range=[start_date,end_date],artist=artist_id).select_related('shot', 'artist',
                                                                                             'shot__sequence',
                                                                                             'shot__sequence__project',
                                                                                             'shot__status',
                                                                                             'shot__task_type',
                                                                                             'shot__location',
                                                                                             'shot__team_lead',
                                                                                             'shot__artist',
                                                                                             'shot__sequence__project__client',
                                                                                             'shot__sequence__project__client__locality')
    elif dept:
        tasks = MyTask.objects.filter(creation_date__range=[start_date, end_date], shot__task_type__name__contains=dept).select_related(
            'shot', 'artist',
            'shot__sequence',
            'shot__sequence__project',
            'shot__status',
            'shot__task_type',
            'shot__location',
            'shot__team_lead',
            'shot__artist',
            'shot__sequence__project__client',
            'shot__sequence__project__client__locality')
    else:
        tasks = MyTask.objects.filter(creation_date__range=[start_date, end_date]).select_related(
            'shot', 'artist',
            'shot__sequence',
            'shot__sequence__project',
            'shot__status',
            'shot__task_type',
            'shot__location',
            'shot__team_lead',
            'shot__artist',
            'shot__sequence__project__client',
            'shot__sequence__project__client__locality')
    serializer = MyTaskArtistSerializer(tasks, many=True)

    return serializer.data

def get_employee(artist_id):
    artist = Employee.objects.get(profile_id=artist_id)
    artist_serializer = EmployeeSerializer(artist)
    json_dump = json.dumps(artist_serializer.data)
    artist_data = json.loads(json_dump)
    return artist_data

def convert_date(conversion_date):
    '''
    Converts Date Time Object to date
    params: datetime
    returns: converted date
    '''
    _date = datetime.datetime.strptime(conversion_date, '%Y-%m-%dT%H:%M:%S').strftime(
        "%d-%m-%Y")
    return _date

def creation_convert_date(conversion_date):
    '''
    Converts Date Time Object to date
    params: datetime
    returns: converted date
    '''
    _date = datetime.datetime.strptime(conversion_date, '%Y-%m-%dT%H:%M:%S.%f').strftime(
        "%d-%m-%Y")
    return _date

def artist_sheet_download(buffer=None, start_date=None, end_date=None, artist_id=None, dept=None):
    workbook = xlsxwriter.Workbook(buffer)
    data = calculate_artist_data(artist_id=artist_id, start_date=start_date, end_date=end_date, dept=dept)
    json_dump = json.dumps(data)
    task_data = json.loads(json_dump)
    shot_list = task_data
    total_shots = len(shot_list)
    worksheet = workbook.add_worksheet()

    bold = workbook.add_format({'bold': True, 'bg_color': '#43d3f7', 'border': 1, 'border_color': 'black'})
    pending_color = workbook.add_format({'bg_color': 'yellow', 'border': 1, 'border_color': 'black'})
    border = workbook.add_format({'border': 1, 'border_color': 'black'})
    # Add a number format for cells with percentage.
    percent = workbook.add_format({'num_format': '0.0%', 'border': 1, 'border_color': 'black'})

    # Write some data headers.
    worksheet.write('A4', 'CLIENT', bold)
    worksheet.write('B4', 'PROJECT', bold)
    worksheet.write('C4', 'SHOT CODE', bold)
    worksheet.write('D4', 'TASK', bold)
    worksheet.write('E4', 'STATUS', bold)
    worksheet.write('F4', 'BID DAYS', bold)
    worksheet.write('G4', 'PROGRESS', bold)
    worksheet.write('H4', 'CONSUMED BID DAYS', bold)
    worksheet.write('I4', 'PENDING BID DAYS', bold)
    worksheet.write('J4', 'ASSIGNED DATE', bold)
    worksheet.write('K4', 'ETA', bold)
    worksheet.write('L4', 'ARTIST', bold)
    worksheet.write('M4', 'TEAM LEAD', bold)

    col = 0
    row = 3
    for shot_id in shot_list:
        try:
            shot_status = shot_id['shot']['status']['code']
            if shot_id['shot']['status']['code'] in ['YTA', 'ATL', 'YTS']:
                shot_status = "YTS"
            elif shot_id['shot']['status']['code'] in ['WIP', 'STC', 'LRT']:
                shot_status = "WIP"
            elif shot_id['shot']['status']['code'] in ['STQ', 'IRT', 'LAP']:
                shot_status = "QC"
            elif shot_id['shot']['status']['code'] == "IAP":
                shot_status = "IAP"
            elif shot_id['shot']['status']['code'] == "CRT":
                shot_status = "RETAKE"

            bid_days = float(shot_id['assigned_bids'])
            percentile = shot_id['shot']['progress'] / 100

            bid_column = 'F{}'.format(row + 2)
            progress_column = 'G{}'.format(row + 2)
            pending_column = 'I{}'.format(row+2)
            due_date = ""
            if shot_id['eta']:
                due_date = convert_date(shot_id['eta'])

            assigned_date = ""
            if shot_id['creation_date']:
                assigned_date = creation_convert_date(shot_id['creation_date'])

            worksheet.write(row + 1, col, shot_id['shot']['sequence']['project']['client']['name'], border)
            worksheet.write(row + 1, col + 1, shot_id['shot']['sequence']['project']['name'], border)
            worksheet.write(row + 1, col + 2, shot_id['shot']['name'], border)
            worksheet.write(row + 1, col + 3, shot_id['shot']['task_type'], border)
            worksheet.write(row + 1, col + 4, shot_status, border)
            worksheet.write(row + 1, col + 5, bid_days, border)
            worksheet.write(row + 1, col + 6, percentile, percent)
            worksheet.write(row + 1, col + 7, '=ROUND(({}-{}),1)'.format(bid_column, pending_column), pending_color)
            worksheet.write(row + 1, col + 8, '=ROUND(({}-{}*{}),1)'.format(bid_column, bid_column, progress_column), pending_color)
            worksheet.write(row + 1, col + 9, assigned_date, border)
            worksheet.write(row + 1, col + 10, due_date, border)
            worksheet.write(row + 1, col + 11, shot_id['artist'], border)
            worksheet.write(row + 1, col + 12, shot_id['shot']['team_lead'], border)

        except Exception as e:
            print(e)
            pass

        row += 1
    merge_format = workbook.add_format({
        'bold': 1,
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'fg_color': 'yellow'})
    fmerge_format = workbook.add_format({
        'bold': 1,
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'fg_color': '#22B2E2'})

    # Merge 3 cells.

    if artist_id:
        artist_data = get_employee(artist_id)
        if artist_data['grade']:
            grade = artist_data['grade']
        else:
            grade = "N/A"
        worksheet.merge_range('A1:M1', str(artist_data['fullName'] + "  Level: "+grade), merge_format)
    elif dept:
        worksheet.merge_range('A1:M1', dept+" Artist Report", merge_format)
    else:
        worksheet.merge_range('A1:M1', "Artist Report" , merge_format)
    worksheet.merge_range('A2:M3', str(convert_date(start_date))+ "  ---  " + str(convert_date(end_date)), merge_format)

    workbook.close()
    return buffer

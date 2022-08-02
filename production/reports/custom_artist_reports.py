import datetime
import json

import xlsxwriter

from hrm.models import Employee
from hrm.serializers import EmployeeSerializer
from production.models import DayLogs, Assignments, ClientVersions, MyTask, Shots, ShotVersions, QCVersions
from production.serializers import DayLogsSerializer, AssignmentSerializer, ClientVersionsSerializer, MyTaskSerializer, \
    MyTaskArtistSerializer, ShotVersionsSerializer, QcVersionsSerializer


def calculate_artist_data(artist_id, start_date, end_date):
    tasks = MyTask.objects.filter(creation_date__range=[start_date,end_date],artist__profile__user_id=artist_id).select_related('shot', 'artist',
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
    # json_dump = json.dumps(serializer.data)
    # task_data = json.loads(json_dump)
    # data = {
    #     "total_shots": 'N/A',
    #     "achieved_mandays": 'N/A',
    #     "yts": 'N/A',
    #     "wip": 'N/A',
    #     "completed": 'N/A',
    #     "total_mandays" : 'N/A',
    #     "act_vs_ach": 'N/A',
    #     "retakes": 'N/A',
    #     "retakes_per": 'N/A',
    #     "yts_per": 'N/A',
    #     "wip_per": 'N/A',
    #     "comp_per": 'N/A'
    # }
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

def artist_sheet_download(buffer, start_date, end_date, artist_id):
    workbook = xlsxwriter.Workbook(buffer)
    data = calculate_artist_data(artist_id, start_date, end_date)
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
    worksheet.write('H4', 'ETA', bold)
    worksheet.write('I4', 'TEAM LEAD', bold)

    col = 0
    row = 3
    for shot_id in shot_list:
        try:
            # lead_version = ShotVersions.objects.select_related('status').filter(shot=shot_id['shot']['id']).last()
            # lead_version_serializer = ShotVersionsSerializer(lead_version)
            # lead_version_json_dump = json.dumps(lead_version_serializer.data)
            # lead_version_data = json.loads(lead_version_json_dump)
            #
            # qc_version = QCVersions.objects.select_related('status').filter(shot=shot_id['shot']['id']).last()
            # qc_version_serializer = QcVersionsSerializer(qc_version)
            # qc_version_json_dump = json.dumps(qc_version_serializer.data)
            # qc_version_data = json.loads(qc_version_json_dump)
            #
            # client_version = ClientVersions.objects.select_related('status').filter(shot=shot_id['shot']['id']).last()
            # client_version_serializer = ClientVersionsSerializer(client_version)
            # client_version_json_dump = json.dumps(client_version_serializer.data)
            # client_version_data = json.loads(client_version_json_dump)

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

            due_date = ""
            if shot_id['eta']:
                due_date = convert_date(shot_id['eta'])

            worksheet.write(row + 1, col, shot_id['shot']['sequence']['project']['client']['name'], border)
            worksheet.write(row + 1, col + 1, shot_id['shot']['sequence']['project']['name'], border)
            worksheet.write(row + 1, col + 2, shot_id['shot']['name'], border)
            worksheet.write(row + 1, col + 3, shot_id['shot']['task_type'], border)
            worksheet.write(row + 1, col + 4, shot_status, border)
            worksheet.write(row + 1, col + 5, bid_days, border)
            worksheet.write(row + 1, col + 6, percentile, percent)
            worksheet.write(row + 1, col + 7, due_date, border)
            worksheet.write(row + 1, col + 8, shot_id['shot']['team_lead'], border)
            # worksheet.write(row + 1, col + 9, client_version_data['version'], border)
            # worksheet.write(row + 1, col + 10, qc_version_data['version'], border)
            # worksheet.write(row + 1, col + 11, lead_version_data['version'], border)
        except Exception as e:
            print(e)
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

    artist_data = get_employee(artist_id)
    worksheet.merge_range('A1:I1', str(artist_data['fullName']), merge_format)
    worksheet.merge_range('A2:I3', str(convert_date(start_date))+ "  ---  " + str(convert_date(end_date)), merge_format)
    # worksheet.merge_range('A4:D6', "Total Shots : " + str(total_shots), fmerge_format)
    # worksheet.merge_range('E4:G6', "Actual ManDays : " + str(round(assign_data[3])), fmerge_format)
    # worksheet.merge_range('H4:J6', "Achieved ManDays : " + str(round(data[1])), fmerge_format)
    # worksheet.merge_range('K4:M6', "Actual vs Achieved : " + str(round(assign_data[3] - data[1])), fmerge_format)
    # worksheet.merge_range('N4:Q6', "Total Artists : 10", fmerge_format)
    #
    # worksheet.merge_range('A7:D8', "YTS : " + str(round(assign_data[0])), fmerge_format)
    # worksheet.merge_range('E7:G8', "WIP : " + str(round(assign_data[1])), fmerge_format)
    # worksheet.merge_range('H7:J8', "HOLD : 0", fmerge_format)
    # worksheet.merge_range('K7:M8', "COMPLETED : " + str(round(assign_data[2])), fmerge_format)
    # worksheet.merge_range('N7:Q8', "RETAKES : "+str(data[2]), fmerge_format)

    workbook.close()
    return buffer

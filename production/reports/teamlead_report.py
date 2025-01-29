#  Copyright (c) 2023.
#  Designed & Developed by Narendar Reddy G, OscarFX Private Limited
#  All rights reserved.

import datetime
import json

import xlsxwriter

from production.models import DayLogs, Assignments, Shots, ShotVersions, QCVersions, ClientVersions
from production.serializers import DayLogsSerializer, AssignmentSerializer, ShotsSerializer, ShotVersionsSerializer, \
    QcVersionsSerializer, ClientVersionsSerializer


def getlogs(start_date, end_date, lead_id):
    daylogs = DayLogs.objects.filter(updated_date__range=[start_date, end_date],
                                     shot__team_lead__profile_id=lead_id).select_related('shot', 'artist', 'updated_by',
                                                                                         'shot__sequence',
                                                                                         'shot__sequence__project',
                                                                                         'shot__status',
                                                                                         'shot__task_type',
                                                                                         'shot__location',
                                                                                         'shot__team_lead',
                                                                                         'shot__artist',
                                                                                         'shot__sequence__project__client',
                                                                                         'shot__sequence__project__client__locality')
    serializer = DayLogsSerializer(daylogs, many=True)
    json_dump = json.dumps(serializer.data)
    daylog_data = json.loads(json_dump)
    total_mandays = 0
    shots = []
    for dat in daylog_data:
        total_mandays += dat['consumed_man_day']
        if dat['shot'] not in shots:
            shots.append(dat['shot'])

    total_retakes = 0
    for shot in shots:
        client_version = ClientVersions.objects.select_related('status').filter(shot=shot, modified_date__range=[start_date, end_date])
        client_version_serializer = ClientVersionsSerializer(client_version, many=True)
        client_version_json_dump = json.dumps(client_version_serializer.data)
        client_version_data = json.loads(client_version_json_dump)
        total_retakes += len(client_version_data)
    return shots, total_mandays, total_retakes

def assign_list(start_date, end_date, lead_id):
    lead = Assignments.objects.filter(lead_id=lead_id, assigned_date__range=[start_date, end_date
                                                                            ]).select_related('lead',
                                                                                              'shot',
                                                                                              'shot__sequence',
                                                                                              'shot__sequence__project',
                                                                                              'shot__sequence__project__client',
                                                                                              'shot__status',
                                                                                              'shot__task_type',
                                                                                              'assigned_by',
                                                                                              'shot__artist',
                                                                                              'shot__team_lead')

    serializer = AssignmentSerializer(lead, many=True)
    json_dump = json.dumps(serializer.data)
    assign_data = json.loads(json_dump)
    length = len(assign_data)
    n = 0
    wip = 0
    completed = 0
    yts = 0
    total_mandays = 0
    while n < length:
        if assign_data[n]['shot']["status"]['code'] in ["YTS", "ATL"]:
            yts += 1

        if assign_data[n]['shot']["status"]['code'] in ["WIP", "STQ", "STC", "IRT", "LRT", "LAP"]:
            wip += 1

        if assign_data[n]['shot']["status"]['code'] in ["IAP", "DTC", "CAP"]:
            completed += 1

        total_mandays += assign_data[n]['shot']['bid_days']
        if n == length - 1:
            break
        n += 1

    return yts, wip, completed, total_mandays

def teamlead_sheet_download(buffer, start_date, end_date, lead_id):
    workbook = xlsxwriter.Workbook(buffer)
    data = getlogs(start_date, end_date, lead_id)
    assign_data = assign_list(start_date, end_date, lead_id)
    shot_list = data[0]
    total_shots = len(shot_list)
    worksheet = workbook.add_worksheet()

    bold = workbook.add_format({'bold': True, 'bg_color': '#43d3f7', 'border': 1, 'border_color': 'black'})
    pending_color = workbook.add_format({'bg_color': 'yellow', 'border': 1, 'border_color': 'black'})
    border = workbook.add_format({'border': 1, 'border_color': 'black'})
    # Add a number format for cells with percentage.
    percent = workbook.add_format({'num_format': '0.0%', 'border': 1, 'border_color': 'black'})

    # Write some data headers.
    worksheet.write('A10', 'CLIENT', bold)
    worksheet.write('B10', 'PROJECT', bold)
    worksheet.write('C10', 'SHOT CODE', bold)
    worksheet.write('D10', 'TOTAL FRAMES', bold)
    worksheet.write('E10', 'TASK', bold)
    worksheet.write('F10', 'STATUS', bold)
    worksheet.write('G10', 'BID DAYS', bold)
    worksheet.write('H10', 'WIP%', bold)
    worksheet.write('I10', 'ACHIEVED MANDAYS', bold)
    worksheet.write('J10', 'PENDING MANDAYS', bold)
    worksheet.write('K10', 'DUE DATE', bold)
    worksheet.write('L10', 'NOTES', bold)
    worksheet.write('M10', 'TEAM', bold)
    worksheet.write('N10', 'ARTIST NAME', bold)
    worksheet.write('O10', 'CLIENT VERSION', bold)
    worksheet.write('P10', 'QC VERSION', bold)
    worksheet.write('Q10', 'LEAD VERSION', bold)

    col = 0
    row = 9
    for shot_id in shot_list:
        try:
            shot = Shots.objects.select_related('sequence__project', 'sequence', 'sequence__project__client', 'status',
                                                'task_type', 'complexity').prefetch_related('status', 'complexity',
                                                                                            'sequence').get(id=shot_id)
            serializer = ShotsSerializer(shot)
            json_dump = json.dumps(serializer.data)
            shot_data = json.loads(json_dump)

            lead_version = ShotVersions.objects.select_related('status').filter(shot=shot_id).last()
            lead_version_serializer = ShotVersionsSerializer(lead_version)
            lead_version_json_dump = json.dumps(lead_version_serializer.data)
            lead_version_data = json.loads(lead_version_json_dump)

            qc_version = QCVersions.objects.select_related('status').filter(shot=shot_id).last()
            qc_version_serializer = QcVersionsSerializer(qc_version)
            qc_version_json_dump = json.dumps(qc_version_serializer.data)
            qc_version_data = json.loads(qc_version_json_dump)

            client_version = ClientVersions.objects.select_related('status').filter(shot=shot_id).last()
            client_version_serializer = ClientVersionsSerializer(client_version)
            client_version_json_dump = json.dumps(client_version_serializer.data)
            client_version_data = json.loads(client_version_json_dump)

            shot_status = shot_data['status']['code']
            if shot_data['status']['code'] in ['YTA', 'ATL', 'YTS']:
                shot_status = "YTS"
            elif shot_data['status']['code'] in ['WIP', 'STC', 'LRT']:
                shot_status = "WIP"
            elif shot_data['status']['code'] in ['STQ', 'IRT', 'LAP']:
                shot_status = "QC"
            elif shot_data['status']['code'] == "IAP":
                shot_status = "IAP"
            elif shot_data['status']['code'] == "CRT":
                shot_status = "RETAKE"

            if shot_data['type'] == "RETAKE":
                bid_days = 0
                percentile = 0
            else:
                bid_days = float(shot_data['bid_days'])
                percentile = shot_data['progress'] / 100

            bid_column = 'G{}'.format(row + 2)
            progress_column = 'H{}'.format(row + 2)
            total_frames = shot_data['actual_end_frame'] - shot_data['actual_start_frame'] + 1
            due_date = ""
            if shot_data['eta']:
                due_date = datetime.datetime.strptime(shot_data['eta'], '%Y-%m-%dT%H:%M:%S').strftime(
                    "%d-%m-%Y")

            worksheet.write(row + 1, col, shot_data['sequence']['project']['client']['name'], border)
            worksheet.write(row + 1, col + 1, shot_data['sequence']['project']['name'], border)
            worksheet.write(row + 1, col + 2, shot_data['name'], border)
            worksheet.write(row + 1, col + 3, str(total_frames), border)
            worksheet.write(row + 1, col + 4, shot_data['task_type'], border)
            worksheet.write(row + 1, col + 5, shot_status, border)
            worksheet.write(row + 1, col + 6, bid_days, border)
            worksheet.write(row + 1, col + 7, percentile, percent)
            worksheet.write(row + 1, col + 9, '=ROUND(({}-{}*{}),1)'.format(bid_column, bid_column, progress_column),
                            pending_color)
            worksheet.write(row + 1, col + 8, '=ROUND({}-{},1)'.format(bid_column, 'J{}'.format(row + 2), border))
            worksheet.write(row + 1, col + 10, due_date, border)
            worksheet.write(row + 1, col + 11, "", border)
            worksheet.write(row + 1, col + 12, shot_data['team_lead'], border)
            worksheet.write(row + 1, col + 13, shot_data['artist'], border)
            worksheet.write(row + 1, col + 14, client_version_data['version'], border)
            worksheet.write(row + 1, col + 15, qc_version_data['version'], border)
            worksheet.write(row + 1, col + 16, lead_version_data['version'], border)
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
    worksheet.merge_range('A1:Q1', 'PAINT TEAM', merge_format)
    worksheet.merge_range('A2:Q3', str(start_date) + "  ---  " + str(end_date), merge_format)
    worksheet.merge_range('A4:D6', "Total Shots : " + str(total_shots), fmerge_format)
    worksheet.merge_range('E4:G6', "Actual ManDays : " + str(round(assign_data[3])), fmerge_format)
    worksheet.merge_range('H4:J6', "Achieved ManDays : " + str(round(data[1])), fmerge_format)
    worksheet.merge_range('K4:M6', "Actual vs Achieved : " + str(round(assign_data[3] - data[1])), fmerge_format)
    worksheet.merge_range('N4:Q6', "Total Artists : 10", fmerge_format)

    worksheet.merge_range('A7:D8', "YTS : " + str(round(assign_data[0])), fmerge_format)
    worksheet.merge_range('E7:G8', "WIP : " + str(round(assign_data[1])), fmerge_format)
    worksheet.merge_range('H7:J8', "HOLD : 0", fmerge_format)
    worksheet.merge_range('K7:M8', "COMPLETED : " + str(round(assign_data[2])), fmerge_format)
    worksheet.merge_range('N7:Q8', "RETAKES : "+str(data[2]), fmerge_format)

    workbook.close()
    return buffer
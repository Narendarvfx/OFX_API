import datetime
import json

import xlsxwriter

from production.models import DayLogs, Assignments, Shots, ShotVersions, QCVersions, ClientVersions
from production.serializers import DayLogsSerializer, AssignmentSerializer, ShotsSerializer, ShotVersionsSerializer, \
    QcVersionsSerializer, ClientVersionsSerializer


def dept_sheet_download(buffer, start_date, end_date, dept):
    workbook = xlsxwriter.Workbook(buffer)

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
    shot_queryset = Shots.objects.select_related('sequence', 'task_type', 'sequence__project',
                                                 'sequence__project__client', 'status', 'complexity', 'team_lead',
                                                 'artist', 'location').filter(task_type__name=dept,
                                                                              creation_date__range=[start_date,
                                                                                                    end_date])
    shot_serializer = ShotsSerializer(shot_queryset, many=True)
    shot_data = shot_serializer.data
    length = len(shot_data)
    n = 0
    wip = 0
    completed = 0
    uploaded = 0
    yts = 0
    total_mandays = 0
    achieved_mandays = 0
    total_retakes = 0
    retakes_per = 0
    while n < length:
        if shot_data[n]["status"]['code'] in ["YTA", "YTS", "ATL"]:
            yts += 1

        if shot_data[n]["status"]['code'] in ["WIP", "STQ", "STC", "IRT", "LRT", "LAP"]:
            wip += 1

        if shot_data[n]["status"]['code'] in ["IAP", "DTC", "CAP"]:
            completed += 1

        if shot_data[n]["status"]['code'] == "DTC":
            uploaded += 1

        achieved_mandays += shot_data[n]['achieved_mandays']
        total_mandays += shot_data[n]['bid_days']

        client_version = ClientVersions.objects.select_related('shot', 'sent_by', 'verified_by', 'status').filter(
            shot=shot_data[n]['id'],
            modified_date__range=[start_date,
                                  end_date])
        client_version_serializer = ClientVersionsSerializer(client_version, many=True)
        client_version_data = client_version_serializer.data
        total_retakes += len(client_version_data)
        if n == length - 1:
            break
        n += 1

        lead_version = ShotVersions.objects.select_related('status', 'sent_by', 'verified_by').filter(
            shot=shot_data[n]['id']).last()
        lead_version_serializer = ShotVersionsSerializer(lead_version)
        lead_version_json_dump = json.dumps(lead_version_serializer.data)
        lead_version_data = json.loads(lead_version_json_dump)

        qc_version = QCVersions.objects.select_related('status', 'sent_by', 'verified_by').filter(shot=shot_data[n]['id']).last()
        qc_version_serializer = QcVersionsSerializer(qc_version)
        qc_version_json_dump = json.dumps(qc_version_serializer.data)
        qc_version_data = json.loads(qc_version_json_dump)

        client_version = ClientVersions.objects.select_related('status', 'sent_by', 'verified_by').filter(
            shot=shot_data[n]['id']).last()
        client_version_serializer = ClientVersionsSerializer(client_version)
        client_version_json_dump = json.dumps(client_version_serializer.data)
        client_version_data = json.loads(client_version_json_dump)

        shot_status = shot_data[n]['status']['code']
        if shot_data[n]['status']['code'] in ['YTA', 'ATL', 'YTS']:
            shot_status = "YTS"
        elif shot_data[n]['status']['code'] in ['WIP', 'STC', 'LRT']:
            shot_status = "WIP"
        elif shot_data[n]['status']['code'] in ['STQ', 'IRT', 'LAP']:
            shot_status = "QC"
        elif shot_data[n]['status']['code'] == "IAP":
            shot_status = "IAP"
        elif shot_data[n]['status']['code'] == "CRT":
            shot_status = "RETAKE"

        if shot_data[n]['type'] == "RETAKE":
            bid_days = 0
            percentile = 0
        else:
            bid_days = float(shot_data[n]['bid_days'])
            percentile = shot_data[n]['progress'] / 100

        bid_column = 'G{}'.format(row + 2)
        progress_column = 'H{}'.format(row + 2)
        total_frames = shot_data[n]['actual_end_frame'] - shot_data[n]['actual_start_frame'] + 1
        due_date = ""
        if shot_data[n]['eta']:
            due_date = datetime.datetime.strptime(shot_data[n]['eta'], '%Y-%m-%dT%H:%M:%S').strftime(
                "%d-%m-%Y")

        worksheet.write(row + 1, col, shot_data[n]['sequence']['project']['client']['name'], border)
        worksheet.write(row + 1, col + 1, shot_data[n]['sequence']['project']['name'], border)
        worksheet.write(row + 1, col + 2, shot_data[n]['name'], border)
        worksheet.write(row + 1, col + 3, str(total_frames), border)
        worksheet.write(row + 1, col + 4, shot_data[n]['task_type'], border)
        worksheet.write(row + 1, col + 5, shot_status, border)
        worksheet.write(row + 1, col + 6, bid_days, border)
        worksheet.write(row + 1, col + 7, percentile, percent)
        worksheet.write(row + 1, col + 9, '=ROUND(({}-{}*{}),1)'.format(bid_column, bid_column, progress_column),
                        pending_color)
        worksheet.write(row + 1, col + 8, '=ROUND({}-{},1)'.format(bid_column, 'J{}'.format(row + 2), border))
        worksheet.write(row + 1, col + 10, due_date, border)
        worksheet.write(row + 1, col + 11, "", border)
        worksheet.write(row + 1, col + 12, shot_data[n]['team_lead'], border)
        worksheet.write(row + 1, col + 13, shot_data[n]['artist'], border)
        worksheet.write(row + 1, col + 14, client_version_data['version'], border)
        worksheet.write(row + 1, col + 15, qc_version_data['version'], border)
        worksheet.write(row + 1, col + 16, lead_version_data['version'], border)

        row += 1

    act_vs_ach = total_mandays - achieved_mandays
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
    worksheet.merge_range('A1:Q1', '{} DEPARTMENT REPORT'.format(dept), merge_format)
    worksheet.merge_range('A2:Q3', str(start_date) + "  ---  " + str(end_date), merge_format)
    worksheet.merge_range('A4:D6', "Total Shots : " + str(length), fmerge_format)
    worksheet.merge_range('E4:G6', "Actual ManDays : " + str(round(total_mandays)), fmerge_format)
    worksheet.merge_range('H4:J6', "Achieved ManDays : " + str(round(achieved_mandays)), fmerge_format)
    worksheet.merge_range('K4:M6', "Actual vs Achieved : " + str(round(act_vs_ach)), fmerge_format)
    worksheet.merge_range('N4:Q6', "Total Artists : 10", fmerge_format)

    worksheet.merge_range('A7:D8', "YTS : " + str(round(yts)), fmerge_format)
    worksheet.merge_range('E7:G8', "WIP : " + str(round(wip)), fmerge_format)
    worksheet.merge_range('H7:J8', "HOLD : 0", fmerge_format)
    worksheet.merge_range('K7:M8', "COMPLETED : " + str(round(completed)), fmerge_format)
    worksheet.merge_range('N7:Q8', "RETAKES : " + str(total_retakes), fmerge_format)

    workbook.close()
    return buffer
import datetime
import json
from itertools import groupby

import xlsxwriter

from production.models import Shots
from production.serializers import ShotsSerializer


def reports_sheet_export(buffer, client_id, project_id, task_type=None):
    workbook = xlsxwriter.Workbook(buffer)
    if task_type:
        shot_data = Shots.objects.filter(sequence__project__client_id=client_id, sequence__project_id=project_id, task_type__name=task_type)
    else:
        shot_data = Shots.objects.filter(sequence__project__client_id=client_id, sequence__project_id=project_id)
    serializer = ShotsSerializer(shot_data, many=True)
    dataa = json.dumps(serializer.data)
    fuck = json.loads(dataa)
    worksheet = workbook.add_worksheet()
    write_to_excel(workbook, worksheet, fuck)
    workbook.close()
    return buffer

def write_to_excel(workbook, worksheet, shots_data):
    # Add a bold format to use to highlight cells.
    bold = workbook.add_format({'bold': True, 'bg_color': '#43d3f7', 'border': 1, 'border_color': 'black'})
    pending_color = workbook.add_format({'bg_color': 'yellow', 'border': 1, 'border_color': 'black'})
    border = workbook.add_format({'border': 1, 'border_color': 'black'})
    # Add a number format for cells with money.
    percent = workbook.add_format({'num_format': '0.0%', 'border': 1, 'border_color': 'black'})

    # Write some data headers.
    worksheet.write('A1', 'SHOW', bold)
    worksheet.write('B1', 'BID PACK', bold)
    worksheet.write('C1', 'SHOT CODE', bold)
    worksheet.write('D1', 'TASK', bold)
    worksheet.write('E1', 'STATUS', bold)
    worksheet.write('F1', 'VERSION', bold)
    worksheet.write('G1', 'SUBMISSION DATE', bold)
    worksheet.write('H1', 'DELIVERY DATE', bold)
    worksheet.write('I1', 'VENDOR NOTES', bold)

    # # Start from the first cell below the headers.
    col = 0
    row = 0
    for shot_data in shots_data:
        shot_status = shot_data['status']['code']
        if shot_data['status']['code'] in ['YTA', 'ATL', 'YTS']:
            shot_status = "YET T0 START"
        elif shot_data['status']['code'] in ['WIP', 'STC', 'STQ', 'IRT']:
            shot_status = "IN PROGRESS"
        elif shot_data['status']['code'] == "IAP":
            shot_status = "INTERNAL APPROVED"
        elif shot_data['status']['code'] == "CRT":
            shot_status = "RETAKE"
        elif shot_data['status']['code'] == "DTC":
            shot_status = "SENT TO CLIENT"

        if shot_data['eta']:
            due_date = datetime.datetime.strptime(shot_data['eta'], '%Y-%m-%dT%H:%M:%S').strftime(
                "%d-%m-%Y")
        else:
            due_date = ""
        if shot_data['submitted_date']:
            submitted_date = datetime.datetime.strptime(shot_data['submitted_date'], '%Y-%m-%dT%H:%M:%S').strftime(
                "%d-%m-%Y")
        else:
            submitted_date = ""
        worksheet.write(row + 1, col, shot_data['sequence']['project']['name'], border)
        worksheet.write(row + 1, col + 1, shot_data['package_id'], border)
        worksheet.write(row + 1, col + 2, shot_data['name'], border)
        worksheet.write(row + 1, col + 3, shot_data['task_type'], border)
        worksheet.write(row + 1, col + 4, shot_status, border)
        worksheet.write(row + 1, col + 5, shot_data['version'], border)
        worksheet.write(row + 1, col + 6, submitted_date, border)
        worksheet.write(row + 1, col + 7, due_date, percent)
        worksheet.write(row + 1, col + 8, "", border)
        row += 1
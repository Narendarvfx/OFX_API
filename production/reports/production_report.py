import datetime
import io
import json
import os

import requests
import xlsxwriter
from django.http import FileResponse
from requests import request, Response

from production.models import Shots
from production.serializers import ShotsSerializer


def get_data(dept):
    status_list = "YTA|ATL|YTS|WIP|STC|STQ|IRT|IAP|CRT"
    status = []
    for stat in status_list.split('|'):
        status.append(stat)
    shot = Shots.objects.select_related('sequence', 'task_type', 'sequence__project', 'sequence__project__client',
                                        'status', 'complexity', 'team_lead', 'artist').filter(status__code__in=status,
                                                                                              task_type__name=dept)
    serializer = ShotsSerializer(shot, many=True)
    # print(json.dumps(serializer.data))
    dataa = json.dumps(serializer.data)
    return json.loads(dataa)

def create_workbook(buffer):
    workbook = xlsxwriter.Workbook(buffer)
    for dept in ['PAINT', 'ROTO', 'MM']:
        shots_data = get_data(dept)
        worksheet = workbook.add_worksheet(dept)
        write_to_excel(workbook, worksheet, shots_data)

    workbook.close()
    return buffer


def write_to_excel(workbook, worksheet, shots_data):
    print("ShotsData:", type(shots_data))
    # Add a bold format to use to highlight cells.
    bold = workbook.add_format({'bold': True, 'bg_color': '#43d3f7', 'border': 1, 'border_color': 'black'})
    pending_color = workbook.add_format({'bg_color': 'yellow', 'border': 1, 'border_color': 'black'})
    border = workbook.add_format({'border': 1, 'border_color': 'black'})
    # Add a number format for cells with percentage.
    percent = workbook.add_format({'num_format': '0.0%', 'border': 1, 'border_color': 'black'})

    # Write some data headers.
    worksheet.write('A1', 'CLIENT', bold)
    worksheet.write('B1', 'PROJECT', bold)
    worksheet.write('C1', 'SHOT CODE', bold)
    worksheet.write('D1', 'TOTAL FRAMES', bold)
    worksheet.write('E1', 'TASK', bold)
    worksheet.write('F1', 'STATUS', bold)
    worksheet.write('G1', 'BID DAYS', bold)
    worksheet.write('H1', 'WIP%', bold)
    worksheet.write('I1', 'DUE MANDAYS', bold)
    worksheet.write('J1', 'DUE DATE', bold)
    worksheet.write('K1', 'NOTES', bold)
    worksheet.write('L1', 'TEAM', bold)
    worksheet.write('M1', 'ARTIST NAME', bold)
    worksheet.write('N1', 'IN DATE', bold)
    worksheet.write('O1', 'PACKAGE ID', bold)
    worksheet.write('P1', 'ESTIMATE ID', bold)
    worksheet.write('Q1', 'ESTIMATE DATE', bold)
    worksheet.write('R1', 'LOCATION', bold)

    # # Start from the first cell below the headers.
    col = 0
    row = 0
    for shot_data in shots_data:
        print(shot_data)
        shot_status = shot_data['status']['code']
        if shot_data['status']['code'] in ['YTA', 'ATL', 'YTS']:
            shot_status = "YTS"
        elif shot_data['status']['code'] in ['WIP', 'STC']:
            shot_status = "WIP"
        elif shot_data['status']['code'] in ['STQ', 'IRT']:
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
        if shot_data['eta']:
            due_date = datetime.datetime.strptime(shot_data['eta'], '%Y-%m-%dT%H:%M:%S').strftime(
                "%d-%m-%Y")
        else:
            due_date = ""
        worksheet.write(row + 1, col, shot_data['sequence']['project']['client']['name'], border)
        worksheet.write(row + 1, col + 1, shot_data['sequence']['project']['name'], border)
        worksheet.write(row + 1, col + 2, shot_data['name'], border)
        worksheet.write(row + 1, col + 3, str(total_frames), border)
        worksheet.write(row + 1, col + 4, shot_data['task_type'], border)
        worksheet.write(row + 1, col + 5, shot_status, border)
        worksheet.write(row + 1, col + 6, bid_days, border)
        worksheet.write(row + 1, col + 7, percentile, percent)
        worksheet.write(row + 1, col + 8,
                        '=ROUND(({}-{}*{}),1)'.format(bid_column, bid_column, progress_column), pending_color)
        worksheet.write(row + 1, col + 9, due_date, border)
        worksheet.write(row + 1, col + 10, " ", border)
        worksheet.write(row + 1, col + 11, shot_data['team_lead'], border)
        worksheet.write(row + 1, col + 12, shot_data['artist'], border)
        in_date = datetime.datetime.strptime(shot_data['creation_date'], '%Y-%m-%dT%H:%M:%S.%f').strftime(
            "%d-%m-%Y")
        worksheet.write(row + 1, col + 13, in_date, border)
        worksheet.write(row + 1, col + 14, shot_data['package_id'], border)
        worksheet.write(row + 1, col + 15, shot_data['estimate_id'], border)
        if shot_data['estimate_date']:
            estimate_date = datetime.datetime.strptime(shot_data['estimate_date'], '%Y-%m-%dT%H:%M:%S').strftime(
                "%d-%m-%Y")
        else:
            estimate_date = ""
        worksheet.write(row + 1, col + 16, estimate_date, border)
        worksheet.write(row + 1, col + 17, shot_data['sequence']['project']['client']['location'], border)
        row += 1
# write_to_excel()

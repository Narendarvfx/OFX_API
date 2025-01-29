#  Copyright (c) 2023.
#  Designed & Developed by Narendar Reddy G, OscarFX Private Limited
#  All rights reserved.

import datetime
import io
import json
import os
from itertools import groupby

import requests
import xlsxwriter
from django.http import FileResponse
from requests import request, Response

from production.models import Shots, DayLogs, ShotVersions, QCVersions
from production.serializers import ShotsSerializer, DayLogsSerializer, AllShotVersionsSerializer, \
    AllShotQcVersionsSerializer


def teamlead_sheet_export(buffer, start_date, end_date, lead_id):
    workbook = xlsxwriter.Workbook(buffer)

    daylogs = DayLogs.objects.filter(updated_date__range=[start_date, end_date], shot__team_lead=lead_id)
    serializer = DayLogsSerializer(daylogs, many=True)
    dataa = json.dumps(serializer.data)
    fuck = json.loads(dataa)
    fuck.sort(key=lambda content: content['shot'])

    # then use groupby with the same key
    groups = groupby(fuck, lambda content: content['shot'])
    dictt = []
    for shot, group in groups:

        ss = [sum(f['consumed_man_day'] for f in group)]
        l_version = ""
        qc_version = ""
        try:
            lead_ver = ShotVersions.objects.filter(shot = shot).select_related('status').latest('modified_date')
            l_serializer = AllShotVersionsSerializer(lead_ver)
            l_ver_dat = json.dumps(l_serializer.data)
            lead_ver_data = json.loads(l_ver_dat)
            if lead_ver:
                l_version = lead_ver_data['version']
        except:
            pass
        try:
            qc_ver = QCVersions.objects.filter(shot=shot).select_related('status').latest('modified_date')
            q_serializer = AllShotQcVersionsSerializer(qc_ver)
            q_ver_dat = json.dumps(q_serializer.data)
            qc_ver_data = json.loads(q_ver_dat)
            if qc_ver:
                qc_version = qc_ver_data['version']
        except:
            pass
        dat = {
            'shot': shot,
            'consumed_manday': ss,
            'l_version': l_version,
            'qc_version': qc_version
        }
        dictt.append(dat)
    worksheet = workbook.add_worksheet()
    write_to_excel(workbook, worksheet, dictt, start_date, end_date)
    workbook.close()
    return buffer


def write_to_excel(workbook, worksheet, shots_data, start_date, end_date):
    merge_format = workbook.add_format({
        'bold': 1,
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'fg_color': 'yellow'})

    # Merge 3 cells.
    worksheet.merge_range('A1:Q1', 'PAINT TEAM', merge_format)
    worksheet.merge_range('A2:Q3', str(start_date) +"  ---  "+ str(end_date), merge_format)
    # Add a bold format to use to highlight cells.
    bold = workbook.add_format({'bold': True, 'bg_color': '#43d3f7', 'border': 1, 'border_color': 'black'})
    pending_color = workbook.add_format({'bg_color': 'yellow', 'border': 1, 'border_color': 'black'})
    border = workbook.add_format({'border': 1, 'border_color': 'black'})
    # Add a number format for cells with money.
    percent = workbook.add_format({'num_format': '0.0%', 'border': 1, 'border_color': 'black'})

    # Write some data headers.
    worksheet.write('A5', 'CLIENT', bold)
    worksheet.write('B5', 'PROJECT', bold)
    worksheet.write('C5', 'SHOT', bold)
    worksheet.write('D5', 'TOTAL FRAMES', bold)
    worksheet.write('E5', 'TASK', bold)
    worksheet.write('F5', 'STATUS', bold)
    worksheet.write('G5', 'BID DAYS', bold)
    worksheet.write('H5', 'WIP%', bold)
    worksheet.write('I5', 'ACHIEVED MANDAYS', bold)
    worksheet.write('J5', 'PENDING MANDAYS', bold)
    worksheet.write('K5', 'DUE DATE', bold)
    worksheet.write('L5', 'NOTES', bold)
    worksheet.write('M5', 'TEAM', bold)
    worksheet.write('N5', 'ARTIST NAME', bold)
    worksheet.write('O5', 'CLIENT VERSION', bold)
    worksheet.write('P5', 'QC VERSION', bold)
    worksheet.write('Q5', 'LEAD VERSION', bold)

    # # Start from the first cell below the headers.
    col = 0
    row = 0
    for dat in shots_data:
        shot = Shots.objects.get(id=dat['shot'])
        serializer = ShotsSerializer(shot)
        # print(json.dumps(serializer.data))
        dataa = json.dumps(serializer.data)
        shot_data = json.loads(dataa)
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
        bid_column = 'G{}'.format(row + 7)
        progress_column = 'H{}'.format(row + 7)
        total_frames = shot_data['actual_end_frame'] - shot_data['actual_start_frame'] + 1
        if shot_data['eta']:
            due_date = datetime.datetime.strptime(shot_data['eta'], '%Y-%m-%dT%H:%M:%S').strftime(
                "%d-%m-%Y")
        else:
            due_date = ""
        worksheet.write(row + 5, col, shot_data['sequence']['project']['client']['name'], border)
        worksheet.write(row + 5, col + 1, shot_data['sequence']['project']['name'], border)
        worksheet.write(row + 5, col + 2, shot_data['name'], border)
        worksheet.write(row + 5, col + 3, str(total_frames), border)
        worksheet.write(row + 5, col + 4, shot_data['task_type'], border)
        worksheet.write(row + 5, col + 5, shot_status, border)
        worksheet.write(row + 5, col + 6, bid_days, border)
        worksheet.write(row + 5, col + 7, percentile, percent)
        worksheet.write(row + 5, col + 8, str(dat['consumed_manday'][0]), border)
        worksheet.write(row + 5, col + 9,
                        '=ROUND(({}-{}*{}),1)'.format(bid_column, bid_column, progress_column), pending_color)
        worksheet.write(row + 5, col + 10, due_date, border)
        worksheet.write(row + 5, col + 11, " ", border)
        worksheet.write(row + 5, col + 12, shot_data['team_lead'], border)
        worksheet.write(row + 5, col + 13, shot_data['artist'], border)
        worksheet.write(row + 5, col + 14, shot_data['version'], border)
        worksheet.write(row + 5, col + 15, dat['qc_version'], border)
        worksheet.write(row + 5, col + 16, dat['l_version'], border)

        row += 1
# write_to_excel()

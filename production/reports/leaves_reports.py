import datetime
from datetime import timedelta
import json

import xlsxwriter
from OFX_API import apiRequestManager
from hrm.models import Leaves


def leaves_sheet_download(buffer=None, from_date=None, to_date=None, leaves_ids=[]):
    apiRequestManagers = apiRequestManager()
    leaveslogs = apiRequestManagers.getDBData(model=Leaves, queryFilter={"targetDate__range": [from_date, to_date],
                                                                            "id__in": leaves_ids},
                                            select_related=['employee','sessionFrom','sessionFrom'],
                                            queryPerams=['id','employee__id','employee__fullName','employee__employee_id','employee__role__id','employee__role__name','employee__department__id','employee__department__name','targetDate', 'dateFrom', 'dateTo', 'leaveType','requestedOn', 'sessionFrom__id','sessionFrom__sessionType','sessionTo__id','sessionTo__sessionType', 'status','modifiedDate']);


    workbook = xlsxwriter.Workbook(buffer)
    worksheet = workbook.add_worksheet()
    bold = workbook.add_format({'bold': True, 'border': 1, 'border_color': 'black'})
    border = workbook.add_format({'border': 1, 'border_color': 'black'})
    worksheet.write('A1', 'DATE', bold)
    worksheet.write('B1', 'EMPLOYEE ID', bold)
    worksheet.write('C1', 'EMPLOYEE NAME', bold)
    worksheet.write('D1', 'ROLE', bold)
    worksheet.write('E1', 'DEPARTMENT', bold)
    worksheet.write('F1', 'FROM', bold)
    worksheet.write('G1', 'TO', bold)
    worksheet.write('H1', 'LEAVE TYPE', bold),
    worksheet.write('I1', 'SESSION FROM', bold),
    worksheet.write('J1', 'SESSION TO', bold),
    worksheet.write('K1', 'REQUESTED DATE', bold),
    worksheet.write('L1', 'STATUS', bold),
    worksheet.write('M1', 'MODIFIED DATE', bold),
    p = 1
    i = 0
    for data in leaveslogs:
        reqsdate =data['requestedOn'].split(' ')[0]
        worksheet.write(i + p, 0,datetime.datetime.strptime(str(data['targetDate']), '%Y-%m-%d %H:%M:%S').strftime("%d-%m-%Y"), border)
        worksheet.write(i + p, 1, data['employee']['employee_id'], border)
        worksheet.write(i + p, 2, data['employee']['fullName'], border)
        worksheet.write(i + p, 3, data['employee']['role']['name'] if data['employee']['role'] is not None else 'N/A', border)
        worksheet.write(i + p, 4, data['employee']['department']['name'] if data['employee']['department'] is not None else 'N/A', border)
        worksheet.write(i + p, 5, datetime.datetime.strptime(str(data['dateFrom']), '%Y-%m-%d %H:%M:%S').strftime("%d-%m-%Y"), border),
        worksheet.write(i + p, 6, datetime.datetime.strptime(str(data['dateTo']), '%Y-%m-%d %H:%M:%S').strftime("%d-%m-%Y"), border),
        worksheet.write(i + p, 7, data['leaveType'] if data['leaveType'] is not None else 'N/A', border),
        worksheet.write(i + p, 8, data['sessionFrom']['sessionType'] if data['sessionFrom'] is not None else 'N/A', border)
        worksheet.write(i + p, 9, data['sessionTo']['sessionType'] if data['sessionTo'] is not None else 'N/A', border)
        worksheet.write(i + p, 10, reqsdate, border)
        worksheet.write(i + p, 11,data['status'] if data['status'] is not None else 'N/A', border)
        worksheet.write(i + p, 12, datetime.datetime.strptime(str(data['modifiedDate']), '%Y-%m-%d %H:%M:%S.%f').strftime("%d-%m-%Y"), border)
        i += 1

    workbook.close()
    return buffer
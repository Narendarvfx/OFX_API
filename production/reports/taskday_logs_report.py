import datetime
from datetime import timedelta
import json

import xlsxwriter
from OFX_API import apiRequestManager
from production.models import TaskDayLogs
def storeDate(_datetime=None):
    _posibs = ['%Y-%m-%d','%Y-%m-%d %H:%M:%S','%Y-%m-%d %H:%M:%S.%f','%Y-%m-%dT%H:%M:%S.%f']
    for pb in _posibs:
        try:
            return datetime.datetime.strptime(_datetime,pb)
        except:
            pass
    return None
def taskday_logs_sheet_download(buffer=None, from_date=None, to_date=None, logs_ids=[]):
    apiRequestManagers = apiRequestManager()
    tasklogs = apiRequestManagers.getDBData(model=TaskDayLogs, queryFilter={"updated_date__range":[from_date, to_date],"id__in": logs_ids},
                                            select_related=['task','artist','updated_by'],
                                            queryPerams=['id', "task__id","task__shot__id", "task__shot__name", "task__artist__id",
                                                         "task__artist__fullName","task_biddays","updated_task_biddays","percentage",
                                                         "day_percentage", "consumed_man_day","artist__id","artist__fullName","artist__employee_id","updated_by__id",
                                                         "updated_by__fullName","updated_by__employee_id", "updated_date","last_updated_date"])

    workbook = xlsxwriter.Workbook(buffer)
    worksheet = workbook.add_worksheet()
    bold = workbook.add_format({'bold': True, 'border': 1, 'border_color': 'black'})
    border = workbook.add_format({'border': 1, 'border_color': 'black'})
    worksheet.write('A1', 'DATE', bold)
    worksheet.write('B1', 'CREATED BY', bold)
    worksheet.write('C1', 'TASK BID DAYS', bold)
    worksheet.write('D1', 'CONSUMED MAN-DAYS', bold)
    worksheet.write('E1', 'ARTIST PERCENTAGE', bold)
    worksheet.write('F1', 'DAY PERCENTAGE', bold)
    worksheet.write('G1', 'UPDATED BY', bold)
    worksheet.write('H1', 'LAST UPDATE', bold)
    p = 1
    i = 0
    for data in tasklogs:
        worksheet.write(i + p, 0, datetime.datetime.strptime(str(data['updated_date']), '%Y-%m-%d %H:%M:%S.%f').strftime( "%d-%m-%Y"), border)
        worksheet.write(i + p, 1, data['artist']['fullName'], border)
        worksheet.write(i + p, 2, data['task_biddays'] if data['task_biddays'] is not None else 'N/A', border)
        worksheet.write(i + p, 3, data['consumed_man_day'] if data['consumed_man_day'] is not None else 'N/A', border)
        worksheet.write(i + p, 4, data['percentage'] if data['percentage'] is not None else 'N/A', border)
        worksheet.write(i + p, 5, data['day_percentage'] if data['day_percentage'] is not None else 'N/A',border)
        worksheet.write(i + p, 6, data['updated_by']['fullName'] if data['updated_by'] is not None else 'N/A', border)
        worksheet.write(i + p, 7,datetime.datetime.strptime(str(data['last_updated_date']), '%Y-%m-%d %H:%M:%S.%f').strftime( "%d-%m-%Y"), border)
        i += 1

    workbook.close()
    return buffer

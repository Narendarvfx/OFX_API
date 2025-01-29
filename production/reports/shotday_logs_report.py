import datetime
from datetime import timedelta
import json
import xlsxwriter
from production.models import DayLogs
from OFX_API import apiRequestManager
def storeDate(_datetime=None):
    _posibs = ['%Y-%m-%d','%Y-%m-%d %H:%M:%S','%Y-%m-%d %H:%M:%S.%f','%Y-%m-%dT%H:%M:%S.%f']
    for pb in _posibs:
        try:
            return datetime.datetime.strptime(_datetime,pb)
        except:
            pass
    return None
def shotday_logs_sheet_download(buffer=None, from_date=None, to_date=None, shot_ids=[]):
    apiRequestManagers = apiRequestManager()
    shotData = apiRequestManagers.getDBData(model=DayLogs, queryFilter={"updated_date__range": [from_date, to_date],
                                                                        "id__in": shot_ids},
                                            select_related=['department'],
                                            queryPerams=["id", "shot__id", "shot__name", "shot_biddays",
                                                         "updated_shot_biddays", "percentage",
                                                         "day_percentage", "consumed_man_day", "artist__id",
                                                         "artist__fullName", "artist__role__id",
                                                         "artist__role__name", "artist__department__id",
                                                         "artist__department__name",
                                                         "updated_by__id", "updated_by__fullName",
                                                         "updated_by__employee_id", "updated_date",
                                                         "last_updated_date"])
    workbook = xlsxwriter.Workbook(buffer)
    worksheet = workbook.add_worksheet()
    bold = workbook.add_format({'bold': True, 'border': 1, 'border_color': 'black'})
    border = workbook.add_format({'border': 1, 'border_color': 'black'})
    worksheet.write('A1', 'DATE', bold)
    worksheet.write('B1', 'SHOT', bold)
    worksheet.write('C1', 'CREATED BY', bold)
    worksheet.write('D1', 'DEPARTMENT', bold)
    worksheet.write('E1', 'SHOT BID DAYS', bold)
    worksheet.write('F1', 'CONSUMED MAN-DAYS', bold)
    worksheet.write('G1', 'SHOT PERCENTAGE', bold)
    worksheet.write('H1', 'DAY PERCENTAGE', bold)
    worksheet.write('I1', 'UPDATED BY ', bold)
    worksheet.write('J1', 'LAST UPDATED ', bold)
    p = 1
    i = 0
    for data in shotData:
        worksheet.write(i + p, 0, datetime.datetime.strptime(str(data['updated_date']), '%Y-%m-%d %H:%M:%S.%f').strftime("%d-%m-%Y"), border)
        worksheet.write(i + p, 1, data['shot']['name'], border)
        worksheet.write(i + p, 2, data['artist']['fullName'], border)
        worksheet.write(i + p, 3, data['artist']['department']['name'] if data['artist']['department'] is not None else 'N/A', border)
        worksheet.write(i + p, 4, data['shot_biddays'], border)
        worksheet.write(i + p, 5, data['consumed_man_day'], border)
        worksheet.write(i + p, 6, data['percentage'], border)
        worksheet.write(i + p, 7, data['day_percentage'],border)
        worksheet.write(i + p, 8, data['updated_by']['fullName'] if data['updated_by'] is not None else 'N/A', border)
        worksheet.write(i + p, 9, datetime.datetime.strptime(str(data['last_updated_date']), '%Y-%m-%d %H:%M:%S.%f').strftime("%d-%m-%Y"), border)
        i += 1
    workbook.close()
    return buffer


#  Copyright (c) 2022-2023.
#  Designed & Developed by Narendar Reddy G, OscarFX Private Limited
#  All rights reserved.
import datetime
from datetime import timedelta
import json

import xlsxwriter
from OFX_API import apiRequestManager
from hrm.models import Employee, EmployeeRoleBinding
from production.models import DayLogs, Assignments, Shots
from production.serializers import ShotTimeLogSerializer
from ofx_statistics.models import LeadDailyStatistics, EmployeeDailyStatistics

def getfontcolor(value_range=100, value=10):
    try:
        set_value =(100 / value_range) * value
        if set_value<25:
            fg_color = "#f62d51"
        elif set_value<50:
            fg_color = "#f57b17"
        elif set_value<75:
            fg_color = "#009efb"
        elif set_value<90:
            fg_color = "#7460ee"
        else:
            fg_color = "#55ce63"
    except:
        fg_color = "#f62d51"
    return fg_color
def diffcolor(value1 =10, value2=10):
    pmd = value1-value2
    if pmd<0:
        return "#EA5455"
    elif pmd ==0:
        return "#0854c2"
    else:
        return "#28C76F"

def storeDate(_datetime=None):
    _posibs = ['%Y-%m-%d','%Y-%m-%d %H:%M:%S','%Y-%m-%d %H:%M:%S.%f','%Y-%m-%dT%H:%M:%S.%f']
    for pb in _posibs:
        try:
            return datetime.datetime.strptime(_datetime,pb)
        except:
            pass
    return None

def addDays(date='2022-01-04',days=1):
    return datetime.datetime.strptime(date,'%Y-%m-%d') + timedelta(days=days)
def daysRange(from_date='2022-01-04',to_date='2022-02-20'):
    return (datetime.datetime.strptime(to_date, '%Y-%m-%d') - datetime.datetime.strptime(from_date, '%Y-%m-%d')).days+1

def dateformate(date):
    return date if len(date.split('.')) > 1 else date + '.000000'
def storeDate(_datetime=None):
    _posibs = ['%Y-%m-%d','%Y-%m-%d %H:%M:%S','%Y-%m-%d %H:%M:%S.%f','%Y-%m-%dT%H:%M:%S.%f']
    for pb in _posibs:
        try:
            return datetime.datetime.strptime(_datetime,pb)
        except:
            pass
    return None

def export_tl_data_by_date(buffer=None, from_date=None, to_date=None, tlDat={}, atristStatistics={},shots=[]):
    workbook = xlsxwriter.Workbook(buffer)
    worksheet = {}
    worksheet['leadSheet'] = workbook.add_worksheet('LEAD SHEET')
    worksheet['leadReport'] = workbook.add_worksheet('LEAD REPORT')
    _range = daysRange(from_date=from_date, to_date=to_date)
    # formate = workbook.add_format({'bold': True, 'bg_color': '#43d3f7', 'border': 1, 'border_color': 'red'})
    # formate = workbook.add_format({'bold': True, 'bg_color': '#43d3f7', 'border': 1, 'border_color': 'red'})
    bold = workbook.add_format({'bold': True, 'border': 1, 'border_color': 'black'})
    border = workbook.add_format({'border': 1, 'border_color': 'black'})
    pending_color = workbook.add_format({'bg_color': 'yellow', 'border': 1, 'border_color': 'black'})
    # Add a number format for cells with percentage.
    percent = workbook.add_format({'num_format': '0.0%', 'border': 1, 'border_color': 'black'})
    merge_format = workbook.add_format({
        'bold': 1,
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'fg_color': 'yellow'})

    summary_format = workbook.add_format({
        'bold': 1,
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'fg_color': '#3cb0f0'
    })
    tmd = 0
    amd =0
    for i in tlDat['statistics']:
        tmd = tmd+float(i['tmd'])
        # amd  = amd+float(i['shot_amd'])
        amd  = amd+float(i['amd'])
    worksheet['leadSheet'].merge_range('A1:F3', "Name of Lead: {}".format(tlDat["fullName"]), merge_format)
    worksheet['leadSheet'].merge_range('G1:L3', "Employee.Id: {}".format(tlDat["employee_id"]), merge_format)
    worksheet['leadSheet'].merge_range('M1:R3', "Department: {}".format(tlDat["department"]['name']), merge_format)
    worksheet['leadSheet'].merge_range('S1:X3', 'Number Of Artists: {}'.format(str(tlDat["artistCount"])), merge_format)
    worksheet['leadSheet'].merge_range('A4:F6', "Team Ability: {}".format(str(round(tlDat["teamAbility"],2))), merge_format)
    worksheet['leadSheet'].merge_range('G4:L6',"Target Man Days: {}".format(str(round(tmd,2))), merge_format)
    worksheet['leadSheet'].merge_range('M4:R6', "Achieved Man Days: {}".format(str(round(amd,2))),merge_format)
    worksheet['leadSheet'].merge_range('S4:X6', "Difference: {}".format(str(round((amd - tmd),2))), merge_format)
    worksheet['leadSheet'].write('A7', 'CLIENT', bold)
    worksheet['leadSheet'].write('B7', 'PROJECT', bold)
    worksheet['leadSheet'].write('C7', 'SHOT CODE', bold)
    worksheet['leadSheet'].write('D7', 'TOTAL FRAMES', bold)
    worksheet['leadSheet'].write('E7', 'TASK', bold)
    worksheet['leadSheet'].write('F7', 'COMPLEXITY', bold)
    worksheet['leadSheet'].write('G7', 'STATUS', bold)
    worksheet['leadSheet'].write('H7', 'BID DAYS', bold)
    worksheet['leadSheet'].write('I7', 'WIP%', bold)
    worksheet['leadSheet'].write('J7', 'DUE MANDAYS', bold)
    worksheet['leadSheet'].write('K7', 'INTERNAL-ETA', bold)
    worksheet['leadSheet'].write('L7', 'CLIENT-ETA', bold)
    worksheet['leadSheet'].write('M7', 'NOTES', bold)
    worksheet['leadSheet'].write('N7', 'SUPERVISOR', bold)
    worksheet['leadSheet'].write('O7', 'TEAM LEAD', bold)
    worksheet['leadSheet'].write('P7', 'COMPILER', bold)
    worksheet['leadSheet'].write('Q7', 'ARTISTS', bold)
    worksheet['leadSheet'].write('R7', 'IN DATE', bold)
    worksheet['leadSheet'].write('S7', 'PACKAGE ID', bold)
    worksheet['leadSheet'].write('T7', 'ESTIMATE ID', bold)
    worksheet['leadSheet'].write('U7', 'ESTIMATE DATE', bold)
    worksheet['leadSheet'].write('V7', 'INTERNAL VERSION', bold)
    worksheet['leadSheet'].write('W7', 'CLIENT VERSION', bold)
    worksheet['leadSheet'].write('X7', 'LOCATION', bold)
    i = 0
    p = 7
    for shot_data in shots:
        shot_status = shot_data['status']['code']
        if shot_data['status']['code'] in ['YTA', 'ATL', 'YTS']:
            shot_status = "YTS"
        elif shot_data['status']['code'] in ['WIP', 'STC', 'LRT']:
            shot_status = "WIP"
        elif shot_data['status']['code'] in ['STQ', 'IRT', 'LAP']:
            shot_status = "QC"
        elif shot_data['status']['code'] == "CRT":
            shot_status = "RETAKE"

        if shot_data['type'] == "RETAKE":
            bid_days = 0
            percentile = 0
            shot_status = "RETAKE"
        else:
            bid_days = float(shot_data['bid_days'])
            percentile = shot_data['progress'] / 100

        bid_column = 'H{}'.format(i + 8)
        progress_column = 'I{}'.format(i + 8)
        total_frames = shot_data['actual_end_frame'] - shot_data['actual_start_frame'] + 1
        if shot_data['internal_eta']:
            due_date = datetime.datetime.strptime(dateformate(shot_data['internal_eta']), '%Y-%m-%dT%H:%M:%S.%f')
        else:
            due_date = ""
        if shot_data['eta']:
            client_eta_date = datetime.datetime.strptime(dateformate(shot_data['eta']), '%Y-%m-%dT%H:%M:%S.%f')
        else:
            client_eta_date = ""
        if shot_data['estimate_date']:
            estimate_date = datetime.datetime.strptime(dateformate(shot_data['estimate_date']), '%Y-%m-%dT%H:%M:%S.%f')
        else:
            estimate_date = ""
        date_format = workbook.add_format({'border': 1, 'border_color': 'black', 'num_format': 'dd/mm/yyyy'})
        in_date = datetime.datetime.strptime(dateformate(shot_data['creation_date']), '%Y-%m-%dT%H:%M:%S.%f')
        worksheet['leadSheet'].write(i+p, 0, shot_data['sequence']['project']['client']['name'], border)
        worksheet['leadSheet'].write(i+p, 1, shot_data['sequence']['project']['name'], border)
        worksheet['leadSheet'].write(i+p, 2, shot_data['name'], border)
        worksheet['leadSheet'].write(i+p, 3, str(total_frames), border)
        worksheet['leadSheet'].write(i+p, 4, shot_data['task_type'], border)
        worksheet['leadSheet'].write(i+p, 5, shot_data['complexity'], border)
        worksheet['leadSheet'].write(i+p, 6, shot_status, border)
        worksheet['leadSheet'].write(i+p, 7, bid_days, border)
        worksheet['leadSheet'].write(i+p, 8, percentile, percent)
        worksheet['leadSheet'].write(i+p, 9,'=ROUND(({}-{}*{}),1)'.format(bid_column, bid_column, progress_column), pending_color)
        worksheet['leadSheet'].write(i+p, 10, due_date, date_format)

        worksheet['leadSheet'].write(i+p, 11, client_eta_date, date_format)
        worksheet['leadSheet'].write(i+p, 12, " ", border)
        worksheet['leadSheet'].write(i+p, 13, shot_data['supervisor'], border)
        worksheet['leadSheet'].write(i+p, 14, shot_data['team_lead'], border)
        worksheet['leadSheet'].write(i+p, 15, shot_data['artist'], border)
        worksheet['leadSheet'].write(i+p, 16, ' '.join([str(elem['fullName'] + ",") for elem in shot_data['artists']]),
                        border)
        worksheet['leadSheet'].write(i+p, 17, in_date, date_format)
        worksheet['leadSheet'].write(i+p, 18, shot_data['package_id'], border)
        worksheet['leadSheet'].write(i+p, 19, shot_data['estimate_id'], border)
        worksheet['leadSheet'].write(i+p, 20, estimate_date, date_format)
        location = ""
        if shot_data['location']:
            location = shot_data['location']
        worksheet['leadSheet'].write(i+p, 21, "", border)
        worksheet['leadSheet'].write(i+p, 22, shot_data['version'], border)
        worksheet['leadSheet'].write(i+p, 23, location, border)
        i += 1

    worksheet['leadReport'].write('A1', 'DATE', bold)
    worksheet['leadReport'].write('B1', 'ARTISTS', bold)
    worksheet['leadReport'].write('C1', 'ARTISTS COUNT', bold)
    worksheet['leadReport'].write('D1', 'TOTAL PRESENT ARTISTS', bold)
    worksheet['leadReport'].write('E1', 'LEAVES', bold)
    worksheet['leadReport'].write('F1', 'TARGET MANDAYS', bold)
    worksheet['leadReport'].write('G1', 'ACHIVED MANDAYS', bold)
    worksheet['leadReport'].write('H1', 'DIFFERENCE', bold)
    
    p = 1
    i = 0
    _statistics = {}
    for x in tlDat["statistics"]:
        formtDateId = 'date_{date}'.format(date=datetime.datetime.strptime(x['logDate'], '%Y-%m-%d').strftime('%Y_%m_%d'))
        _statistics[formtDateId] = json.loads(json.dumps(x))
    for day in range(0,_range):
        thisDate = addDays(date=from_date, days=_range-(day+1))
        if thisDate.strftime('%Y-%m-%d') in tlDat["logDates"]:
            formtDateId = 'date_{date}'.format(date=thisDate.strftime('%Y_%m_%d'))
            worksheet['leadReport'].write(i + p, 0, _statistics[formtDateId]['logDate'],border)
            worksheet['leadReport'].write(i + p, 1, ', '.join([art['fullName'] for art in _statistics[formtDateId]['artists']]),border)
            worksheet['leadReport'].write(i + p, 2, _statistics[formtDateId]['artists_count'],border)
            worksheet['leadReport'].write(i + p, 3, _statistics[formtDateId]['total_workdays'],border)
            worksheet['leadReport'].write(i + p, 4, _statistics[formtDateId]['leaves'],border)
            worksheet['leadReport'].write(i + p, 5, _statistics[formtDateId]['tmd'],border)
            worksheet['leadReport'].write(i + p, 6, _statistics[formtDateId]['amd'],border)
            worksheet['leadReport'].write(i + p, 7, _statistics[formtDateId]['amd'] - _statistics[formtDateId]['tmd'],border)
            i += 1
    
    for day in range(0,_range):
        thisDate = addDays(date=from_date, days=_range-(day+1))
        if thisDate.strftime('%Y-%m-%d') in tlDat["logDates"]:
            formtDateId = 'date_{date}'.format(date=thisDate.strftime('%Y_%m_%d'))
            sheet_name = str(thisDate.strftime('%Y-%m-%d'))
            worksheet[formtDateId] = workbook.add_worksheet(sheet_name)
            worksheet[formtDateId].write('A1', 'EMPLOYEE ID', bold)
            worksheet[formtDateId].write('B1', 'EMPLOYEE NAME', bold)
            worksheet[formtDateId].write('C1', 'DEPARTMENT', bold)
            worksheet[formtDateId].write('D1', 'DESIGNATION', bold)
            worksheet[formtDateId].write('E1', 'DOJ', bold)
            worksheet[formtDateId].write('F1', 'DOE', bold)
            worksheet[formtDateId].write('G1', 'GRADE', bold)
            worksheet[formtDateId].write('H1', 'TARGET MANDAYS/DAY', bold)
            worksheet[formtDateId].write('I1', 'LEAVES', bold)
            worksheet[formtDateId].write('J1', 'TARGET MANDAYS ', bold)
            worksheet[formtDateId].write('K1', 'ACHIVED MANDAYS', bold)
            worksheet[formtDateId].write('L1', 'DIFFERENCE', bold)
            worksheet[formtDateId].write('M1', 'MISSING ETA', bold)
            worksheet[formtDateId].write('N1', 'REQUIRED WORKING HOURS', bold)
            worksheet[formtDateId].write('O1', 'AVALIABLE HOURS', bold)
            worksheet[formtDateId].write('P1', 'ACTIVE HOURS', bold)
            worksheet[formtDateId].write('Q1', 'LOCATION', bold)
            p = 1
            i = 0
            for x in list(atristStatistics.values()):
                if x.get(formtDateId,None) is not None:
                    _missETA = "N/A"
                    worksheet[formtDateId].write(i + p, 0, x[formtDateId]["employee"]["employee_id"],border)
                    worksheet[formtDateId].write(i + p, 1, x[formtDateId]["employee"]["fullName"],border)
                    worksheet[formtDateId].write(i + p, 2, x[formtDateId]["employee"]["department"]["name"],border)
                    worksheet[formtDateId].write(i + p, 3, x[formtDateId]["employee"]['role']['name'],border)
                    worksheet[formtDateId].write(i + p, 4,  storeDate(_datetime=x[formtDateId]["employee"]['creation_date']).strftime("%d-%m-%Y"),border)
                    worksheet[formtDateId].write(i + p, 5,  storeDate(_datetime=x[formtDateId]["employee"]['doe']).strftime("%d-%m-%Y") if x[formtDateId]["employee"]['doe'] is not None else "N/A",border)
                    worksheet[formtDateId].write(i + p, 6, x[formtDateId]["employee"]["grade"]["name"] if x[formtDateId]["employee"]['grade'] is not None and x[formtDateId]["employee"]['grade']['a_man_day'] is not None else 'N/A',border)
                    worksheet[formtDateId].write(i + p, 7, x[formtDateId]["employee"]['grade']['a_man_day'] if x[formtDateId]["employee"]['grade'] is not None and x[formtDateId]["employee"]['grade']['a_man_day'] is not None else 'N/A',border)
                    worksheet[formtDateId].write(i + p, 8, x[formtDateId]["leaves"],border)
                    worksheet[formtDateId].write(i + p, 9, x[formtDateId]["tmd"],border)
                    worksheet[formtDateId].write(i + p, 10, x[formtDateId]["amd"],border)
                    worksheet[formtDateId].write(i + p, 11, (x[formtDateId]["amd"]-x[formtDateId]["tmd"]),border)
                    worksheet[formtDateId].write(i + p, 12, _missETA,border)
                    worksheet[formtDateId].write(i + p, 13, x[formtDateId]["rwh"],border)
                    worksheet[formtDateId].write(i + p, 14, x[formtDateId]["aeh"],border)
                    worksheet[formtDateId].write(i + p, 15, x[formtDateId]["ash"],border)
                    worksheet[formtDateId].write(i + p, 16, x[formtDateId]["employee"]["location"]["name"] if x[formtDateId]["employee"]["location"] is not None else "GLOBAL",border)
                    i += 1
    workbook.close()
    return buffer

def export_tl_data_by_artist(buffer=None, from_date=None, to_date=None, tlDat={},atristStatistics={}, shots=[]):
    workbook = xlsxwriter.Workbook(buffer)
    worksheet = {}
    worksheet['leadSheet'] = workbook.add_worksheet('LEAD SHEET')
    # formate = workbook.add_format({'bold': True, 'bg_color': '#43d3f7', 'border': 1, 'border_color': 'red'})
    # formate = workbook.add_format({'bold': True, 'bg_color': '#43d3f7', 'border': 1, 'border_color': 'red'})
    bold = workbook.add_format({'bold': True, 'border': 1, 'border_color': 'black'})
    border = workbook.add_format({'border': 1, 'border_color': 'black'})
    pending_color = workbook.add_format({'bg_color': 'yellow', 'border': 1, 'border_color': 'black'})
    # Add a number format for cells with percentage.
    percent = workbook.add_format({'num_format': '0.0%', 'border': 1, 'border_color': 'black'})
    merge_format = workbook.add_format({
        'bold': 1,
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'fg_color': 'yellow'})

    summary_format = workbook.add_format({
        'bold': 1,
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'fg_color': '#3cb0f0'
    })
    tmd = 0
    amd = 0
    for i in tlDat['statistics']:
        tmd = tmd+float(i['tmd'])
        # amd  = amd+float(i['shot_amd'])
        amd  = amd+float(i['amd'])
    worksheet['leadSheet'].merge_range('A1:C3', "Name of Lead: {}".format(tlDat["fullName"]), merge_format)
    worksheet['leadSheet'].merge_range('D1:E3', "Employee.Id: {}".format(tlDat["employee_id"]), merge_format)
    worksheet['leadSheet'].merge_range('F1:G3', "Department: {}".format(tlDat["department"]['name']), merge_format)
    worksheet['leadSheet'].merge_range('H1:I3', 'Number Of Artists: {}"'.format(str(tlDat["artistCount"])),
                                       merge_format)
    worksheet['leadSheet'].merge_range('J1:K3', "Team Ability: {}".format(str(round(tlDat["teamAbility"], 2))),
                                       merge_format)
    worksheet['leadSheet'].merge_range('A4:C6', "Target Man Days: {}".format(str(round(tmd,2))), merge_format)
    worksheet['leadSheet'].merge_range('D4:F6', "Achieved Man Days: {}".format(str(round(amd,2))), merge_format)
    worksheet['leadSheet'].merge_range('G4:I6', "Difference: {}".format(str(round((amd - tmd), 2))), merge_format)
    worksheet['leadSheet'].write('A7', 'CLIENT', bold)
    worksheet['leadSheet'].write('B7', 'PROJECT', bold)
    worksheet['leadSheet'].write('C7', 'SHOT CODE', bold)
    worksheet['leadSheet'].write('D7', 'TOTAL FRAMES', bold)
    worksheet['leadSheet'].write('E7', 'TASK', bold)
    worksheet['leadSheet'].write('F7', 'COMPLEXITY', bold)
    worksheet['leadSheet'].write('G7', 'STATUS', bold)
    worksheet['leadSheet'].write('H7', 'BID DAYS', bold)
    worksheet['leadSheet'].write('I7', 'WIP%', bold)
    worksheet['leadSheet'].write('J7', 'DUE MANDAYS', bold)
    worksheet['leadSheet'].write('K7', 'INTERNAL-ETA', bold)
    worksheet['leadSheet'].write('L7', 'CLIENT-ETA', bold)
    worksheet['leadSheet'].write('M7', 'NOTES', bold)
    worksheet['leadSheet'].write('N7', 'SUPERVISOR', bold)
    worksheet['leadSheet'].write('O7', 'TEAM LEAD', bold)
    worksheet['leadSheet'].write('P7', 'COMPILER', bold)
    worksheet['leadSheet'].write('Q7', 'ARTISTS', bold)
    worksheet['leadSheet'].write('R7', 'IN DATE', bold)
    worksheet['leadSheet'].write('S7', 'PACKAGE ID', bold)
    worksheet['leadSheet'].write('T7', 'ESTIMATE ID', bold)
    worksheet['leadSheet'].write('U7', 'ESTIMATE DATE', bold)
    worksheet['leadSheet'].write('V7', 'INTERNAL VERSION', bold)
    worksheet['leadSheet'].write('W7', 'CLIENT VERSION', bold)
    worksheet['leadSheet'].write('X7', 'LOCATION', bold)
    i = 0
    p = 7
    for shot_data in shots:
        shot_status = shot_data['status']['code']
        if shot_data['status']['code'] in ['YTA', 'ATL', 'YTS']:
            shot_status = "YTS"
        elif shot_data['status']['code'] in ['WIP', 'STC', 'LRT']:
            shot_status = "WIP"
        elif shot_data['status']['code'] in ['STQ', 'IRT', 'LAP']:
            shot_status = "QC"
        elif shot_data['status']['code'] == "CRT":
            shot_status = "RETAKE"

        if shot_data['type'] == "RETAKE":
            bid_days = 0
            percentile = 0
            shot_status = "RETAKE"
        else:
            bid_days = float(shot_data['bid_days'])
            percentile = shot_data['progress'] / 100

        bid_column = 'H{}'.format(i + 2)
        progress_column = 'I{}'.format(i + 2)
        total_frames = shot_data['actual_end_frame'] - shot_data['actual_start_frame'] + 1
        if shot_data['internal_eta']:
            due_date = datetime.datetime.strptime(dateformate(shot_data['internal_eta']), '%Y-%m-%dT%H:%M:%S.%f')
        else:
            due_date = ""
        if shot_data['eta']:
            client_eta_date = datetime.datetime.strptime(dateformate(shot_data['eta']), '%Y-%m-%dT%H:%M:%S.%f')
        else:
            client_eta_date = ""
        if shot_data['estimate_date']:
            estimate_date = datetime.datetime.strptime(dateformate(shot_data['estimate_date']), '%Y-%m-%dT%H:%M:%S.%f')
        else:
            estimate_date = ""
        date_format = workbook.add_format({'border': 1, 'border_color': 'black', 'num_format': 'dd/mm/yyyy'})
        in_date = datetime.datetime.strptime(dateformate(shot_data['creation_date']), '%Y-%m-%dT%H:%M:%S.%f')
        worksheet['leadSheet'].write(i + p, 0, shot_data['sequence']['project']['client']['name'], border)
        worksheet['leadSheet'].write(i + p, 1, shot_data['sequence']['project']['name'], border)
        worksheet['leadSheet'].write(i + p, 2, shot_data['name'], border)
        worksheet['leadSheet'].write(i + p, 3, str(total_frames), border)
        worksheet['leadSheet'].write(i + p, 4, shot_data['task_type'], border)
        worksheet['leadSheet'].write(i + p, 5, shot_data['complexity'], border)
        worksheet['leadSheet'].write(i + p, 6, shot_status, border)
        worksheet['leadSheet'].write(i + p, 7, bid_days, border)
        worksheet['leadSheet'].write(i + p, 8, percentile, percent)
        worksheet['leadSheet'].write(i + p, 9,'=ROUND(({}-{}*{}),1)'.format(bid_column, bid_column, progress_column),
                                     pending_color)
        worksheet['leadSheet'].write(i + p, 10, due_date, date_format)

        worksheet['leadSheet'].write(i + p, 11, client_eta_date, date_format)
        worksheet['leadSheet'].write(i + p, 12, " ", border)
        worksheet['leadSheet'].write(i + p, 13, shot_data['supervisor'], border)
        worksheet['leadSheet'].write(i + p, 14, shot_data['team_lead'], border)
        worksheet['leadSheet'].write(i + p, 15, shot_data['artist'], border)
        worksheet['leadSheet'].write(i + p, 16,
                                     ' '.join([str(elem['fullName'] + ",") for elem in shot_data['artists']]),
                                     border)
        worksheet['leadSheet'].write(i + p, 17, in_date, date_format)
        worksheet['leadSheet'].write(i + p, 18, shot_data['package_id'], border)
        worksheet['leadSheet'].write(i + p, 19, shot_data['estimate_id'], border)
        worksheet['leadSheet'].write(i + p, 20, estimate_date, date_format)
        location = ""
        if shot_data['location']:
            location = shot_data['location']
        worksheet['leadSheet'].write(i + p, 21, "", border)
        worksheet['leadSheet'].write(i + p, 22, shot_data['version'], border)
        worksheet['leadSheet'].write(i + p, 23, location, border)
        i += 1
        # for i in range(0,tlData["artistCount"]):
    return buffer

def lead_sheet_download_2(buffer=None, from_date=None, to_date=None, tl_id=None, type='DATE', lead=None):
    '''
    type='ARTIST|DATE'
    '''
    apiRequestManagers = apiRequestManager()
    tlData = apiRequestManagers.getDBData(model=Employee, queryFilter={"id": tl_id}, select_related=['department'], queryPerams=["id", "fullName", "employee_id", "department__id", "department__name", "location__id", "location__name", "creation_date"])[0]
    if lead == 'HEAD OF DEPARTMENT':
        art_bind = []
        bindX = []
        _art_bind = apiRequestManagers.getDBData(model=EmployeeRoleBinding, queryFilter={ "employee__role__name":"VFX ARTIST","employee__department__name":tlData["department"]["name"],"employee__location__name":tlData['location']['name']}, select_related=['employee', 'role', 'employee__grade','employee__location', 'bindWith' ], queryPerams=["id", "employee__id", "employee__employee_id", "employee__grade__id", "employee__grade__a_man_day"])
        for x in _art_bind:
            if x['employee']['id'] not in bindX:
                bindX.append(x['employee']['id'])
                art_bind.append({
                    "id": x['id'],
                    "employee":{
                        "id": x['employee']['id'],
                        "employee_id": x['employee']['employee_id'],
                        "grade": x['employee']['grade'],
                        }
                    }.copy())
    else:
        art_bind = apiRequestManagers.getDBData(model=EmployeeRoleBinding,queryFilter={"bindWith__id": tl_id, "role__name": lead, "employee__role__name":"VFX ARTIST"},select_related=['employee', 'employee__role', 'role', 'employee__grade', 'bindWith'],queryPerams=["id", "employee__id", "employee__employee_id", "employee__grade__id", "employee__grade__a_man_day" ])
    tlData["artistCount"] = len(art_bind)
    tlData["teamAbility"] = 0
    for x in art_bind:
        if x['employee']['grade'] is not None and x['employee']['grade']['a_man_day'] is not None:
            tlData["teamAbility"] = tlData["teamAbility"] + x['employee']['grade']['a_man_day']
    
    tlData["statistics"] = apiRequestManagers.getDBData(model=LeadDailyStatistics,queryFilter={"logDate__range": [from_date, to_date], "lead__id": tl_id},select_related=['lead'],queryPerams=['id', "artists__id","artists__fullName","artists_count","total_workdays",'tmd', 'amd', 'shot_amd', 'leaves', 'logDate'])
    if lead == 'HEAD OF DEPARTMENT':
        shotlogdata = apiRequestManagers.getDBData(model=DayLogs,queryFilter={"updated_date__range": [from_date, to_date],"shot__task_type__name": tlData["department"]["name"],"shot__location__name":tlData['location']['name']},select_related=['shot','shot__task_type','shot__location','artist','updated_by'],queryPerams=['id', "shot__id"])
        _rUniq = []
        shots_tlData = []
        for x in shotlogdata:
            if x['shot']['id'] not in _rUniq:
                _rUniq.append(x['shot']['id'])
                shots_tlData.append({
                    'id':x['shot']['id'],
                    "shot":{ "id": x['shot']['id']}
                    }.copy())    
    else:
        shotlogdata = apiRequestManagers.getDBData(model=DayLogs,queryFilter={"updated_date__range": [from_date, to_date]},select_related=['shot','artist','updated_by'],queryPerams=['id', "shot__id"])
        shots_tlData = apiRequestManagers.getDBData(model=Assignments, queryFilter={"shot__id__in": [x['shot']['id'] for x in shotlogdata], "lead__id": tl_id}, select_related=['lead','shot', 'assigned_by'],queryPerams=['id', "shot__id"])
    shots_data = json.loads(json.dumps(ShotTimeLogSerializer(instance=Shots.objects.prefetch_related('timelogs', 'artists').select_related('sequence', 'task_type', 'sequence__project', 'sequence__project__client', 'status', 'complexity', 'team_lead', 'artist', 'location', 'sequence__project__client__locality', 'status__status_segregation', 'supervisor').filter(pk__in=[x['shot']['id'] for x in shots_tlData]), many=True).data))
    _data = {}
    # print("obj_len",len(tlData["statistics"]),tlData["statistics"])
    tlData["logDates"] = []
    for dat in tlData["statistics"]:
        artist_id = [x['id'] for x in dat['artists'] if x.get('id',None) is not None]
        # print(artist_id)
        formtDateId = 'date_{date}'.format(date=datetime.datetime.strptime(dat['logDate'], '%Y-%m-%d').strftime('%Y_%m_%d'))
        ofx_stac = apiRequestManagers.getDBData(model=EmployeeDailyStatistics,queryFilter={"logDate": dat['logDate'], "employee__id__in": artist_id},select_related=['employee'], queryPerams=['id', "employee__id","employee__employee_id", "employee__fullName","employee__grade__id","employee__grade__name",'employee__grade__a_man_day',"employee__department__id","employee__department__name","employee__role__id","employee__role__name","employee__location__id","employee__location__name","employee__creation_date","employee__doe",'tmd','amd','rwh','aeh','ash','leaves','logDate'])
        for _stat in ofx_stac:
            if dat['logDate'] not in tlData["logDates"]:
                tlData["logDates"].append(dat['logDate'])
            eId = 'pk_{date}'.format(date=_stat['employee']['id'])
            if _data.get(eId,None) is None:
                _data[eId] = {}
            _data[eId][formtDateId] = _stat
    if type=="ARTIST":
        return export_tl_data_by_artist(buffer=buffer, from_date=from_date, to_date=to_date, tlDat=tlData, atristStatistics=_data, shots=shots_data)
    elif type=="DATE":
        return export_tl_data_by_date(buffer=buffer, from_date=from_date, to_date=to_date, tlDat=tlData, atristStatistics=_data, shots=shots_data)
    else:
        return buffer



 
def leads_sheet_download(buffer=None, from_date=None, to_date=None, tl_ids=[], lead=None):
    apiRequestManagers = apiRequestManager()
    workbook = xlsxwriter.Workbook(buffer)
    worksheet = workbook.add_worksheet()
    bold = workbook.add_format({'bold': True,  'border': 1, 'border_color': 'black'})
    # formate = workbook.add_format({'bold': True, 'bg_color': '#43d3f7', 'border': 1, 'border_color': 'red'})
    border = workbook.add_format({'border': 1, 'border_color': 'black'})
    _leads = apiRequestManagers.getDBData(model=Employee, queryFilter={"id__in": tl_ids}, select_related=['department'], queryPerams=["id", "fullName", "employee_id","doe", "location__id", "location__name", "department__id","department__name","role__id","role__name","creation_date"])
    _leadDeps = {}
    _leadLocation = {}
    if lead == 'HEAD OF DEPARTMENT':
        art_bind = []
        _art_bind = apiRequestManagers.getDBData(model=EmployeeRoleBinding, queryFilter={ "employee__role__name":"VFX ARTIST","employee__location__name__in":[x['location']['name'] for x in _leads] }, select_related=['employee', 'role','employee__location', 'employee__grade', 'bindWith' ], queryPerams=["id", "employee__id", "employee__employee_id", 'employee__location__id', 'employee__location__name', "employee__grade__id", "employee__grade__a_man_day", "employee__department__id", "employee__department__name" ])
        bindX = []
        for x in _leads:
            if _leadDeps.get(x["department"]["name"],None) is None:
                _leadDeps[x["department"]["name"]] = []
            _leadDeps[x["department"]["name"]].append(x["id"])
            _leadLocation['id_{id}'.format(id=x["id"])] = x["location"]['name'] if x["location"] is not None else None
        for x in _art_bind:
            if x['employee']['id'] not in bindX:
                bindX.append(x['employee']['id'])
                for ldLp in _leadDeps.get(x['employee']["department"]["name"],[]):
                    if x['employee']['location']['name']==_leadLocation['id_{id}'.format(id=ldLp)]:
                        art_bind.append({
                            "id": x['id'],
                            "employee":{
                                "id": x['employee']['id'],
                                "employee_id": x['employee']['employee_id'],
                                "grade": x['employee']['grade'],
                                },
                            "bindWith": {
                                "id": ldLp
                                }
                            }.copy())
    else:
        art_bind = apiRequestManagers.getDBData(model=EmployeeRoleBinding, queryFilter={"bindWith__id__in": tl_ids, "role__name": lead, "employee__role__name":"VFX ARTIST" }, select_related=['employee', 'role', 'employee__grade', 'bindWith' ], queryPerams=["id", "employee__id", "employee__employee_id", "employee__grade__id", "employee__grade__a_man_day", "bindWith__id" ])
    _tlDaily = apiRequestManagers.getDBData(model=LeadDailyStatistics, queryFilter={"logDate__range":[from_date,to_date], "lead__id__in": tl_ids}, select_related=['lead'], queryPerams=['id','lead__id','total_workdays','tmd','amd','shot_amd','leaves','logDate'])
    _tldata = []
    for _l in _leads:
        _tlData = {
            "leadInfo": {
                "id": _l["id"],
                "fullName": _l["fullName"],
                "employee_id": _l["employee_id"],
                "department": _l["department"]["name"],
                "location": _l["location"]["name"] if _l["location"] is not None else None,
                "role": _l["role"]["name"],
                "doe": _l["doe"],
                "creation_date": _l["creation_date"],
                },
            "artistsCount":0,
            "artistManday":0,
            "artistWorkingDays":0,
            "artistLeaves":0,
            "artistTMD":0,
            "artistAMD":0,
            "shotsAMD":0,
            }

        for _ab in art_bind:
            if _ab["bindWith"]["id"]==_l["id"]:
                _tlData["artistsCount"] = _tlData["artistsCount"] + 1
                if _ab["employee"]["grade"] is not None and _ab["employee"]["grade"]["a_man_day"] is not None:
                    _tlData["artistManday"] = _tlData["artistManday"] + _ab["employee"]["grade"]["a_man_day"]

        for _td in _tlDaily:
            if _td["lead"]["id"]==_l["id"]:
                _tlData["artistTMD"] = _tlData["artistTMD"] + _td["tmd"]
                _tlData["artistAMD"] = _tlData["artistAMD"] + _td["amd"]
                # _tlData["shotsAMD"] = _tlData["shotsAMD"] + _td["shot_amd"]
                _tlData["shotsAMD"] = _tlData["shotsAMD"] + _td["amd"]
                _tlData["artistWorkingDays"] = _tlData["artistWorkingDays"] + _td["total_workdays"];
                _tlData["artistLeaves"] = _tlData["artistLeaves"] + _td["leaves"]
        _tldata.append(json.loads(json.dumps(_tlData)))

    worksheet.write('A1', 'FROM DATE', bold)
    worksheet.write('B1', 'TO DATE', bold)
    worksheet.write('C1', 'EMPLOYEE NUMBER', bold)
    worksheet.write('D1', 'EMPLOYEE NAME', bold)
    worksheet.write('E1', 'DEPARTMENT', bold)
    worksheet.write('F1', 'DESIGNATION', bold)
    worksheet.write('G1', 'DOJ', bold)
    worksheet.write('H1', 'DOE', bold)
    worksheet.write('I1', 'ARTISTS', bold)
    worksheet.write('J1', 'TEAM ABILITY', bold)
    worksheet.write('K1', 'TOTAL WORKING DAYS', bold)
    worksheet.write('L1', 'TOTAL PRESENT DAYS', bold)
    worksheet.write('M1', 'TOTAL LEAVES', bold)
    worksheet.write('N1', 'TARGET MANDAYS ', bold)
    worksheet.write('O1', 'ACHIVED MANDAYS', bold)
    worksheet.write('P1', 'DIFFERENCE', bold)
    worksheet.write('Q1', 'LOCATION', bold)
    
    p = 1
    for j,d in enumerate(_tldata):
        worksheet.write(p + j, 0, storeDate(_datetime=from_date).strftime("%d-%m-%Y"), border)
        worksheet.write(p + j, 1, storeDate(_datetime=to_date).strftime("%d-%m-%Y"), border)
        worksheet.write(p + j, 2, d["leadInfo"]['employee_id'], border)
        worksheet.write(p + j, 3, d["leadInfo"]["fullName"], border)
        worksheet.write(p + j, 4, d["leadInfo"]["department"], border)
        worksheet.write(p + j, 5, d["leadInfo"]["role"], border)
        worksheet.write(p + j, 6, storeDate(_datetime=d["leadInfo"]["creation_date"]).strftime("%d-%m-%Y"), border)
        worksheet.write(p + j, 7, storeDate(_datetime=d["leadInfo"]["doe"]).strftime("%d-%m-%Y") if d["leadInfo"]["doe"] is not None else "N/A", border)
        worksheet.write(p + j, 8, d['artistsCount'], border)
        worksheet.write(p + j, 9, d['artistManday'], border)
        worksheet.write(p + j, 10, d['artistWorkingDays'] + d['artistLeaves'], border)
        worksheet.write(p + j, 11, d['artistWorkingDays'], border)
        worksheet.write(p + j, 12, d['artistLeaves'], border)
        worksheet.write(p + j, 13, d['artistTMD'],border)
        worksheet.write(p + j, 14, d['artistAMD'], workbook.add_format({"font_color": getfontcolor(value_range=d['artistTMD'], value=d['artistAMD']),'border': 1, 'border_color': 'black' }))
        worksheet.write(p + j, 15, (d['artistAMD'] - d['artistTMD']),workbook.add_format({"font_color": diffcolor(value1=d['artistAMD'],value2=d['artistTMD']),'border': 1, 'border_color': 'black'}))
        worksheet.write(p + j, 16, d["leadInfo"]["location"], border)
  
    workbook.close()
    return buffer
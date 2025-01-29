import datetime
import xlsxwriter
from OFX_API import apiRequestManager
from hrm.models import Attendance
def attendance_sheet_download(buffer=None, from_date=None, to_date=None, atd_ids=[]):
    apiRequestManagers = apiRequestManager()
    attendance_data = apiRequestManagers.getDBData(model=Attendance, queryFilter={"attendanceDate__range": [from_date, to_date], "id__in": atd_ids}, select_related=['employee'],
                                            queryPerams=['id',"attendanceDate", "dayType", "employee__id", "employee__fullName","employee__employee_id","firstInOfTheDay" ,"lastOutOfTheDay", "leaveDayStatus","shiftBreakDuration" ,"shiftDuration" , "shiftEffectiveDuration" ,"shiftEndTime","shiftStartTime","totalBreakDuration","totalEffectiveHours" ,"totalGrossHours" ,"creationDate","modifiedDate"])
    workbook = xlsxwriter.Workbook(buffer)
    worksheet = workbook.add_worksheet()
    bold = workbook.add_format({'bold': True, 'border': 1, 'border_color': 'black'})
    border = workbook.add_format({'border': 1, 'border_color': 'black'})
    worksheet.write('A1', 'DATE', bold)
    worksheet.write('B1', 'EMPLOYEE NAME', bold)
    worksheet.write('C1', 'EMPLOYEE_ID', bold)
    worksheet.write('D1', 'DAY TYPE', bold)
    worksheet.write('E1', 'FIRST IN', bold)
    worksheet.write('F1', 'LAST OUT', bold)
    worksheet.write('G1', 'TOTAL BREAK DURATION', bold)
    worksheet.write('H1', 'TOTAL EFFECTIVE HOURS', bold)
    worksheet.write('I1', 'TOTAL GROSS HOURS', bold)
    worksheet.write('J1', 'MODIFIED DATE', bold)
    p = 1
    i = 0
    for data in attendance_data:
        worksheet.write(i + p, 0, datetime.datetime.strptime(str(data['attendanceDate']), '%Y-%m-%d %H:%M:%S').strftime("%d-%m-%Y"), border)
        worksheet.write(i + p, 1, data['employee']['fullName'], border)
        worksheet.write(i + p, 2, data['employee']['employee_id'], border)
        worksheet.write(i + p, 3, data['dayType'], border)
        worksheet.write(i + p, 4, datetime.datetime.strptime(str(data['firstInOfTheDay']), '%Y-%m-%d %H:%M:%S').strftime("%d-%m-%Y,%H:%M:%S"), border)
        worksheet.write(i + p, 5, datetime.datetime.strptime(str(data['lastOutOfTheDay']), '%Y-%m-%d %H:%M:%S').strftime("%d-%m-%Y,%H:%M:%S"), border)
        worksheet.write(i + p, 6, data['totalBreakDuration'], border)
        worksheet.write(i + p, 7, data['totalEffectiveHours'], border)
        worksheet.write(i + p, 8, data['totalGrossHours'], border)
        worksheet.write(i + p, 9, datetime.datetime.strptime(str(data['modifiedDate']), '%Y-%m-%d %H:%M:%S.%f').strftime("%d-%m-%Y"), border)
        i +=1
    workbook.close()
    return buffer
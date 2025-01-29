#  Copyright (c) 2023.
#  Designed & Developed by Narendar Reddy G, OscarFX Private Limited
#  All rights reserved.

from OFX_API import apiRequestManager
from hrm.models import EmployeeRoleBinding
import xlsxwriter, json


def allartistlist_sheet_download(buffer):
    leads = ['SUPERVISOR','TEAM LEAD','HEAD OF DEPARTMENT']
    apiRequestManagers = apiRequestManager()
    employeeRoleBinding_data = apiRequestManagers.getDBData(model=EmployeeRoleBinding, queryFilter={"role__name__in": leads,'employee__role__name':'VFX ARTIST', 'employee__employement_status__name':'Active', 'bindWith__employement_status__name':'Active' }, queryPerams=['id','employee__id','employee__employee_id','employee__fullName','department__id','department__name','employee__grade__id','employee__grade__name','employee__grade__a_man_day','role__id','role__name','bindWith__id','bindWith__employee_id','bindWith__fullName','bindWith__role__id','bindWith__role__name'])
    _rdata = {}
    for emp in employeeRoleBinding_data:
        key = 'id_{id}'.format(id=emp["employee"]["id"])
        if _rdata.get(key,None) is None:
            _rdata[key] = {
                "id": emp["employee"]["id"],
                "employee_id": emp["employee"]["employee_id"],
                "fullName": emp["employee"]["fullName"],
                "grade": emp["employee"]["grade"],
                "department": emp["department"],
                }
            for led in leads:
                _rdata[key][apiRequestManagers.makeKey(led)] = None
        if emp["bindWith"] is not None and apiRequestManagers.makeKey(emp["role"]["name"])==apiRequestManagers.makeKey(emp["bindWith"]["role"]["name"]):
            _rdata[key][apiRequestManagers.makeKey(emp["role"]["name"])] = json.loads(json.dumps(emp["bindWith"]))
    workbook = xlsxwriter.Workbook(buffer)
    worksheet = workbook.add_worksheet()
    bold = workbook.add_format({'bold': True, 'bg_color': '#43d3f7', 'border': 1, 'border_color': 'black'})
    border = workbook.add_format({'border': 1, 'border_color': 'black'})

    # Write some data headers.
    worksheet.write('A1', 'EMPLOYEE ID', bold)
    worksheet.write('B1', 'EMPLOYEE NAME', bold)
    worksheet.write('C1', 'GRAD', bold)
    worksheet.write('D1', 'DEPARTMENT', bold)
    worksheet.write('E1', 'SUPERVISOR', bold)
    worksheet.write('F1', 'TEAM LEAD', bold)
    worksheet.write('G1', 'HEAD OF DEPARTMENT', bold)
     
    col = 0
    row = 0
    for artist in list(_rdata.values()):
        try:
            worksheet.write(row + 1, col, artist['employee_id'], border)
            worksheet.write(row + 1, col + 1, artist['fullName'], border)
            worksheet.write(row + 1, col + 2, '{a}({b})'.format(a=artist['grade']['name'],b=artist['grade']['a_man_day']) if artist['grade'] is not None else 'N/A', border)
            worksheet.write(row + 1, col + 3, artist['department']['name'], border)
            worksheet.write(row + 1, col + 4, artist[apiRequestManagers.makeKey('SUPERVISOR')]['fullName'] if artist[apiRequestManagers.makeKey('SUPERVISOR')] is not None else 'N/A', border)
            worksheet.write(row + 1, col + 5, artist[apiRequestManagers.makeKey('TEAM LEAD')]['fullName'] if artist[apiRequestManagers.makeKey('TEAM LEAD')] is not None else 'N/A', border)
            worksheet.write(row + 1, col + 6, artist[apiRequestManagers.makeKey('HEAD OF DEPARTMENT')]['fullName'] if artist[apiRequestManagers.makeKey('HEAD OF DEPARTMENT')] is not None else 'N/A', border)
        except Exception as e:
            print(artist)
        row += 1
    workbook.close()
    return buffer
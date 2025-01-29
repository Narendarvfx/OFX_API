#  Copyright (c) 2023.
#  Designed & Developed by Narendar Reddy G, OscarFX Private Limited
#  All rights reserved.

from datetime import datetime
import json

import xlsxwriter

from production.models import Shots
from production.serializers import ShotsSerializer


# def get_data(dept):
#     status_list = "YTA|ATL|YTS|WIP|STC|STQ|IRT|IAP|CRT|LAP|LRT"
#     status = []
#     for stat in status_list.split('|'):
#         status.append(stat)
#     shot = Shots.objects.select_related('sequence', 'task_type', 'sequence__project', 'sequence__project__client',
#                                         'status', 'complexity', 'team_lead', 'artist').filter(status__code__in=status,
#                                                                                               task_type__name=dept)
#     serializer = ShotsSerializer(shot, many=True)
#     # print(json.dumps(serializer.data))
#     dataa = json.dumps(serializer.data)
#     return json.loads(dataa)

def dateformate(date):
    return date if len(date.split('.')) > 1 else date + '.000000'

def create_workbook(buffer, request):
    argumentos = {}
    if request.GET.get('shot_id'):
        argumentos['pk'] = request.GET.get('shot_id')
    # Handle search query
    search_query = request.GET.get('search', None)
    if request.GET.get('search'):
        argumentos['name__icontains'] = request.GET.get('search')
    if request.GET.get('client_id'):
        clients = []
        for client in request.GET.get('client_id').split('|'):
            clients.append(client)
        argumentos['sequence__project__client__pk__in'] = clients
    if request.GET.get('client'):
        clients = request.GET.get('client')
        if clients:
            clients_list = clients.split(',')
            argumentos['sequence__project__client__name__in'] = clients_list
    if request.GET.get('project'):
        projects = request.GET.get('project')
        if projects:
            projects_list = projects.split(',')
            argumentos['sequence__project__name__in'] = projects_list
    if request.GET.get('project_id'):
        projects = []
        for project in request.GET.get('project_id').split('|'):
            projects.append(project)
        argumentos['sequence__project__pk__in'] = projects
    if request.GET.get('status'):
        status_codes = request.GET.get('status')
        if status_codes:
            # Split the string into a list of values
            status_code_list = status_codes.split(',')
            argumentos['status__code__in'] = status_code_list
    else:
        status_codes = ['YTS','YTA','ATL','WIP','STQ','STC','IAP','CRT','IRT','LAP','LRT','ATC','ATS']
        argumentos['status__code__in'] = status_codes
    if request.GET.get('task type'):
        task_types = request.GET.get('task type')
        if task_types:
            # Split the string into a list of values
            task_type_list = task_types.split(',')
            argumentos['task_type__name__in'] = task_type_list
    if request.GET.get('type'):
        types = request.GET.get('type')
        if types:
            # Split the string into a list of values
            type_list = types.split(',')
            argumentos['type__in'] = type_list
    if request.GET.get('complexity'):
        complexity = request.GET.get('complexity')
        if complexity:
            # Split the string into a list of values
            complexity_list = complexity.split(',')
            argumentos['complexity__name__in'] = complexity_list
    if request.GET.get('dept'):
        depts = []
        for dept in request.GET.get('dept').split('|'):
            depts.append(dept)
        argumentos['task_type__name__in'] = depts
    if request.GET.get('shot_ids'):
        shot_ids = []
        for shot_id in request.GET.get('shot_ids').split('|'):
            shot_ids.append(shot_id)
        argumentos['pk__in'] = shot_ids

    shotsdata = Shots.objects.prefetch_related('timelogs','artists','artists__role','artists__department','artists__role__permissions','artist__role__permissions').select_related('sequence', 'task_type',
                                                                                 'sequence__project',
                                                                                 'sequence__project__client', 'status',
                                                                                 'complexity',
                                                                                 'team_lead', 'artist', 'location','artist__role','artist__department',
                                                                                 'sequence__project__client__locality','status__status_segregation','supervisor','hod').filter(
                **argumentos).order_by('name').exclude(sequence__project__status="ARCHIVED")
    serializer = ShotsSerializer(shotsdata, many=True)
    shotdata = json.dumps(serializer.data)
    shots_data= json.loads(shotdata)
    # print(shots_data)
    workbook = xlsxwriter.Workbook(buffer)
    # for dept in ['PAINT', 'ROTO', 'MM', 'COMP']:
    #     shots_data = get_data(dept)
    #     worksheet = workbook.add_worksheet(dept)
    #     write_to_excel(workbook, worksheet, shots_data)
    worksheet = workbook.add_worksheet()
    write_to_excel(workbook, worksheet, shots_data, request)
    workbook.close()
    return buffer


def write_to_excel(workbook, worksheet, shots_data,request):
    userPermissions = [ v.permission_key for v in request.user.employee.role.permissions.all()]

    # Add a bold format to use to highlight cells.
    bold = workbook.add_format({'bold': True, 'bg_color': '#43d3f7', 'border': 1, 'border_color': 'black'})
    pending_color = workbook.add_format({'bg_color': 'yellow', 'border': 1, 'border_color': 'black'})
    border = workbook.add_format({'border': 1, 'border_color': 'black', })
    # Add a number format for cells with percentage.
    percent = workbook.add_format({'num_format': '0.0%', 'border': 1, 'border_color': 'black'})
    # Write some data headers.
    worksheet.write('A1', 'CLIENT', bold)
    worksheet.write('B1', 'PROJECT', bold)
    worksheet.write('C1', 'SHOT CODE', bold)
    worksheet.write('D1', 'TOTAL FRAMES', bold)
    worksheet.write('E1', 'TASK', bold)
    worksheet.write('F1', 'COMPLEXITY', bold)
    worksheet.write('G1', 'STATUS', bold)
    worksheet.write('H1', 'BID DAYS', bold)
    worksheet.write('I1', 'WIP%', bold)
    worksheet.write('J1', 'DUE MANDAYS', bold)
    worksheet.write('K1', 'INTERNAL-ETA', bold)
    if 'can_view_client_eta' in userPermissions:
        worksheet.write('L1', 'CLIENT-ETA', bold)
        worksheet.write('M1', 'NOTES', bold)
        worksheet.write('N1', 'SUPERVISOR', bold)
        worksheet.write('O1', 'TEAM LEAD', bold)
        worksheet.write('P1', 'COMPILER', bold)
        worksheet.write('Q1', 'ARTISTS', bold)
        worksheet.write('R1', 'IN DATE', bold)
        worksheet.write('S1', 'PACKAGE ID', bold)
        worksheet.write('T1', 'ESTIMATE ID', bold)
        worksheet.write('U1', 'ESTIMATE DATE', bold)
        worksheet.write('V1', 'INTERNAL VERSION', bold)
        worksheet.write('W1', 'CLIENT VERSION', bold)
        worksheet.write('X1', 'LOCATION', bold)
    else:
        worksheet.write('L1', 'NOTES', bold)
        worksheet.write('M1', 'SUPERVISOR', bold)
        worksheet.write('N1', 'TEAM LEAD', bold)
        worksheet.write('O1', 'COMPILER', bold)
        worksheet.write('P1', 'ARTISTS', bold)
        worksheet.write('Q1', 'IN DATE', bold)
        worksheet.write('R1', 'PACKAGE ID', bold)
        worksheet.write('S1', 'ESTIMATE ID', bold)
        worksheet.write('T1', 'ESTIMATE DATE', bold)
        worksheet.write('U1', 'INTERNAL VERSION', bold)
        worksheet.write('V1', 'CLIENT VERSION', bold)
        worksheet.write('W1', 'LOCATION', bold)

    date_format = workbook.add_format({'border': 1, 'border_color': 'black', 'num_format': 'dd/mm/yyyy'})

    # # Start from the first cell below the headers.
    col = 0
    row = 0
    for shot_data in shots_data:
        shot_status = shot_data['status']['code']
        if shot_data['status']['code'] in ['YTA', 'ATL', 'YTS']:
            shot_status = "YTS"
        elif shot_data['status']['code'] in ['WIP', 'STC', 'LRT']:
            shot_status = "WIP"
        elif shot_data['status']['code'] in ['STQ', 'IRT','LAP']:
            shot_status = "QC"
        elif shot_data['status']['code'] == "CRT":
            shot_status = "RETAKE"

        if shot_data['type'] == "RETAKE":
            bid_days = 0
            percentile = 0
        else:
            bid_days = float(shot_data['bid_days'])
            percentile = shot_data['progress'] / 100

        bid_column = 'H{}'.format(row + 2)
        progress_column = 'I{}'.format(row + 2)
        total_frames = shot_data['actual_end_frame'] - shot_data['actual_start_frame'] + 1
        if shot_data['internal_eta']:
            due_date = datetime.strptime(dateformate(shot_data['internal_eta']), '%Y-%m-%dT%H:%M:%S.%f')
        else:
            due_date = ""
        if shot_data['eta']:
            client_eta_date = datetime.strptime(dateformate(shot_data['eta']), '%Y-%m-%dT%H:%M:%S.%f')
        else:
            client_eta_date = ""
        if shot_data['estimate_date']:
            estimate_date = datetime.strptime(dateformate(shot_data['estimate_date']), '%Y-%m-%dT%H:%M:%S.%f')
        else:
            estimate_date = ""

        in_date = datetime.strptime(dateformate(shot_data['creation_date']), '%Y-%m-%dT%H:%M:%S.%f')

        worksheet.write(row + 1, col, shot_data['sequence']['project']['client']['name'], border)
        worksheet.write(row + 1, col + 1, shot_data['sequence']['project']['name'], border)
        worksheet.write(row + 1, col + 2, shot_data['name'], border)
        worksheet.write(row + 1, col + 3, str(total_frames), border)
        worksheet.write(row + 1, col + 4, shot_data['task_type'], border)
        worksheet.write(row + 1, col + 5, shot_data['complexity'], border)
        worksheet.write(row + 1, col + 6, shot_status, border)
        worksheet.write(row + 1, col + 7, bid_days, border)
        worksheet.write(row + 1, col + 8, percentile, percent)
        worksheet.write(row + 1, col + 9,
                        '=ROUND(({}-{}*{}),1)'.format(bid_column, bid_column, progress_column), pending_color)
        worksheet.write(row + 1, col + 10, due_date, date_format)
        if 'can_view_client_eta' in userPermissions:
            worksheet.write(row+1, col+11, client_eta_date, date_format)
            worksheet.write(row + 1, col + 12, " ", border)
            worksheet.write(row + 1, col + 13, shot_data['supervisor'], border)
            worksheet.write(row + 1, col + 14, shot_data['team_lead'], border)
            worksheet.write(row + 1, col + 15, shot_data['artist'], border)
            worksheet.write(row + 1, col + 16, ' '.join([str(elem['fullName']+",") for elem in shot_data['artists']]), border)
            worksheet.write(row + 1, col + 17, in_date, date_format)
            worksheet.write(row + 1, col + 18, shot_data['package_id'], border)
            worksheet.write(row + 1, col + 19, shot_data['estimate_id'], border)
            worksheet.write(row + 1, col + 20, estimate_date, date_format)
            location = ""
            if shot_data['location']:
                location = shot_data['location']
            worksheet.write(row + 1, col + 21, "", border)
            worksheet.write(row + 1, col + 22, shot_data['version'], border)
            worksheet.write(row + 1, col + 23, location, border)
            row += 1
        else:
            worksheet.write(row + 1, col + 11, " ", border)
            worksheet.write(row + 1, col + 12, shot_data['supervisor'], border)
            worksheet.write(row + 1, col + 13, shot_data['team_lead'], border)
            worksheet.write(row + 1, col + 14, shot_data['artist'], border)
            worksheet.write(row + 1, col + 15, ' '.join([str(elem['fullName']+",") for elem in shot_data['artists']]), border)
            worksheet.write(row + 1, col + 16, in_date, date_format)
            worksheet.write(row + 1, col + 17, shot_data['package_id'], border)
            worksheet.write(row + 1, col + 18, shot_data['estimate_id'], border)
            worksheet.write(row + 1, col + 19, estimate_date, date_format)
            location = ""
            if shot_data['location']:
                location = shot_data['location']
            worksheet.write(row + 1, col + 20, "", border)
            worksheet.write(row + 1, col + 21, shot_data['version'], border)
            worksheet.write(row + 1, col + 22, location, border)
            row += 1


# write_to_excel()


# def check_filters(buffer=None, client_id=None, project_id=None, taskType_id=None, status_idd=None, location_id=None, locality_id=None):
#     shot = Shots.objects.select_related('sequence', 'task_type', 'sequence__project', 'sequence__project__client',
#                                         'status', 'complexity', 'team_lead', 'artist').all()
#     status_list = "YTA|ATL|YTS|WIP|STC|STQ|IRT|IAP|CRT|LAP|LRT"
#     status = []
#     for stat in status_list.split('|'):
#         status.append(stat)
#     if client_id:
#         shot = shot.filter(sequence__project__client_id=client_id)
#     if project_id:
#         shot = shot.filter(sequence__project_id=project_id)
#     if status_idd:
#         shot = shot.filter(status_id=status_idd)
#     else:
#         shot = shot.filter(status__code__in=status)
#     if locality_id:
#         shot = shot.filter(sequence__project__client__locality_id=locality_id)
#     if location_id:
#         shot = shot.filter(location_id=location_id)
#     if taskType_id:
#         shot = shot.filter(task_type_id=taskType_id)
#     serializer = ShotsSerializer(shot, many=True)
#     dataa = json.dumps(serializer.data)
#     workbook = xlsxwriter.Workbook(buffer)
#     worksheet = workbook.add_worksheet()
#     write_to_excel(workbook, worksheet, json.loads(dataa))
#
#     workbook.close()
#     return buffer
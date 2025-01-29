import json
import xlsxwriter
from production.models import Clients, Projects, Task_Type
def writeVersionreportWorksheet(buffer,query={},data={},isOnly=False):
    myKeys = list(data.keys())
    myKeys.sort(reverse=True)
    data = json.loads(json.dumps({i: data[i] for i in myKeys}))
    clientName = list(Clients.objects.filter(id=query['shot__sequence__project__client__id']).values('name'))[0]['name']
    projectsName = list(Projects.objects.filter(id=query['shot__sequence__project__id']).values('name'))[0]['name'] if query.get('shot__sequence__project__id',None) is not None else 'All Projects'
    departmentName = list(Task_Type.objects.filter(id=query['shot__task_type__id']).values('name'))[0]['name'] if query.get('shot__task_type__id',None) is not None else 'All Departments'
    workbook = xlsxwriter.Workbook(buffer)
    merge_format = workbook.add_format({
        'bold': 1,
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'fg_color': 'yellow'})
    borderWithColor = workbook.add_format({'border': 1, 'border_color': 'black', 'bg_color': 'red', 'font_color':'#ffffff'})
    bold = workbook.add_format({'bold': True, 'bg_color': '#43d3f7', 'border': 1, 'border_color': 'black'})
    border = workbook.add_format({'border': 1, 'border_color': 'black'})
    worksheet1 = workbook.add_worksheet(name='Version Report')
    worksheet1.merge_range('A1:D2', 'CLIENT: {clientName}'.format(clientName=clientName), merge_format)
    worksheet1.merge_range('E1:H2', 'PROJECT: {projectsName}'.format(projectsName=projectsName), merge_format)
    worksheet1.merge_range('I1:M2', 'DEPARTMENT: {departmentName}'.format(departmentName=departmentName), merge_format)
    if isOnly:
        worksheet1.merge_range('N1:P1', 'VERSION: {versions}'.format(versions=', '.join(query.get('version__in',['All Versions']))), merge_format)
        worksheet1.merge_range('Q1:S1', 'SHOTS: {shotsCount}'.format(shotsCount=len(data[list(data.keys())[0]]['shots'])), merge_format)
    else:
        worksheet1.merge_range('N1:S1', 'VERSIONS: {versions}'.format(versions=', '.join(query.get('version__in',['All Versions']))), merge_format)
    if query.get('modified_date__range',None) is not None:
        worksheet1.merge_range('N2:P2', 'FROM DATE: {fromDate}'.format(fromDate=query['modified_date__range'][0].split(' ')[0]), merge_format)
        worksheet1.merge_range('Q2:S2', 'TO DATE: {fromDate}'.format(fromDate=query['modified_date__range'][1].split(' ')[0]), merge_format)
    else:
        worksheet1.merge_range('N2:S2', 'DATE: All Dates', merge_format)
    if isOnly is False:
        worksheet1.write('A3', 'VERSIONS', bold)
        worksheet1.write('B3', 'SHOTS', bold)
    row = 3
    worksheets = {}

    for vName, vData in data.items():
        if isOnly is False:
            worksheet1.write(row,0,vData['name'], border)
            worksheet1.write(row,1,len(vData['shots']), border)
            worksheets[vData['name']] = workbook.add_worksheet(name=vData['name'])
        else:
            worksheets[vData['name']] = worksheet1
        worksheets[vData['name']].write('A{index}'.format(index=row if isOnly else 1), 'SHOT CODE', bold)
        worksheets[vData['name']].write('B{index}'.format(index=row if isOnly else 1), 'PROJECT', bold)
        worksheets[vData['name']].write('C{index}'.format(index=row if isOnly else 1), 'SEQUENCE', bold)
        worksheets[vData['name']].write('D{index}'.format(index=row if isOnly else 1), 'VERSION', bold)
        worksheets[vData['name']].write('E{index}'.format(index=row if isOnly else 1), 'DEPARTMENT', bold)
        worksheets[vData['name']].write('F{index}'.format(index=row if isOnly else 1), 'SUBMISSION DATE', bold)
        worksheets[vData['name']].write('G{index}'.format(index=row if isOnly else 1), 'CAPTAIN', bold)
        worksheets[vData['name']].write('H{index}'.format(index=row if isOnly else 1), 'ACTUAL BIDS', bold)
        worksheets[vData['name']].write('I{index}'.format(index=row if isOnly else 1), 'SUPERVISOR', bold)
        worksheets[vData['name']].write('J{index}'.format(index=row if isOnly else 1), 'TEAM LEAD', bold)
        worksheets[vData['name']].write('K{index}'.format(index=row if isOnly else 1), 'HOD', bold)
        worksheets[vData['name']].write('L{index}'.format(index=row if isOnly else 1), 'ARTIST', bold)
        worksheets[vData['name']].write('M{index}'.format(index=row if isOnly else 1), 'PACKAGE ID', bold)
        worksheets[vData['name']].write('N{index}'.format(index=row if isOnly else 1), 'LOCATION', bold)
        shotRow = row if isOnly else 1
        for shot in vData['shots']:
            worksheets[vData['name']].write(shotRow,0,shot['shot']['name'], border)
            worksheets[vData['name']].write(shotRow,1,shot['shot']['sequence']['project']['name'], border)
            worksheets[vData['name']].write(shotRow,2,shot['shot']['sequence']['name'], border)
            worksheets[vData['name']].write(shotRow,3,shot['shot']['version'] ,borderWithColor if shot['shot']['version']!=vData['name'] else border)
            worksheets[vData['name']].write(shotRow,4,shot['shot']['task_type']['name'], border)
            worksheets[vData['name']].write(shotRow,5,shot['modified_date'].split(' ')[0], border)
            worksheets[vData['name']].write(shotRow,6,shot['shot']['artist']['fullName'] if shot['shot']['artist'] is not None else 'N/A', border)
            worksheets[vData['name']].write(shotRow,7,shot['shot']['bid_days'] if shot['shot']['bid_days'] is not None else 'N/A', border)
            worksheets[vData['name']].write(shotRow,8,shot['shot']['supervisor']['fullName'] if shot['shot']['supervisor'] is not None else 'N/A', border)
            worksheets[vData['name']].write(shotRow,9,shot['shot']['team_lead']['fullName'] if shot['shot']['team_lead'] is not None else 'N/A', border)
            worksheets[vData['name']].write(shotRow,10,shot['shot']['hod']['fullName'] if shot['shot']['hod'] is not None else 'N/A', border)
            worksheets[vData['name']].write(shotRow,11,', '.join([x['fullName'] for x in shot['shot']['artists']]) if len(shot['shot']['artists'])>0 else 'N/A', border)
            worksheets[vData['name']].write(shotRow,12,shot['shot']['package_id'] if shot['shot']['package_id'] is not None else 'N/A', border)
            worksheets[vData['name']].write(shotRow,13,shot['shot']['location']['name'] if shot['shot']['location'] is not None else 'GLOBAL', border)  
            shotRow += 1
        row += 1

    workbook.close()
    return buffer
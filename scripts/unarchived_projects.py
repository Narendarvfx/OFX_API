import requests
import xlsxwriter

server = "http://127.0.0.1:8000"
token = '040734ca148cc9e7a62f2321e2238125204d6b80'

project_api_url = "{}/api/production/projects/".format(server)

def get_projects():
    r = requests.get(project_api_url, headers={'Authorization': 'Token {}'.format(token)},
                             verify=False)
    print(r.json())
    workbook = xlsxwriter.Workbook("Projects.xlsx")
    worksheet = workbook.add_worksheet()
    bold = workbook.add_format({'bold': True, 'border': 1, 'border_color': 'black'})
    border = workbook.add_format({'border': 1, 'border_color': 'black'})
    worksheet.write('A1', 'CLIENT', bold)
    worksheet.write('B1', 'PROJECT', bold)
    worksheet.write('C1', 'STATUS', bold)
    p = 1
    i = 0
    for project in r.json():
        worksheet.write(i + p, 0, project['client'], border)
        worksheet.write(i + p, 1, project['name'], border)
        worksheet.write(i + p, 2, project['status'], border)
        i += 1
    workbook.close()
get_projects()
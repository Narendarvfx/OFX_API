import datetime

import requests
import xlsxwriter

# server = "http://shotbuzz.oscarfx.com"
server = "http://127.0.0.1:8000"
token = '040734ca148cc9e7a62f2321e2238125204d6b80'

shots = []

def get_dtc_shots():
    from_date = "2023-10-01T00:00:00.000000"
    to_date = "2023-10-31T23:59:59.999999"
    api_url = "{}/api/production/client_versions/?from_date={}&to_date={}".format(server, from_date, to_date)
    data = requests.get(api_url, headers={'Authorization': 'Token {}'.format(token)}, verify=False)
    return data.json()
    # if get_user_id.json():

def format_date(_date):
    try:
        format_date = datetime.datetime.strptime(_date, '%Y-%m-%dT%H:%M:%S.%f').strftime("%d-%m-%Y")
    except:
        format_date = datetime.datetime.strptime(_date, '%Y-%m-%dT%H:%M:%S').strftime("%d-%m-%Y")

    return format_date
def version_sheet_export(shots_data=None):
    print(shots_data)
    workbook = xlsxwriter.Workbook("October_Uploads.xlsx")
    worksheet = workbook.add_worksheet()
    bold = workbook.add_format({'bold': True, 'border': 1, 'border_color': 'black'})
    border = workbook.add_format({'border': 1, 'border_color': 'black'})
    worksheet.write('A1', 'CLIENT', bold)
    worksheet.write('B1', 'PROJECT', bold)
    worksheet.write('C1', 'SHOT CODE', bold)
    worksheet.write('D1', 'TASK', bold)
    worksheet.write('E1', 'HOD', bold)
    worksheet.write('F1', 'SUPERVISOR', bold)
    worksheet.write('G1', 'TEAM LEAD', bold)
    worksheet.write('H1', 'VERSION', bold)
    worksheet.write('I1', 'SUBMISSION DATE', bold)
    p = 1
    i = 0
    for data in shots_data:
        worksheet.write(i + p, 0, data['sequence']['project']['client']['name'], border)
        worksheet.write(i + p, 1, data['sequence']['project']['name'], border)
        worksheet.write(i + p, 2, data['name'], border)
        worksheet.write(i + p, 3, data['task_type'], border)
        worksheet.write(i + p, 4, "", border)
        worksheet.write(i + p, 5, data['supervisor'], border)
        worksheet.write(i + p, 6, data['team_lead'], border)
        worksheet.write(i + p, 7, data['version'], border)
        worksheet.write(i + p, 8, format_date(str(data['submitted_date'])), border)
        i +=1
    workbook.close()

def get_shots_data(shot_id):
    api_url = "{}/api/production/production_sheet/?shot_id={}".format(server, shot_id)
    data = requests.get(api_url, headers={'Authorization': 'Token {}'.format(token)}, verify=False)
    return data.json()
def main():
    dtc_data = get_dtc_shots()
    # print(len(dtc_data))
    shots = []
    for i ,shot_data in enumerate(dtc_data):
        shots_data = get_shots_data(shot_data['shot'])
        print(shots_data)
        if shots_data:
            shots.append(shots_data[0])
        # print(shots_data[0])
    version_sheet_export(shots_data=shots)
if __name__ == '__main__':
    main()
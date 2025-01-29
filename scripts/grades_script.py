import csv
import logging

import requests

# server = "http://127.0.0.1:8000"
server = "http://shotbuzz.oscarfx.com"
token = '040734ca148cc9e7a62f2321e2238125204d6b80'
grades_csv = r"C:\Users\Administrator\Documents\new_pdt_final.csv"

grade_api_url = "{}/api/hrm/grades/".format(server)

# Create and configure logger
logging.basicConfig(filename=r"C:\Users\Administrator\Documents\grades_log.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')

# Creating an object
logger = logging.getLogger()

# Setting the threshold of logger to DEBUG
logger.setLevel(logging.DEBUG)
def post_grade_data():
    """
    Import employee data from csv file
    :return:
    """

    with open(grades_csv, 'r', newline='', encoding="utf-8-sig") as csvfile:
        reader = csv.DictReader(csvfile)
        print(reader)
        for row in reader:
            print(row)
            data = {
                "name": row['Grade'],
                "a_man_day": row['Manday']
            }
            response = requests.post(grade_api_url, data=data, headers={'Authorization': 'Token {}'.format(token)}, verify=False)
            print(response.text)

def get_grade_data():

    response = requests.get(grade_api_url, headers={'Authorization': 'Token {}'.format(token)},
                             verify=False)
    print(len(response.json()))

def update_employee_grade():
    employee_url = "{}/api/hrm/employee/".format(server)
    employee_request = requests.get(employee_url, headers={'Authorization': 'Token {}'.format(token)},
                             verify=False)
    for emp in employee_request.json():
        print(emp)
        data = {
            'grade': emp['employee_id'],
        }
        put_url = "{}/api/hrm/employee/{}/".format(server, emp['id'])
        put_req = requests.put(put_url, data=data, headers={'Authorization': 'Token {}'.format(token)},
                             verify=False)
        print(put_req.text)

def update_all_grades():
    with open(grades_csv, 'r', newline='', encoding="utf-8-sig") as csvfile:
        reader = csv.DictReader(csvfile)
        print(reader)
        for row in reader:
            # print(grade_api_url+'?name={}'.format(row['EMP ID']))
            if len(row['EMP ID'])>0:
                response = requests.get(grade_api_url+'?name={}'.format(row['EMP ID']), headers={'Authorization': 'Token {}'.format(token)},
                                        verify=False)
                grade_data = response.json()
                if grade_data:
                    print(grade_data)
                    data = {
                        "a_man_day": row['PDT']
                    }
                    response = requests.put(grade_api_url+'?id={}'.format(grade_data[0]['id']), data=data, headers={'Authorization': 'Token {}'.format(token)}, verify=False)

                    print(response.text)
                else:
                    logger.info("Not Found: {}".format(row['EMP ID']))

update_all_grades()
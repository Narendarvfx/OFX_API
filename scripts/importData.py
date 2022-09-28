"""
This Script is used to import data in Oscarfx Pipeline System
"""

import datetime
import csv
import requests

server = "http://192.168.5.14"
token = '70e563f1062d898b1fa8bce26daf6aa83e55126d'
employee_csv = r"/Users/ofxlap-28/Documents/OFX/OFX_API/scripts/data/training_employees_final.csv"

########################################################################################################################

def update_employee_details(data, row):
    """
    This function will read data from employee csv file and update in hrm
    employee model
    :param data:
    :param row:
    :return:
    """
    user_api_url = "{}/api/hrm/employee/{}/".format(server, data['id'])
    data_edit = {
        "employee_id": row['Employee ID'],
        "fullName": row['Full Name'],
        "email": row['Email ID'],
        "employement_status": "Active",
        "department": row['Department'],
        "role": row['Role'],
        "grade": row['Grade'],
        "team_lead": row['Team Lead']
    }
    response = requests.put(user_api_url, data=data_edit, headers={'Authorization': 'Token {}'.format(token)})
    print(response.text)

def import_employee_data():
    """
    Import employee data from csv file
    :return:
    """
    default_password = "Ofx@12345"
    user_api_url = "{}/api/users/".format(server)

    with open(employee_csv, 'r', newline='', encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        print(reader)
        for row in reader:
            data = {
                "password": default_password,
                "is_superuser": False,
                "username": row['UserName'],
                "email": row['Email ID'],
                "first_name":row['Full Name'],
                "is_staff": False,
                "is_active": True
            }
            response = requests.post(user_api_url, data=data, headers={'Authorization': 'Token {}'.format(token)}, verify=False)
            update_employee_details(response.json(), row)


def generate_default_profile_photo():
    import shutil
    with open(employee_csv, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['GENDER'] == 'male':
                shutil.copyfile('img/male.png', 'img/default/{}.jpg'.format(row['EMPLOYEE ID']))
            elif row['GENDER'] == 'female':
                shutil.copyfile('img/female.png', 'img/default/{}.jpg'.format(row['EMPLOYEE ID']))

def setTeamId():
    get_user_url = "{}/api/hrm/employee/".format(server)
    get_user_id = requests.get(get_user_url, headers={'Authorization': 'Token {}'.format(token)}, verify=False)
    # print(get_user_id.text)
    for user in get_user_id.json():
        # print(user)
        with open(employee_csv, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['EmployeeID'] == user['employee_id']:
                    data = {
                        "team_lead" : row['TeamId'],
                        "role": row['Role']
                    }
                    user_api_url = "{}/api/hrm/employee/{}/".format(server, user['id'])
                    try:
                        response = requests.put(user_api_url, data=data, headers={'Authorization': 'Token {}'.format(token)}, verify=False)
                    except Exception as e:
                        print("Not Updated: ", row['EmployeeID'])
                    
                    

if __name__ == '__main__':
    #generate_default_profile_photo()
    #update_username()
    import_employee_data()
    #setTeamId()
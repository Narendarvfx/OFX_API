"""
This Script is used to import data in Oscarfx Pipeline System
"""

import datetime
import csv
import requests

server = "http://172.168.1.197:80"
token = '8f1192dfa465d1f566c38e53ed199d8da7090a55'
employee_csv = 'data/Employees_data_final.csv'

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
    print(user_api_url)
    data_edit = {
        "employee_id": row['Employee ID'],
        "fullName": row['Full Name'],
        "email": row['Email ID'],
        "employement_status": "Active",
        "department": row['Department'],
        "role": row['Role'],
        "grade": row['Grade'],
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

    with open(employee_csv, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            print(row['UserName'])
            data = {
                "password": default_password,
                "is_superuser": False,
                "username": row['UserName'],
                "email": row['Email ID'],
                "first_name":row['Full Name'],
                "is_staff": False,
                "is_active": True
            }
            response = requests.post(user_api_url, data=data, headers={'Authorization': 'Token {}'.format(token)})
            print(response.text)
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
    get_user_url = "{}/api/users/".format(server)
    get_user_id = requests.get(get_user_url, headers={'Authorization': 'Token {}'.format(token)})
    # print(get_user_id.text)
    for user in get_user_id.json():
        with open(employee_csv, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['UserName'] == user['username']:
                    data = {
                        "team" : row['Team']
                    }
                    user_api_url = "{}/api/hrm/employee/{}/".format(server, user['id'])
                    response = requests.put(user_api_url, data=data, headers={'Authorization': 'Token {}'.format(token)})
                    print(response.text)
                    
                    

if __name__ == '__main__':
    #generate_default_profile_photo()
    #update_username()
    # import_employee_data()
    # update_employee_pan_details()
    # update_el_data()
    setTeamId()
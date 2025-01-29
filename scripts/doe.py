import datetime
import csv
import requests

server = "http://shotbuzz.oscarfx.com"
# server = "http://127.0.0.1:8000"
# token = '084d0a3f093028ad4cd7981885527586e94d60aa' # Local
token = '040734ca148cc9e7a62f2321e2238125204d6b80'
employee_csv = r"C:\Users\Administrator\Documents\exit_emp.csv"

def get_employee(employee_id, doe):
    user_api_url = "{}/api/hrm/employee/?ofx_id={}&status={}".format(server, employee_id,"Deactive")
    get_user_id = requests.get(user_api_url, headers={'Authorization': 'Token {}'.format(token)}, verify=False)
    print(get_user_id.json())
    if get_user_id.json():
        try:
            update_emp_deo(get_user_id.json()[0]['id'], doe)
        except:
            pass
            print("Not Updated:", employee_id, doe)

def update_emp_deo(employee_id, doe):
    """
    This function will read data from employee csv file and update in hrm
    employee model
    :param data:
    :param row:
    :return:
    """
    user_api_url=""
    data_edit = {
        "employement_status": "Deactive",
        "doe": doe
    }
    user_api_url = "{}/api/hrm/employee/{}/".format(server, employee_id)
    response = requests.put(user_api_url, data=data_edit, headers={'Authorization': 'Token {}'.format(token)})
    print(response.json())

def emp_bind_del(_id):
    emp_bind_url = "{}/api/hrm/employeerolebinding/{}".format(server, _id)
    response = requests.delete(emp_bind_url, headers={'Authorization': 'Token {}'.format(token)})
    print(response)

def remove_emp_bind(emp_id):
    emp_bind_url = "{}/api/hrm/employeerolebinding/?employee_ofx_id={}".format(server, emp_id)
    get_emp_bind_id = requests.get(emp_bind_url, headers={'Authorization': 'Token {}'.format(token)}, verify=False)
    # print(len(get_emp_bind_id.json()))
    if get_emp_bind_id.json():
        for _id in get_emp_bind_id.json():
            print("Employee Found:", emp_id)
            # emp_bind_del(_id)

def get_csv_data():
    with open(employee_csv, 'r', newline='', encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        # print(reader)
        # remove_emp_bind("OFX1617")

        for row in reader:
            # print(row['DOE'])
            # remove_emp_bind(row['EMP ID'])
            # remove_emp_bind("OFX1617")
            # break;
            date_object = datetime.datetime.strptime(row['DOE'], "%d-%b-%Y")
            formatted_date = date_object.strftime("%Y-%m-%d")
            get_employee(row['EMP ID'], formatted_date)
            # update_emp_deo(row['EMP ID'], formatted_date)

if __name__ == '__main__':
    #generate_default_profile_photo()
    #update_username()
    get_csv_data()
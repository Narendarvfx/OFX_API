#  Copyright (c) 2023.
#  Designed & Developed by Narendar Reddy G, OscarFX Private Limited
#  All rights reserved.

import requests
from datetime import *



session = requests.Session()
token = "39bdb2c0347f12746b2fa909c9b48a81247ca120"


emp_dic = []
def get_dep_employees():
    base_url = "https://shotbuzz.oscarfx.com"
    url = base_url + "/api/hrm/employee/?dept=PAINT&role=VFX ARTIST"
    response = session.get(url, headers={'Authorization': 'token {}'.format(token)}, verify=False)
    #print(response.json())
    return response.json()

def get_emp_id():
    artist_id = []
    empty = []
    found = []

    emp_id = get_dep_employees()
    for emp in emp_id:
        e = emp['id']
        try:
            teamlead = emp['team_lead']['fullName']
        except:
            teamlead = ""
        today = date.today()
        d1 = today.strftime("%Y-%m-%d")
        d2 = time.min
        d3 = time.max.strftime("%H:%M:%S")
        ee = "https://shotbuzz.oscarfx.com/api/production/taskdaylogsfilter/?artist_id="+str(e)+"&from_date="+d1+"T"+str(d2)+"&to_date="+d1+"T"+str(d3)
        #print(ee)
        response = session.get(ee, headers={'Authorization': 'token {}'.format(token)}, verify=False)
        #print(response.json())
        if len(response.json()) == 0:
            emp_dic = {'Full_Name':emp['fullName'], 'Employee_id':emp['employee_id'], 'department':emp['department'], 'Team_lead':teamlead}
            empty.append(emp_dic)
        else:
            found.append(e)
    print(empty)
    #print('Found:',found)

get_emp_id()




def get_employee_task():
    pass




# pass the artist id to task day logs
#"https://shotbuzz.oscarfx.com/api/production/taskdaylogsfilter/?artist_id=167&from_date=2022-12-21T00:00:00&to_date=2022-12-21T23:59:59"
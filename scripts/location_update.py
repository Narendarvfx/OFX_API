import requests

server = "http://127.0.0.1:8000"
token = '040734ca148cc9e7a62f2321e2238125204d6b80'

total_data = []
total_pages = 0
shot_location = []
def get_shots():
    api_url = "{}/api/v1/shots/?page_size=20".format(server)
    data = requests.get(api_url, headers={'Authorization': 'Token {}'.format(token)}, verify=False)
    return data.json()['data']
    # print(data.json()['data'])

def update_shot(shot_id):
    api_url = "{}/api/production/shots/{}/".format(server, str(shot_id))
    data = {
        'location': 1
    }
    data = requests.put(api_url,data=data, headers={'Authorization': 'Token {}'.format(token)}, verify=False)
    print(data.json())

for data in get_shots():
    print(data['location'])

    update_shot(data['id'])

# update_shot(2281)
# get_shots()
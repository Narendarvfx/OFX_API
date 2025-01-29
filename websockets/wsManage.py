#  Copyright (c) 2023.
#  Designed & Developed by Narendar Reddy G, OscarFX Private Limited
#  All rights reserved.

import json
import string
import random
from hrm.models import Employee, EmployeeGroups
from hrm.serializers import EmployeeSerializer, EmployeeGroupCompactSerializer


# for every new conncection you should genrate new wstoken for the same user it'll keep all devices connected at same time

class wsManage():

    def __init__(self):
        self.users = {
            # 'zmd2ifra6f1n7x50ml92fko9y4m0a8d8': {"name": "client A", "groups": ['a9546688f6397e8e66e6f58e410d6a',
            #                                                                     '8e7f475ecd7dd73638ddfc6211a881',
            #                                                                     '6d524c5e0345661a442ccbc1f819eb',
            #                                                                     'de4780468d0081c48806715bfdeb67']},
            # 'iwyodqzy2wu61satos0wx4ui060ra84m': {"name": "client B", "groups": ['a9546688f6397e8e66e6f58e410d6a',
            #                                                                     '6d524c5e0345661a442ccbc1f819eb']},
            # '63c316512279c3a6220c9b7c8d97b8': {"name": "client C", "groups": ['8e7f475ecd7dd73638ddfc6211a881',
            #                                                                   'de4780468d0081c48806715bfdeb67']},
            # '99e297252585b1299373477e73c692': {"name": "client D", "groups": ['a9546688f6397e8e66e6f58e410d6a',
            #                                                                   '8e7f475ecd7dd73638ddfc6211a881',
            #                                                                   '6d524c5e0345661a442ccbc1f819eb']},
            # '56d36465c5fffadaedd7ab56fe6790': {"name": "client E", "groups": ['a9546688f6397e8e66e6f58e410d6a',
            #                                                                   '8e7f475ecd7dd73638ddfc6211a881',
            #                                                                   'de4780468d0081c48806715bfdeb67']},
            # '0695747e9cc48a4bf823c8af4c9f14': {"name": "client F", "groups": ['a9546688f6397e8e66e6f58e410d6a',
            #                                                                   '6d524c5e0345661a442ccbc1f819eb',
            #                                                                   'de4780468d0081c48806715bfdeb67']},
            # '11e9542aeb9533cd6b70d9e888da09': {"name": "client J", "groups": ['8e7f475ecd7dd73638ddfc6211a881',
            #                                                                   '6d524c5e0345661a442ccbc1f819eb',
            #                                                                   'de4780468d0081c48806715bfdeb67']},
            # '093be53cc4b9e38380a6f2d02f5951': {"name": "client H", "groups": ['a9546688f6397e8e66e6f58e410d6a',
            #                                                                   'de4780468d0081c48806715bfdeb67']},
            # '8ed41b90e41b53c762143cec0da489': {"name": "client I", "groups": ['8e7f475ecd7dd73638ddfc6211a881',
            #                                                                   '6d524c5e0345661a442ccbc1f819eb']},
            # 'c0afaf268e0c99e302e2c7e21d304e': {"name": "client J", "groups": []}
        }
        self.groups = {
            # 'a9546688f6397e8e66e6f58e410d6a': {"name": "Dev Group"},
            # '8e7f475ecd7dd73638ddfc6211a881': {"name": "Testing Team"},
            # '6d524c5e0345661a442ccbc1f819eb': {"name": "QA Team"},
            # 'de4780468d0081c48806715bfdeb67': {"name": "Prod Team"}
        }

    def getUserData(self, apiKey='',isSelf=False):
        # isSelf is used for get group ids
        try:
            userData = Employee.objects.get(apikey=apiKey)
            serialize_data = EmployeeSerializer(userData)
            userData = json.dumps(serialize_data.data, sort_keys=True,indent=1)
            data = {
                'user': json.loads(userData),
                'groups': {}
            }
            if isSelf is True:
                for g in data['user']['employee_groups']:
                    data['groups'][g['groupkey']] = g
                    # print(self.getGroupData(GroupId=g['groupkey']))
            return data  # None
        except Exception as e:
            print(e)
            return None

    def getGroupData(self, GroupId=''):
        try:
            groupdata = EmployeeGroups.objects.get(groupkey=GroupId)
            serialize_data = EmployeeGroupCompactSerializer(groupdata)
            return json.dumps(serialize_data.data, sort_keys=True, indent=1)
        except Exception as e:
            return None

    def getRandomStrings(self, length=10):
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

    def genarateWSToken(self, apiKey=''):
        return self.getRandomStrings(10)

    def oathUser(self, apiKey='', wsToken=''):
        userData = self.getUserData(apiKey, True)
        # print("UserData:",userData)
        # print("ApiKey:", apiKey)
        # try:
        #     ud = Employee.objects.filter(apikey=apiKey)
        #     print("EmployeeData:", ud[0].apikey)
        # except Exception as e:
        #     print("Error:",e)
        return {
            'status': True if userData is not None else False,
            'uniqId': apiKey,  # this will take a reference of User Account ID, also used for group indexing
            'user': userData['user'] if userData is not None else userData,
            'groups': userData['groups'] if userData is not None else {},
        }

    def saveData(self, fromUser='',fromGroup='',toUsers=[],toGroups=[], data={}):
        # print('Saved_to_data')
        # print(data)
        return True

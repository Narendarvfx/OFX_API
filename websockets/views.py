#  Copyright (c) 2023.
#  Designed & Developed by Narendar Reddy G, OscarFX Private Limited
#  All rights reserved.

from django.shortcuts import render

# import string
# import random
# from string import join
# #for every new conncection you should genrate new wstoken for the same user it'll keep all devices connected at same time

# class dataBase():

#     def __init__(self):
#         pass
    
#     def getRandomStrings(self,length=10):
#         return join(random.choices(string.ascii_lowercase + string.digits, k=length))

#     def genarateWSToken(self,apiKey=''):
#         return self.getRandomStrings(10)
    
#     def oathUser(self,apiKey='',wsToken=''):
#         return {
#             'status': True,
#             'uniqId':apiKey, #this will take a reference of User Account ID, also used for group indexing
#             }
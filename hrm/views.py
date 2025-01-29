#  Copyright (c) 2023.
#  Designed & Developed by Narendar Reddy G, OscarFX Private Limited
#  All rights reserved.
from django.contrib import auth
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from hrm.models import Employee
from django.contrib.auth.models import update_last_login
from rest_framework.authtoken.models import Token



# Create your views here.
def login_view(request):
    """
    Login View
    :param request:
    :return:
    """
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            update_last_login(None, user)
            auth.login(request, user)

            # if user.groups.filter(name='WebUsers').exists():
            #     auth.login(request, user)
                # s = Profile.objects.get(user=user)
                # if s.force_password_change:
                #     context = {
                #         'user':user.id
                #     }
                #     return render(request, 'profile/password_change.html', context=context)
                # else:
            return HttpResponseRedirect('/')

            # else:
            #     return render(request, 'profile/pages-error-403.html')
        else:
            context = {
                'error': 'Wrong Username or Password'
            }

            return render(request, 'profile/login.html', context)
    else:
        return render(request, 'profile/login.html')

def change_password(request):
    user = request.user
    context = {
        'user': user.id
    }
    return render(request, 'profile/password_change.html', context=context)

def logout_view(request):
    """
    Logout View
    :param request:
    :return:
    """
    auth.logout(request)
    return HttpResponseRedirect('/')

def profile_view(request):
    token, created = Token.objects.get_or_create(user=request.user)
    context = {
        'token': token.key,
    }
    return render(request, 'profile/profile.html', context)

def employee_view(request):
    employees = Employee.objects.select_related('profile', 'department', 'role', 'employement_status', 'grade', 'profile__auth_token').prefetch_related(
            'team_lead', 'team_lead__department', 'team_lead__profile', 'team_lead__profile', 'supervisor',
            'supervisor__department', 'employee_groups', 'employee_groups__department', 'profile__groups',
            'profile__user_permissions').filter(department__name= 'PAINT')
    context = {
        'employees' : employees
    }
    return render(request,'main/employeelist.html', context)

def leaves_view(request):
    return render(request,'home/comming_soon.html')

def my_record_view(request):
    return render(request,'home/comming_soon.html')

def test_view(request):
    return HttpResponse("Done")
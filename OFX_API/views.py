#  Copyright (c) 2023.
#  Designed & Developed by Narendar Reddy G, OscarFX Private Limited
#  All rights reserved.

from django.shortcuts import render

from production.models import Clients, Projects, Task_Type

from hrm.models import Employee
def home_view(request):
    """
    Home View
    :param request:
    :return:
    """
    clients = Clients.objects.all()
    projects = Projects.objects.all()
    task_type = Task_Type.objects.all()
    context = {
        'clients': clients,
        'projects': projects,
        'task_type': task_type,
        'user':request.user
    }
    user = Employee.objects.get(profile__id=request.user.id)
    if user.role.name =='CHIEF EXECUTIVE OFFICER' or user.role.name =='CHIEF OPERATING OFFICER' or user.role.name =='CENTRAL PRODUCTION MANAGER' or user.role.name =='HEAD OF PRODUCTION' or user.role.name =='VFX PRODUCER' or user.role.name =='PIPELINE ADMIN':
        return render(request, 'production/studio_report.html', context)
    elif user.role.name =='HEAD OF DEPARTMENT':
        return render(request, 'production/department_report.html', context)
    elif user.role.name =='SUPERVISOR' or user.role.name =='TEAM LEAD':
        return render(request, 'production/myreport_teamlead.html', context)
    elif user.role.name =='VFX ARTIST':
        return render(request, 'production/my_task.html', context)
    else:
        return render(request, 'home/comming_soon.html', context)
    # return render(request, 'home/dashboard.html', context)

# HTTP Error 400
def bad_request(request,*args, **argv):

    return render(request, 'error_pages/pages-error-400.html', status=400)

# HTTP Error 403
def permission_denied(request,*args, **argv):

    return render(request, 'error_pages/pages-error-403.html', status=403)

# HTTP Error 404
def page_not_found(request, *args, **argv):

    return render(request, 'error_pages/pages-error-404.html', status=404)

# HTTP Error 500
def server_error(request, *args, **argv):

    return render(request, 'error_pages/pages-error-500.html', status=500)


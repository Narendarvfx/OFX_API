from django.shortcuts import render

from production.models import Clients, Projects, Task_Type

from django.template import RequestContext

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
    return render(request, 'home/dashboard.html', context)

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
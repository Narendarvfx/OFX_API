from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from django.contrib import auth
from django.http import HttpResponseRedirect

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
        print(user.groups.filter(name='WebUsers').exists())
        if user is not None:
            if user.groups.filter(name='WebUsers').exists():
                auth.login(request, user)
                return HttpResponseRedirect('/')
            else:
                return render(request, 'profile/pages-error-403.html')
        else:
            return render(request, 'profile/login.html', {'message': 'Invalid login credentials'})
    else:
        return render(request, 'profile/login.html')

def logout_view(request):
    """
    Logout View
    :param request:
    :return:
    """
    auth.logout(request)
    return HttpResponseRedirect('/')
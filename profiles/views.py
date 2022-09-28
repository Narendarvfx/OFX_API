from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect, csrf_exempt

from profiles.models import Profile

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
            if user.groups.filter(name='WebUsers').exists():
                auth.login(request, user)
                s = Profile.objects.get(user=user)
                if s.force_password_change:
                    context = {
                        'user':user.id
                    }
                    return render(request, 'profile/password_change.html', context=context)
                else:
                    return HttpResponseRedirect('/')
            else:
                return render(request, 'profile/pages-error-403.html')
        else:
            return render(request, 'profile/login.html', {'message': 'Invalid login credentials'})
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
    return render(request, 'profile/profile.html')
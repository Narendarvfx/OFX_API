from django.shortcuts import render


def home_view(request):
    """
    Home View
    :param request:
    :return:
    """
    return render(request, 'home/dashboard.html')
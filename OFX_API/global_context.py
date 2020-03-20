from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def password_change(request):
    """
    this function will pass the user form to html
    :param request:
    :return:
    """
    html = ''
    if request.method == 'POST':
        password_change_form = PasswordChangeForm(request.user, request.POST)
        if password_change_form.is_valid():
            user = password_change_form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        password_change_form = PasswordChangeForm(request.user)
    return {'password_change_form': password_change_form, 'message': html}
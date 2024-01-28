from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse
from django.shortcuts import redirect


def user_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_user == True:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse("You are not a User")
        else:
            return redirect('cinystoreapp:auth_login')
    return wrapper_func



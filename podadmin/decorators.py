# Decorator functions to restrict the views to the podadmin team

from django.http import HttpResponse
from django.shortcuts import redirect

def podadmin_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_podadmin == True:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse("You are not a podadmin team member")
        else:
            return redirect('/podadmin/login')
    return wrapper_func
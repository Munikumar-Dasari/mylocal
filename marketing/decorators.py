# Decorator funtions to restrict the views to the marketing team

from django.http import HttpResponse
from django.shortcuts import redirect

def marketing_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_marketing == True:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse("You are not a marketing team member")
        else:
            return redirect('marketing:market_login')
    return wrapper_func
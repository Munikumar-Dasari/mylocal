# Decorator function to make the producer view only the pages allowed to the producer

from django.http import HttpResponse
from django.shortcuts import redirect

def producer_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_producer == True:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse("You are not a producer")
        else:
            return redirect('business:producerlogin')
    return wrapper_func
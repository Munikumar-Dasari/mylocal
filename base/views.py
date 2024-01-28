from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader



def index(request):
    return render(request, 'keepitshortbase.html')

def corporate_base(request):
    template = loader.get_template('corporate_base.html')
    context = {
        'corporate_base':corporate_base,
    }
    return HttpResponse(template.render(context, request))

def corporateBase(request):
    template = loader.get_template('corporateBase.html')
    context = {
        'corporateBase':corporateBase,
    }
    return HttpResponse(template.render(context, request))

def admin_base(request):
    template = loader.get_template('admin_base.html')
    context = {
        'admin_base':admin_base,
    }
    return HttpResponse(template.render(context, request))

def base(request):
    template = loader.get_template('base.html')
    context = {
        'base':base,
    }
    return HttpResponse(template.render(context, request))

def businessBase(request):
    template = loader.get_template('businessBase.html')
    context = {
        'businessBase':businessBase,
    }
    return HttpResponse(template.render(context, request))
def corpbase(request):
    template = loader.get_template('corpbase.html')
    context = {
        'corpbase':corpbase,
    }
    return HttpResponse(template.render(context, request))
def head(request):
    template = loader.get_template('head.html')
    context = {
        'head':head,
    }
    return HttpResponse(template.render(context, request))
def keepitshortbase(request):
    template = loader.get_template('keepitshortbase.html')
    context = {
        'keepitshortbase':keepitshortbase,
    }
    return HttpResponse(template.render(context, request))

def kis_team_base(request):
    template = loader.get_template('kis_team_base.html')
    context = {
        'kis_team_base':kis_team_base,
    }
    return HttpResponse(template.render(context, request))
def market_base(request):
    template = loader.get_template('market_base.html')
    context = {
        'market_base':market_base,
    }
    return HttpResponse(template.render(context, request))
def market_base_login(request):
    template = loader.get_template('market_base_login.html')
    context = {
        'market_base_login':market_base_login,
    }
    return HttpResponse(template.render(context, request))
def PodBase(request):
    template = loader.get_template('PodBase.html')
    context = {
        'PodBase':PodBase,
    }
    return HttpResponse(template.render(context, request))
def producer_base(request):
    template = loader.get_template('producer_base.html')
    context = {
        'producer_base':producer_base,
    }
    return HttpResponse(template.render(context, request))

def producerhead(request):
    template = loader.get_template('producerhead.html')
    context = {
        'producerhead':producerhead,
    }
    return HttpResponse(template.render(context, request))

def superadmin_base(request):
    template = loader.get_template('superadmin_base.html')
    context = {
        'superadmin_base':superadmin_base,
    }
    return HttpResponse(template.render(context, request))
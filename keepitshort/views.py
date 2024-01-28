from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader



def index(request):
    return render(request, 'keepitshort.html')

def keepitshortbase(request):
    template = loader.get_template('keepitshortbase.html')
    context = {
        'keepitshortbase':keepitshort,
    }
    return HttpResponse(template.render(context, request))

# Create your views here.


def keepitshort(request):
    template = loader.get_template('keepitshort.html')
    context = {
        'keepitshort':keepitshort,
    }
    return HttpResponse(template.render(context, request))

# Create your views here.
def kis_team_account(request):
    template = loader.get_template('kis_team_account.html')
    context = {
        'kis_team_account':kis_team_account,
    }
    return HttpResponse(template.render(context, request))

def kis_team_login(request):
    template = loader.get_template('kis_team_login.html')
    context = {
        'kis_team_login':kis_team_login,
    }
    return HttpResponse(template.render(context, request))

def kis_team_dashboard(request):
    template = loader.get_template('kis_team_dashboard.html')
    context = {
        'kis_team_dashboard':kis_team_dashboard,
    }
    return HttpResponse(template.render(context, request))

def kis_team_Logout(request):
    template = loader.get_template('kis_team_Logout.html')
    context = {
        'kis_team_Logout':kis_team_Logout,
    }
    return HttpResponse(template.render(context, request))

def activate_kis_team(request):
    template = loader.get_template('activate_kis_team.html')
    context = {
        'activate_kis_team':activate_kis_team,
    }
    return HttpResponse(template.render(context, request))  

def kis_team_register(request): 
    template = loader.get_template('kis_team_register.html')
    context = {
        'kis_team_register':kis_team_register,
    }
    return HttpResponse(template.render(context, request))  

def kis_team_reset_password(request):    
    template = loader.get_template('kis_team_reset_password.html')
    context = {
        'kis_team_reset_password':kis_team_reset_password,
    }
    return HttpResponse(template.render(context, request))

def kis_team_reset_confirm(request):        
    template = loader.get_template('kis_team_reset_confirm.html')
    context = {
        'kis_team_reset_confirm':kis_team_reset_confirm,
    }
    return HttpResponse(template.render(context, request))

def kis_team_change_password(request):        
    template = loader.get_template('kis_team_change_password.html')
    context = {
        'kis_team_change_password':kis_team_change_password,
    }
    return HttpResponse(template.render(context, request))  

def kis_team_profile(request):        
    template = loader.get_template('kis_team_profile.html')
    context = {
        'kis_team_profile':kis_team_profile,
    }
    return HttpResponse(template.render(context, request))  

def kis_team_update_profile(request):        
    template = loader.get_template('kis_team_update_profile.html')
    context = {
        'kis_team_update_profile':kis_team_update_profile,
    }
    return HttpResponse(template.render(context, request))  

def kis_team_content(request):        
    template = loader.get_template('kis_team_content.html')
    context = {
        'kis_team_content':kis_team_content,
    }
    return HttpResponse(template.render(context, request))

def kis_team_statistics(request):     
    template = loader.get_template('kis_team_statistics.html')
    context = {
        'kis_team_statistics':kis_team_statistics,
    }
    return HttpResponse(template.render(context, request))  

def kis_team_submitlabel(request):     
    template = loader.get_template('kis_team_submitlabel.html')
    context = {
        'kis_team_submitlabel':kis_team_submitlabel,
    }
    return HttpResponse(template.render(context, request))  

def kis_institute_register(request):
    template = loader.get_template('kis_institute_register.html')
    context = {
        'kis_institute_register':kis_institute_register,
    }
    return HttpResponse(template.render(context, request))

def kis_institute_login(request):
    template = loader.get_template('kis_institute_login.html')
    context = {
        'kis_institute_login':kis_institute_login,
    }
    return HttpResponse(template.render(context, request))

def kis_institute_details(request):
    template = loader.get_template('kis_institute_details.html')
    context = {
        'kis_institute_details':kis_institute_register,
    }
    return HttpResponse(template.render(context, request))

def kis_team_dashboard(request):
    template = loader.get_template('kis_team_dashboard.html')
    context = {
        'kis_team_dashboard':kis_team_dashboard,
    }
    return HttpResponse(template.render(context, request))

def kis_create_team(request):
    template = loader.get_template('kis_create_team.html')
    context = {
        'kis_create_team':kis_create_team,
    }
    return HttpResponse(template.render(context, request))

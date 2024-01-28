from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail
from cinystore import settings
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from cinystoreapp.tokens import generate_token
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from cinystoreapp.models import *
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.views import View
import random
import http.client
from django.conf import settings


def index(request):
    return render(request, 'login.html')


def superadmin_account(request):
    template = loader.get_template('superadmin_account.html')
    context = {
        'superadmin_account': superadmin_account,
    }
    return HttpResponse(template.render(context, request))

def superadmin_add_clips(request):
    template = loader.get_template('superadmin_add_clips.html')
    context = {
        'superadmin_add_clips': superadmin_add_clips,
    }
    return HttpResponse(template.render(context, request))


def superadmin_add_post(request):
    template = loader.get_template('superadmin_add_post.html')
    context = {
        'superadmin_add_post': superadmin_add_post,
    }
    return HttpResponse(template.render(context, request))


def superadmin_base(request):
    template = loader.get_template('superadmin_base.html')
    context = {
        'superadmin_base': superadmin_base,
    }
    return HttpResponse(template.render(context, request))


def superadmin_content(request):
    template = loader.get_template('superadmin_content.html')
    context = {
        'superadmin_content': superadmin_content,
    }
    return HttpResponse(template.render(context, request))


def superadmin_statistics(request):
    template = loader.get_template('superadmin_statistics.html')
    context = {
        'superadmin_statistics': superadmin_statistics,
    }
    return HttpResponse(template.render(context, request))



def businessBase(request):
    template = loader.get_template('businessBase.html')
    context = {
        'businessBase': businessBase,
    }
    return HttpResponse(template.render(context, request))


def corporateBase(request):
    template = loader.get_template('corporateBase.html')
    context = {
        'corporateBase': corporateBase,
    }
    return HttpResponse(template.render(context, request))



def login(request):
    template = loader.get_template('login.html')
    context = {
        'login': login,
    }
    return HttpResponse(template.render(context, request))



def registerPage(request):
    template = loader.get_template('registerPage.html')
    context = {
        'registerPage': registerPage,
    }
    return HttpResponse(template.render(context, request))
















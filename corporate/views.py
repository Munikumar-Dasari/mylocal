from configparser import ConfigParser
from cinystore import settings
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .forms import ContactForm
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
import requests
from marketing.models import Privacy1, Terms
import mysql.connector
from .models import *
from marketing.models import Blog



db = mysql.connector.connect(
  host="3.109.48.139",
  user="myuser",
  password="cinystore",
  database="cinystore"
)
cursor = db.cursor()


def index(request):
   return render(request, 'corporate.html')


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()  # This saves the form data to the database. Send an email to the company
            subject = 'Contact Form Submission'
            message = f"Name: {form.cleaned_data['Name']}\nEmail: {form.cleaned_data['Email']}\nSubject: {form.cleaned_data['Subject']}\nMessage: {form.cleaned_data['Message']}"
            from_email = 'settings.EMAIL_HOST_USER'
            recipient_list = ['varun.agarwal@cinystore.com']

            send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        return redirect('contact')  # Redirect to a success page
    else:
        form = ContactForm()
    return render(request, 'contactPage.html', {'form': form})

def creator(request):
    template  = loader.get_template('creatorPage.html')
    context = {
        'creator': creator,
    }
    return HttpResponse(template.render(context, request))


def allblogs(request):
    mydata = Blog.objects.all()
    template = loader.get_template('allblogs.html')
    context = {
        'Blog': mydata
    }
    return HttpResponse(template.render(context, request))


def blog(request, slug):
    mydata = Blog.objects.filter(slug=slug)
    template = loader.get_template('Blog.html')
    context = {
        'Blog': mydata
    }
    return HttpResponse(template.render(context, request))
   
def faq(request):
    template  = loader.get_template('faqPage.html')
    context = {
        'faq': faq,
    }
    return HttpResponse(template.render(context, request))


def index(request):
    #template  = loader.get_template('corporate.html')
    # context = {
    #     'corporateHome': corporateHome,
    # }
    return render(request, 'corporate.html')


def reviews(request):
    template  = loader.get_template('reviewsPage.html')
    context = {
        'reviews': reviews,
    }
    return HttpResponse(template.render(context, request))



def Privacy(request):
    mydata = Privacy1.objects.all().order_by('timestamp_field')
    template = loader.get_template('Privacy.html')
    context = {
        'Privacy': mydata,
    }
    return HttpResponse(template.render(context, request))


def terms(request):
    mydata = Terms.objects.all().order_by('timestamp_field')
    template = loader.get_template('terms.html')
    context = {
        'terms': mydata,
    }
    return HttpResponse(template.render(context, request))


def corporate(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()  # This saves the form data to the database. Send an email to the company
            subject = 'Contact Form Submission'
            message = f"Name: {form.cleaned_data['Name']}\nEmail: {form.cleaned_data['Email']}\nSubject: {form.cleaned_data['Subject']}\nMessage: {form.cleaned_data['Message']}"
            from_email = 'settings.EMAIL_HOST_USER'
            recipient_list = ['varun.agarwal@cinystore.com']

            send_mail(subject, message, from_email, recipient_list, fail_silently=False)

            return redirect('corporate')  # Redirect to a success page
    else:
        form = ContactForm()
    return render(request, 'corporate.html', {'form': form})












from django.contrib.auth.models import AbstractUser
from django.db import models
from cinystoreapp.models import User
from phonenumber_field.modelfields import PhoneNumberField
from uuid import uuid4
import os
from datetime import datetime
from django.utils import timezone


def rename_marketing(instance, filename):
    upload_to = 'marketing/'
    ext = filename.split('.')[-1]
    # username = user.username
    if instance.profile_image:
        filename = '{}_{}.{}'.format(instance.username,datetime.now(), ext)
    else:
        filename ='{}_{}.{}'.format(uuid4.hex, datetime.now(), ext)
    return os.path.join(upload_to, filename)



class MarketingRegister(models.Model):
    marketing = models.OneToOneField(User, on_delete = models.CASCADE, primary_key = True)
    username = models.CharField(max_length=45)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = PhoneNumberField() 
    email = models.CharField(max_length=100)
    profile_image = models.ImageField(upload_to=rename_marketing, default='marketing/blank_profile.webp', null=True)
    last_login = models.DateTimeField(verbose_name='last login', blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'marketing_register'


def path_and_rename_blog(instance, filename):
    upload_to = 'blogPoster/'
    ext = filename.split('.')[-1]
    # get filename
    if instance.Blog_name:
        filename = '{}_{}.{}'.format(instance.Blog_name,datetime.now(), ext)
    else:
        # set filename as random string
        filename = '{}_{}.{}'.format(uuid4().hex,datetime.now(), ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)

   
class Blog(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    Author = models.ForeignKey(MarketingRegister, on_delete=models.CASCADE)
    username = models.CharField(max_length=45)
    Blog_name = models.CharField(max_length=100)
    Introduction = models.TextField(max_length=5000)
    Conclusion = models.TextField(max_length=5000)
    Image1 = models.ImageField(upload_to=path_and_rename_blog, blank=True)
    Image2 = models.ImageField(upload_to=path_and_rename_blog, blank=True)
    description1 = models.TextField(max_length=5000)
    description2 = models.TextField(max_length=5000)
    description3 = models.TextField(max_length=5000, null=True, blank=True, default='True')
    description4 = models.TextField(max_length=5000, null=True, blank=True, default='True')
    heading1 = models.TextField(max_length=200)
    heading2 = models.TextField(max_length=200)
    heading3 = models.TextField(max_length=200, null=True, blank=True, default='True')
    heading4 = models.TextField(max_length=200, null=True, blank=True, default='True')
    slug = models.SlugField(null=True, blank=True, default='True')
    timestamp_field = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp_field']
        db_table = 'blog'

    def __str__(self):
        return '%s - %s' % (self.Blog_name, self.timestamp_field)


class Privacy1(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    text = models.CharField(max_length=5000)
    Heading = models.CharField(max_length=200, null=True, blank=True, default='')
    timestamp_field = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'privacy'
        ordering = ['timestamp_field']
    def __str__(self):
        return '%s - %s' % (self.Heading, self.text)


class Terms(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    text = models.CharField(max_length=5000)
    Heading = models.CharField(max_length=200, null=True, blank=True, default='')
    timestamp_field = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'terms'
        ordering = ['timestamp_field']

    def __str__(self):
        return '%s - %s' % (self.Heading, self.text)


class Guidelines(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    text = models.CharField(max_length=5000)
    Heading = models.CharField(max_length=200, null=True, blank=True, default='')
    timestamp_field = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'guidelines'
        ordering = ['timestamp_field']
    def __str__(self):
        return '%s - %s' % (self.Heading, self.text)

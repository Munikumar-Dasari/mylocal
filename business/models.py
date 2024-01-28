from django.contrib.auth.models import AbstractUser
from django.db import models
from cinystoreapp.models import User
from uuid import uuid4
from datetime import datetime
import os
from phonenumber_field.modelfields import PhoneNumberField
import phonenumbers
from cinystoreapp.models import *
from podadmin.models import *
from podadmin.models import PostText1, Clips, CreateLabel


class CorporateRegister(models.Model):
    producer = models.OneToOneField(User, on_delete = models.CASCADE, primary_key = True)
    username = models.CharField(max_length=45)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    production_house = models.CharField(max_length=100)
    website = models.CharField(max_length=50)
    country_name = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    company_brief = models.CharField(max_length=2000)
    phone_number = PhoneNumberField(default= None)
    last_login = models.DateTimeField(verbose_name='last login', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    facebook_account = models.CharField(max_length=100, null=True)
    twitter_account = models.CharField(max_length=100, null=True)

    class Meta:
        db_table = 'corporateregister'


class IndividualRegister(models.Model):
    producer = models.OneToOneField(User, on_delete = models.CASCADE, primary_key = True)
    username = models.CharField(max_length=45)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    production_house = models.CharField(max_length=100)
    website = models.CharField(max_length=50)
    country_name = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    company_brief = models.CharField(max_length=2000)
    phone_number = PhoneNumberField(default=None)
    last_login = models.DateTimeField(verbose_name='last login', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    facebook_account = models.CharField(max_length=100, null=True)
    twitter_account = models.CharField(max_length=100, null=True)

    class Meta:
        db_table = 'individualregister'

class OttRegister(models.Model):
    producer = models.OneToOneField(User, on_delete = models.CASCADE, primary_key = True)
    username = models.CharField(max_length=45)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    production_house = models.CharField(max_length=100)
    website = models.CharField(max_length=50)
    country_name = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    company_brief = models.CharField(max_length=2000)
    phone_number = PhoneNumberField(default=None)
    last_login = models.DateTimeField(verbose_name='last login', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    facebook_account = models.CharField(max_length=100, null=True)
    twitter_account = models.CharField(max_length=100, null=True)

    class Meta:
        db_table = 'ottregister'


class AgencyRegister(models.Model):
    producer = models.OneToOneField(User, on_delete = models.CASCADE, primary_key = True)
    username = models.CharField(max_length=45)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    production_house = models.CharField(max_length=100)
    website = models.CharField(max_length=50)
    country_name = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    company_brief = models.CharField(max_length=2000)
    phone_number = PhoneNumberField(default=None)
    last_login = models.DateTimeField(verbose_name='last login', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    facebook_account = models.CharField(max_length=100, null=True)
    twitter_account = models.CharField(max_length=100, null=True)

    class Meta:
        db_table = 'agencyregister'


def path_and_rename(instance, filename):
    upload_to = 'Posters/'
    ext = filename.split('.')[-1]
    # get filename
    if instance.Movie_name:
        filename = '{}_{}.{}'.format(instance.Movie_name,datetime.now(), ext)
    else:
        # set filename as random string
        filename = '{}_{}.{}'.format(uuid4().hex,datetime.now(), ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)


class SubmitLabel(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    Movie_name = models.CharField(max_length=100)
    Language = models.CharField(max_length=100)
    Genre = models.CharField(max_length=100)
    Production_house = models.CharField(max_length=50)
    Producer = models.CharField(max_length=100)
    cast = models.CharField(max_length=250)
    Director = models.CharField(max_length=100)
    Music_director = models.CharField(max_length=100)
    Poster = models.ImageField(upload_to= path_and_rename , blank=True, null=True)
    Banner = models.ImageField(upload_to= path_and_rename, blank=True, null=True)
    Release_date = models.DateField(max_length=100, default='TBA')
    synopsis = models.CharField(max_length=2000)
    trailer = models.CharField(max_length=255)
    timestamp_field = models.DateTimeField(auto_now_add=True)
    model_type = models.CharField(max_length=100, default='mydata')
    producer_id = models.ForeignKey('cinystoreapp.ProducerRegister', default=1, verbose_name="producer_register", on_delete=models.SET_DEFAULT, db_column='producer_id')
    Url_name = models.CharField(max_length=100,default=None, null=True)
    Other_Languages = models.CharField(max_length=100, null=True)
    lyricist = models.CharField(max_length=100, null=True)
    choreographer = models.CharField(max_length=100, null=True)
    Script_writer = models.CharField(max_length=100, null=True)
    Running_Time = models.CharField(max_length=100, null=True)
    Maturity = models.CharField(max_length=100, null=True)
    Budget = models.CharField(max_length=100, null=True)
    Distribution = models.CharField(max_length=100, null=True)
    Recording_studio = models.CharField(max_length=100, null=True)
    Graphic_designer = models.CharField(max_length=100, null=True)
    like_count = models.BigIntegerField(null=True, blank=True, default='0')
    follow_count = models.BigIntegerField(null=True, blank=True, default='0')
    share_count = models.BigIntegerField(null=True, blank=True, default='0')
    comment_count = models.BigIntegerField(null=True, blank=True, default='0')
    Singers = models.CharField(max_length=100, null=True)
    Editor = models.CharField(max_length=100, null=True)
    Cinematographer = models.CharField(max_length=100, null=True)
    source = models.CharField(max_length=100, null= True, blank=True, default='Cinystore News Network')
    logo = models.CharField(max_length=255, null= True, blank=True, default='User/blank_profile.webp')
    status = models.CharField(max_length=100, default='Pending')


    class Meta:
        db_table = 'submit_label'
        ordering = ['-timestamp_field']


    def __str__(self):
        return self.Movie_name

def path_rename_video(instance, filename):
    upload_to = 'videos/'
    ext = filename.split('.')[-1]
    # get filename
    if instance.Movie_name:
        filename = '{}_{}.{}'.format(instance.Movie_name,datetime.now(), ext)
    else:
        # set filename as random string
        filename = '{}_{}.{}'.format(uuid4().hex,datetime.now(), ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)


class SubmitClips(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    Heading = models.CharField(max_length=200, null=True, blank=True, default='')
    text = models.CharField(max_length=2000)
    Movie_name = models.CharField(max_length=100)
    Video = models.FileField(upload_to= path_rename_video, null=True, verbose_name="")
    Image = models.ImageField(upload_to='Posters/', blank=True)
    timestamp_field = models.DateTimeField(auto_now_add=True)
    model_type = models.CharField(max_length=100, default='mydata2')
    like_count = models.BigIntegerField(null=True, blank=True, default=False)
    comment_count = models.BigIntegerField(null=True, blank=True, default=False)
    share_count = models.BigIntegerField(null=True, blank=True, default=False)
    Language = models.CharField(max_length=100, null=True, blank=True)
    Genre = models.CharField(max_length=100, null=True, blank=True)
    source = models.CharField(max_length=100, null=True, blank=True, default='Cinystore News Network')
    logo = models.CharField(max_length=255, null=True, blank=True, default='Users/blank_profile.webp')
    slug = models.SlugField()
    status = models.CharField(max_length=100, default='Pending')
    auto_created = True,

    def _str_(self) -> str:
        return self.Movie_name

    class Meta:
        db_table = 'submit_clips'
        ordering = ['-timestamp_field']


def path_and_rename_post(instance, filename):
    upload_to = 'Posttext/'
    ext = filename.split('.')[-1]
    # get filename
    if instance.Movie_name:
        filename = '{}_{}.{}'.format(instance.Movie_name,datetime.now(), ext)
    else:
        # set filename as random string
        filename = '{}_{}.{}'.format(uuid4().hex,datetime.now(), ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)

class SubmitPost(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    Movie_name = models.CharField(max_length=100)
    text = models.CharField(max_length=2000)
    Image = models.ImageField(upload_to=path_and_rename_post, blank=True)
    Heading = models.CharField(max_length=200, null=True, blank=True, default='')
    timestamp_field = models.DateTimeField(auto_now_add=True)
    model_type = models.CharField(max_length=100, default='mydata3')
    like_count = models.BigIntegerField(null=True, blank=True, default='0')
    comment_count = models.BigIntegerField(null=True, blank=True, default='0')
    share_count = models.BigIntegerField(null=True, blank=True, default='0')
    follow_count = models.BigIntegerField(null=True, blank=True, default='0')
    Language = models.CharField(max_length=100, null=True, blank=True)
    Genre = models.CharField(max_length=100, null=True, blank=True)
    source = models.CharField(max_length=100, null=True, blank=True, default='Cinystore News Network')
    logo = models.CharField(max_length=255, null= True, blank=True, default='Users/blank_profile.webp')
    slug = models.SlugField(default=0)
    status = models.CharField(max_length=100, default='Pending')
    auto_created = True,

    class Meta:
        db_table = 'submit_post'
        ordering = ['-timestamp_field']

    def __str__(self):
        return '%s - %s - %s - %s - %s - %s - %s' % (self.Movie_name, self.text, self.Heading, self.like_count, self.comment_count, self.share_count, self.follow_count)


class UserLikes(models.Model):
    id = models.BigAutoField(auto_created=True,primary_key=True, serialize=False, verbose_name='ID')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, blank= True, null=True)
    label = models.ForeignKey(CreateLabel, on_delete=models.CASCADE, blank= True, null=True)
    post = models.ForeignKey(PostText1, on_delete=models.CASCADE, blank= True, null=True)
    review = models.ForeignKey(Review, on_delete=models.CASCADE, blank= True, null=True)
    clip = models.ForeignKey(Clips, on_delete=models.CASCADE, blank= True, null=True)
    model_type = models.CharField(max_length=100, null=False, blank=False)
    timestamp_field = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'userlikes'
        ordering = ['timestamp_field']

    def __str__(self):
        return self.user
    
class UserFollows(models.Model):
    id = models.BigAutoField(auto_created=True,primary_key=True, serialize=False, verbose_name='ID')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, blank= True, null=True)
    label = models.ForeignKey(CreateLabel, on_delete=models.CASCADE, blank= True, null=True)
    model_type = models.CharField(max_length=100)
    timestamp_field = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'userfollows'
        ordering = ['timestamp_field']

    def __str__(self):
        return self.user
    
class UserComments(models.Model):
    id = models.BigAutoField(auto_created=True,primary_key=True, serialize=False, verbose_name='ID')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, blank= True, null=True)
    label = models.ForeignKey(CreateLabel, on_delete=models.CASCADE, blank= True, null=True)
    post = models.ForeignKey(PostText1, on_delete=models.CASCADE, blank= True, null=True)
    review = models.ForeignKey(Review, on_delete=models.CASCADE, blank= True, null=True)
    clip = models.ForeignKey(Clips, on_delete=models.CASCADE, blank= True, null=True)
    comments = models.CharField(max_length=1000)
    model_type = models.CharField(max_length=100, null=False, blank=False)
    like_count = models.BigIntegerField(null=True, blank=True, default='0')
    report_count = models.BigIntegerField(null=True, blank=True, default='0')
    timestamp_field = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'usercomments'
        ordering = ['timestamp_field']

    def __str__(self):
        return self.user

class UserShares(models.Model):
    id = models.BigAutoField(auto_created=True,primary_key=True, serialize=False, verbose_name='ID')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, blank= True, null=True)
    label = models.ForeignKey(CreateLabel, on_delete=models.CASCADE, blank= True, null=True)
    post = models.ForeignKey(PostText1, on_delete=models.CASCADE, blank= True, null=True)
    review = models.ForeignKey(Review, on_delete=models.CASCADE, blank= True, null=True)
    clip = models.ForeignKey(Clips, on_delete=models.CASCADE, blank= True, null=True)
    model_type = models.CharField(max_length=100)
    timestamp_field = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'usershares'
        ordering = ['timestamp_field']

    def __str__(self):
        return self.user

class UserSearches(models.Model):
    id = models.BigAutoField(auto_created=True,primary_key=True, serialize=False, verbose_name='ID')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    search_query = models.CharField(max_length=100)
    timestamp_field = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'usersearches'
        ordering = ['timestamp_field']

    def __str__(self):
        return self.user


class AbuseReport(models.Model):
    id = models.BigAutoField(auto_created=True,primary_key=True, serialize=False, verbose_name='ID')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, blank= True, null=True)
    label = models.ForeignKey(CreateLabel, on_delete=models.CASCADE, blank= True, null=True)
    post = models.ForeignKey(PostText1, on_delete=models.CASCADE, blank= True, null=True)
    review = models.ForeignKey(Review, on_delete=models.CASCADE, blank= True, null=True)
    clip = models.ForeignKey(Clips, on_delete=models.CASCADE, blank= True, null=True)
    model_type = models.CharField(max_length=100)
    reason = models.CharField(max_length=1000)
    timestamp_field = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'abusereport'
        ordering = ['timestamp_field']

    def __str__(self):
        return self.user
    
class NotInterested(models.Model):
    id = models.BigAutoField(auto_created=True,primary_key=True, serialize=False, verbose_name='ID')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, blank= True, null=True)
    label = models.ForeignKey(CreateLabel, on_delete=models.CASCADE, blank= True, null=True)
    post = models.ForeignKey(PostText1, on_delete=models.CASCADE, blank= True, null=True)
    review = models.ForeignKey(Review, on_delete=models.CASCADE, blank= True, null=True)
    clip = models.ForeignKey(Clips, on_delete=models.CASCADE, blank= True, null=True)
    reason = models.CharField(max_length=1000)
    model_type = models.CharField(max_length=100)
    timestamp_field = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'notinterested'
        ordering = ['timestamp_field']

    def __str__(self):
        return self.user


class ReportComments(models.Model):
    id = models.BigAutoField(auto_created=True,primary_key=True, serialize=False, verbose_name='ID')
    reporting_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Reporting_user')
    reported_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Reported_user')
    reason = models.CharField(max_length=1000)
    comment = models.ForeignKey(UserComments, default=True, verbose_name="usercomments", on_delete=models.CASCADE)
    comments = models.CharField(max_length = 1000)
    movie_name = models.CharField(max_length=255, default=None)
    username = models.CharField(max_length=255, default=None)
    timestamp_field = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'report_comment'
        ordering = ['timestamp_field']

    def __str__(self):
        return '%s - %s' % (self.username, self.movie_name)

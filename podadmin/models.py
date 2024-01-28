from django.contrib.auth.models import AbstractUser
from django.db import models
from cinystoreapp.models import User
# import uuid4 and datetime
import uuid as uuid4
from datetime import datetime
import os
from cinystoreapp.models import ProducerRegister


class PodAdmin(models.Model):
    pod = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    pod_name = models.CharField(max_length=100)
    pod_email = models.EmailField(max_length=100)
    pod_phone = models.CharField(max_length=100)
    pod_created_at = models.DateTimeField(auto_now_add=True)
    pod_is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'podadmin'

    def __str__(self):
        return self.pod_name
    

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


class CreateLabel(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    Movie_name = models.CharField(max_length=100)
    Language = models.CharField(max_length=100)
    Genre = models.CharField(max_length=100)
    Production_house = models.CharField(max_length=50)
    Producer = models.CharField(max_length=100)
    cast = models.CharField(max_length=250)
    Director = models.CharField(max_length=100)
    Music_director = models.CharField(max_length=100)
    Poster = models.ImageField(upload_to= path_and_rename , blank=True)
    Banner = models.ImageField(upload_to= path_and_rename, blank=True)
    Release_date = models.DateField(max_length=100)
    synopsis = models.CharField(max_length=2000)
    trailer = models.CharField(max_length=255)
    timestamp_field = models.DateTimeField(auto_now_add=True)
    model_type = models.CharField(max_length=100, default='mydata')
    producer_id = models.ForeignKey(ProducerRegister, default=1, verbose_name="producer_register", on_delete=models.SET_DEFAULT, db_column='producer_id')
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


    class Meta:
        db_table = 'Create_label'
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


class Clips(models.Model):
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
    source = models.CharField(max_length=100, null=True, blank=True, default='Cinystore News Network')
    logo = models.CharField(max_length=255, null=True, blank=True, default='Users/blank_profile.webp')
    slug = models.SlugField()
    Language = models.CharField(max_length=100, null=True, blank=True)
    Genre = models.CharField(max_length=100, null=True, blank=True)

    auto_created = True,

    def _str_(self) -> str:
        return self.Movie_name

    class Meta:
        db_table = 'Clips'
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


class PostText1(models.Model):
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
    Language = models.CharField(max_length=100, null=True, blank=True)
    Genre = models.CharField(max_length=100, null=True, blank=True)
    follow_count = models.BigIntegerField(null=True, blank=True, default='0')
    source = models.CharField(max_length=100, null=True, blank=True, default='Cinystore News Network')
    logo = models.CharField(max_length=255, null= True, blank=True, default='Users/blank_profile.webp')
    slug = models.SlugField(default=0)
    auto_created = True,

    class Meta:
        db_table = 'PostText'
        ordering = ['-timestamp_field']

    def __str__(self):
        return '%s - %s - %s - %s - %s - %s - %s' % (self.Movie_name, self.text, self.Heading, self.like_count, self.comment_count, self.share_count, self.follow_count)


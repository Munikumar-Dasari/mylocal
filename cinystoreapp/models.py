#from django.contrib.auth.models import User
from django.utils import timezone
import os
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from uuid import uuid4
import os
from datetime import datetime


''' Custom Model'''
from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

class User(AbstractUser):
    is_user = models.BooleanField(default=False)
    is_producer = models.BooleanField(default=False)
    is_marketing = models.BooleanField(default=False)
    is_podadmin = models.BooleanField(default=False)
    is_keepitshort = models.BooleanField(default=False)
    phone_numbers = models.OneToOneField('PhoneNumber', related_name='users',null=True, on_delete=models.CASCADE)
    email = models.EmailField(unique=True, blank=True, null=True)

    class Meta:
        unique_together = ('username','phone_numbers')

class PhoneNumber(models.Model):
    number = PhoneNumberField()  # Define your field for phone numbers
    email = models.EmailField(null=True, blank=True)
    # user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='phone_numbers')
    otp  = models.IntegerField(null=True, blank=True)
    uid = models.UUIDField(default=uuid4, editable=False, unique=True)

    def __str__(self):
        return str(self.number)
    
    class Meta:
        db_table = 'phone_number'


def rename(instance, filename):
    upload_to = 'Users/'
    ext = filename.split('.')[-1]
    # username = user.username
    if instance.username:
        filename = '{}_{}.{}'.format(instance.username,datetime.now(), ext)
    else:
        filename ='{}_{}.{}'.format(uuid4.hex, datetime.now(), ext)
    return os.path.join(upload_to, filename)

class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, primary_key = True)
    username = models.CharField(max_length=45)
    profilephoto = models.ImageField(upload_to=rename, default='Users/blank_profile.webp', null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    website = models.CharField(max_length=50)
    date_of_birth = models.DateField(max_length=100, default='2000-01-01')
    phone_number = PhoneNumberField() 
    country_name = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    company_brief = models.CharField(max_length=2000)
    gender = models.CharField(max_length=255)
    facebook_account = models.CharField(max_length=100)
    twitter_account = models.CharField(max_length=100)
    spotify_account = models.CharField(max_length=100)
    class Meta:
        db_table = 'user_info'
    def __str__(self):
        return '%s - %s' % (self.username, self.email)



def rename_producer(instance, filename):
    upload_to = 'Producers/'
    ext = filename.split('.')[-1]
    # username = user.username
    if instance.production_house_image:
        filename = '{}_{}.{}'.format(instance.production_house,datetime.now(), ext)
    else:
        filename ='{}_{}.{}'.format(uuid4.hex, datetime.now(), ext)
    return os.path.join(upload_to, filename)

class ProducerRegister(models.Model):
    producer = models.OneToOneField(User, on_delete = models.CASCADE, primary_key = True)
    production_house_image = models.ImageField(upload_to=rename_producer, default='Producers/blank_profile.webp', null=True)
    producer_first_name = models.CharField(max_length=100)
    producer_last_name = models.CharField(max_length=100)
    producer_email = models.CharField(max_length=100)
    production_house = models.CharField(max_length=100)
    producer_website = models.CharField(max_length=50)
    producer_phone_number = models.CharField(max_length=20)
    producer_country_name = models.CharField(max_length=100)
    producer_state = models.CharField(max_length=100)
    producer_city = models.CharField(max_length=100)
    production_house_brief = models.CharField(max_length=2000)
    producer_facebook_account = models.CharField(max_length=100)
    producer_twitter_account = models.CharField(max_length=100)
    last_login = models.DateTimeField(verbose_name='last login', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_agency = models.BooleanField(default=False)
    is_ott = models.BooleanField(default=False)
    is_individual = models.BooleanField(default=False)
    is_corporate = models.BooleanField(default=False)

    class Meta:
        db_table = 'Producerregister'
    
    def __str__(self):
        return '%s - %s' % (self.production_house, self.producer_email)




class Movie(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    movie_title = models.CharField(max_length=255)
    overview = models.TextField(max_length=1000)
    release_date = models.DateField(max_length=100, null=True)
    poster_path = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)
    genre = models.CharField(max_length=100, default=False, null=True)
    language = models.CharField(max_length=50, default=False, null=True)
    video = models.URLField(default=False, null=True)
    producer = models.CharField(max_length=100, default=False, null=True)
    director = models.CharField(max_length=100,  default=False, null=True)
    music_director = models.CharField(max_length=100, default=False, null=True)
    crew = models.CharField(max_length=100,  default=False, null=True)
    cast = models.CharField(max_length=2000, default=False, null=True)
    timestamp_field = models.DateTimeField(default=timezone.now)
    model_type = models.CharField(max_length=50, default='movies')
    like_count = models.BigIntegerField(null=True, blank=True, default='0')
    follow_count = models.BigIntegerField(null=True, blank=True, default='0')
    share_count = models.BigIntegerField(null=True, blank=True, default='0')
    comment_count = models.BigIntegerField(null=True, blank=True, default='0')
    source = models.CharField(max_length=100, null= True, blank=True, default='TMDB')
    logo = models.CharField(max_length=100, null= True, blank=True, default='TMDB/TMDB_logo.png')
    slug = models.SlugField(default=0)

    class Meta:
        ordering = ['-timestamp_field']
        db_table = 'movie'

    def __str__(self):
        return f"{self.movie_title}'s model"



def path_and_rename_webseries_label(instance, filename):
    upload_to = 'WebSeriesPoster/'
    ext = filename.split('.')[-1]
    # get filename
    if instance.webseries_name:
        filename = '{}_{}.{}'.format(instance.webseries_name,datetime.now(), ext)
    else:
        # set filename as random string
        filename = '{}_{}.{}'.format(uuid4().hex,datetime.now(), ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)


class WebSeriesLabel(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    webseries_name = models.CharField(max_length=100)
    Language = models.CharField(max_length=100)
    Genre = models.CharField(max_length=100)
    Production_house = models.CharField(max_length=50)
    Producer = models.CharField(max_length=100)
    cast = models.CharField(max_length=250)
    Director = models.CharField(max_length=100)
    season = models.CharField(max_length=100)
    episodes = models.CharField(max_length=100)
    streaming_on = models.CharField(max_length=100)
    Poster = models.ImageField(upload_to= path_and_rename_webseries_label , blank=True)
    Release_date = models.DateField(max_length=100)
    synopsis = models.CharField(max_length=2000)
    trailer = models.CharField(max_length=255)
    timestamp_field = models.DateTimeField(auto_now_add=True)
    model_type = models.CharField(max_length=100, default='webseriesdata')
    producer_id = models.ForeignKey('ProducerRegister', default=1, verbose_name="producer_register", on_delete=models.SET_DEFAULT, db_column='producer_id')
    slug = models.SlugField(default=0)
    class Meta:
        db_table = 'webseries_label'
        ordering = ['-timestamp_field']


    def __str__(self):
        return self.webseries_name

   
class ProducerManager(models.Manager):
    def create_producer(self, producer_first_name, producer_email, producer_password):
        producer = self.create(
            producer_first_name=producer_first_name,
            producer_email=producer_email,
            producer_password=producer_password,
        )

        # Additional logic for creating the producer
        return producer



def get_data(self):
    time = datetime.now()
    if self.created_at.day == time.day:
        return str(time.hour - self.created_at.hour) + "hours ago"
    else:
        if self.created_at.month == time.month:
            return str(time.day - self.created_at.day) + "days ago"
        else:
            if self.created_at.year == time.year:
                return str(time.month - self.created_at.month) + "months ago"
    return self.created_at


    def __str__(self):
        return self.title


class Review(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    author = models.CharField(max_length=40, default="")
    review_date = models.DateField(max_length=100)
    stars = models.FloatField(null=True)
    comment = models.TextField(max_length=4000)
    Movie_name = models.CharField(max_length=100)
    timestamp_field = models.DateTimeField(auto_now_add=True)
    model_type = models.CharField(max_length=100, default='mydata1')
    like_count = models.BigIntegerField(null=True, blank=True, default='0')
    comment_count = models.BigIntegerField(null=True, blank=True, default='0')
    share_count = models.BigIntegerField(null=True, blank=True, default='0')
    source = models.CharField(max_length=100, null= True, blank=True)
    logo = models.CharField(max_length=255, null= True, blank=True, default='Users/blank_profile.webp')
    slug = models.SlugField(default=0)

    class Meta:
        ordering = ['-timestamp_field']
        db_table = 'review'


    def __str__(self):
        return '%s - %s - %s - %s - %s - %s - %s' % (self.Movie_name, self.comment, self.author, self.like_count, self.comment_count, self.share_count, self.stars)

class BoxOffice(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    Movie_name = models.CharField(max_length=100)
    production_house = models.CharField(max_length=100)
    movie_collections = models.DecimalField(null=True, max_digits=10, decimal_places=2)
    day_collections = models.DecimalField(null=True, max_digits=10, decimal_places=2)
    weekly_collections = models.DecimalField(null=True, max_digits=10, decimal_places=2)
    month_collections = models.DecimalField(null=True, max_digits=10, decimal_places=2)
    timestamp_field = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp_field']
        db_table = 'box_office'
    def __str__(self):
        return '%s - %s' % (self.Movie_name, self.movie_collections)


class News(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    Movie_name = models.CharField(max_length=100)
    text = models.CharField(max_length=5000)
    author = models.CharField(max_length=255)
    timestamp_field = models.DateTimeField(auto_now_add=True)
    auto_created = True,

    class Meta:
        db_table = 'news'
        ordering = ['timestamp_field']

    def __str__(self):
        return '%s - %s - %s' % (self.Movie_name, self.text, self.author)


class UserLogs(models.Model):
    id = models.BigAutoField(auto_created=True,primary_key=True, serialize=False, verbose_name='ID')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    login_time = models.DateTimeField(auto_now_add=True)
    logout_time = models.DateTimeField()

    class Meta:
        db_table = 'userlogs'
        ordering = ['id']

    def __str__(self):
        return self.user
    
    

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


## New Models
from podadmin.models import CreateLabel

class TopRatedMovies(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    movie_title = models.CharField(max_length=255)
    overview = models.TextField(max_length=1000)
    release_date = models.DateField(max_length=100, null=True)
    poster_path = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)
    genre = models.CharField(max_length=100, default=False, null=True)
    language = models.CharField(max_length=50, default=False, null=True)
    video = models.URLField(default=False, null=True)
    producer = models.CharField(max_length=100, default=False, null=True)
    director = models.CharField(max_length=100,  default=False, null=True)
    music_director = models.CharField(max_length=100, default=False, null=True)
    crew = models.CharField(max_length=100,  default=False, null=True)
    cast = models.CharField(max_length=2000, default=False, null=True)
    timestamp_field = models.DateTimeField(default=timezone.now)
    model_type = models.CharField(max_length=50, default='top_rated_movies')
    like_count = models.BigIntegerField(null=True, blank=True, default='0')
    follow_count = models.BigIntegerField(null=True, blank=True, default='0')
    share_count = models.BigIntegerField(null=True, blank=True, default='0')
    comment_count = models.BigIntegerField(null=True, blank=True, default='0')
    source = models.CharField(max_length=100, null= True, blank=True, default='TMDB/top_rated_movies')
    logo = models.CharField(max_length=100, null= True, blank=True, default='TMDB/TMDB_logo.png')
    slug = models.SlugField(default=False)

    class Meta:
        ordering = ['-timestamp_field']
        db_table = 'top_rated_movies'

    def __str__(self):
        return f"{self.movie_title}'s model"
    



class RecentMovies(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    movie_title = models.CharField(max_length=255)
    overview = models.TextField(max_length=1000)
    release_date = models.DateField(max_length=100, null=True)
    poster_path = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)
    genre = models.CharField(max_length=100, default=False, null=True)
    language = models.CharField(max_length=50, default=False, null=True)
    video = models.URLField(default=False, null=True)
    producer = models.CharField(max_length=100, default=False, null=True)
    director = models.CharField(max_length=100,  default=False, null=True)
    music_director = models.CharField(max_length=100, default=False, null=True)
    crew = models.CharField(max_length=100,  default=False, null=True)
    cast = models.CharField(max_length=2000, default=False, null=True)
    timestamp_field = models.DateTimeField(default=timezone.now)
    model_type = models.CharField(max_length=50, default='recent_movies')
    like_count = models.BigIntegerField(null=True, blank=True, default='0')
    follow_count = models.BigIntegerField(null=True, blank=True, default='0')
    share_count = models.BigIntegerField(null=True, blank=True, default='0')
    comment_count = models.BigIntegerField(null=True, blank=True, default='0')
    source = models.CharField(max_length=100, null= True, blank=True, default='TMDB/recent_movies')
    logo = models.CharField(max_length=100, null= True, blank=True, default='TMDB/TMDB_logo.png')
    slug = models.SlugField(default=False)

    class Meta:
        ordering = ['-timestamp_field']
        db_table = 'recent_movies'

    def __str__(self):
        return f"{self.movie_title}'s model"
    

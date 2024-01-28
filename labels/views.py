from django.shortcuts import render
from configparser import ConfigParser
from django.http import HttpResponse,Http404
from django.template import loader
import mysql.connector as sql
from django.views.generic import ListView, CreateView
from cinystoreapp.forms import *
import mysql.connector
from business.models import *
from django.db.models import Q
import requests
from itertools import chain
from operator import attrgetter
# from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_protect
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail
from cinystore import settings
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
#from django.utils.encoding import force_bytes, force_text
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm,SetPasswordForm
from django.contrib.auth import update_session_auth_hash
from django.http import JsonResponse
from io import BytesIO
from email.mime.image import MIMEImage
from django.db.models import Sum
from cinystoreapp.models import *
from podadmin.models import *
from cinystoreapp.decorators import user_only




db = mysql.connector.connect(
  host="3.109.48.139",
  user="myuser",
  password="cinystore",
  database="cinystore"
)
cursor = db.cursor()
# Create your views here.




@user_only
def Browsemovies(request):

    username = request.user.username
    # Retrieve a queryset of records with the desired username
    matching_records = UserInfo.objects.filter(username=username)
    # Check if any records with the desired username exist
    username_exists = matching_records.exists()

    if username_exists:
        userdata = UserInfo.objects.filter(username=username)
    else:
        userdata = User.objects.filter(username=username)

    ## user information storing ends here 
    template = loader.get_template('Browsemovies.html')
    class Browsemovies(ListView):
        Movie_name = ""
        synopsis = ""
        Production_house = ""
        Poster = ""

    mydata = CreateLabel.objects.all().order_by('-timestamp_field')

    movies = Movie.objects.all().order_by('-timestamp_field')
    context = {'mydata': mydata, 'movies': movies}
    Browsemovies = list(chain(mydata, movies))

    return render(request, 'Browsemovies.html', context)


def index(request):
    return render(request, 'Home.html')

   
def Home(request): 
    template = loader.get_template('Home.html')
    mydata = CreateLabel.objects.all().order_by('-timestamp_field')
    api_key = "9456c6fdcf8a04e157e45387ebf0c687"
    url = f"https://api.themoviedb.org/3/movie/popular?api_key={api_key}"
    response = requests.get(url)
    movies = response.json()["results"]
    movies = Movie.objects.all()
    mydata1 = Review.objects.all().values()
    mydata2 = BoxOffice.objects.all().values()

    context = {
        'mydata': mydata,
        'movies': movies,
        'mydata1': mydata1,
        'publictrailer': mydata,
        'genBox_office': mydata2,
    }
    return HttpResponse(template.render(context, request))

@user_only
def Labeltmdb(request, movie_title):
    mydata = Movie.objects.filter(movie_title=movie_title)
    template = loader.get_template('Labeltmdb.html')
    context = {
        'Labeltmdb': mydata,

    }
    return HttpResponse(template.render(context, request))


def Clipsview(request):
    mydata = Clips.objects.all().order_by('-timestamp_field')
    template = loader.get_template('Clipsview.html')
    context = {
        'Clipsview': mydata,

    }
    return HttpResponse(template.render(context, request))

@user_only
def Indianmovies(request):
    template = loader.get_template('Indianmovies.html')
    mydata = CreateLabel.objects.all().order_by('-timestamp_field')
    context = {
        'mydata': mydata,
        
    }
    return HttpResponse(template.render(context, request))

@user_only
def Internationalmovies(request):
    template = loader.get_template('Internationalmovies.html')
    mydata = Movie.objects.all().order_by('-timestamp_field')
    context = {
        'mydata': mydata,
        
    }
    return HttpResponse(template.render(context, request))

def Label2(request, movie_title):
    mydata = Movie.objects.filter(movie_title=movie_title)
    template = loader.get_template('Label2.html')
    context = {
        'Label2': mydata,

    }
    return HttpResponse(template.render(context, request))

@user_only
def review_label(request, Movie_name):
    mydata = Review.objects.filter(Movie_name=Movie_name)
    template = loader.get_template('review_label.html')
    context = {
        'review_label': mydata,
    }
    return HttpResponse(template.render(context, request))

@user_only
def userreview_label(request, Movie_name):
    mydata = Review.objects.filter(Movie_name=Movie_name)
    template = loader.get_template('userreview_label.html')
    context = {
        'userreview_label': mydata,
    }
    return HttpResponse(template.render(context, request))

@user_only
def Box_office_label(request, Movie_name):
    mydata = BoxOffice.objects.filter(Movie_name=Movie_name)
    template = loader.get_template('Box_office_label.html')
    context = {
        'Box_office_label': mydata,
    }
    return HttpResponse(template.render(context, request))


@user_only
def genBox_office(request):
    mydata = BoxOffice.objects.all()
    template = loader.get_template('genBox_office.html')
    context = {
        'genBox_office': mydata,
    }
    return HttpResponse(template.render(context, request))


@user_only
def web_createlabel(request):
    template = loader.get_template('web_createlabel.html')
    context = {
        'web_createlabel': web_createlabel
    }
    return HttpResponse(template.render(context, request))


@user_only
def web_createlabel1(request):
    template = loader.get_template('web_createlabel1.html')
    context = {
        'web_createlabel1': web_createlabel1
    }
    return HttpResponse(template.render(context, request))


def publiclabel(request, Movie_name):
    mydata = CreateLabel.objects.filter(Movie_name=Movie_name).order_by('-timestamp_field')
    mydata2 = PostText1.objects.filter(Movie_name=Movie_name).order_by('-timestamp_field')
    all_data = list(chain(mydata, mydata2))
    all_data.sort(key=attrgetter('timestamp_field'), reverse=True)
    template = loader.get_template('publiclabel.html')
    context = {
        'publiclabel': all_data,
        'mydata':mydata,
        'PostTextView':mydata2,
    }
    return HttpResponse(template.render(context, request))

def promo_tmdb(request, slug):
    mydata = Movie.objects.filter(slug=slug).order_by('-timestamp_field')
    template = loader.get_template('promo_tmdb.html')
    context = {
        'promo_tmdb': mydata,
    }
    return HttpResponse(template.render(context, request))

def promo_review(request, slug):
    mydata = Review.objects.all().order_by('-timestamp_field')
    mydata1 = Review.objects.filter(slug=slug).order_by('-timestamp_field')
    template = loader.get_template('promo_review.html')
    context = {
        'promo_review': mydata1,
        'mydata': mydata,
	'mydata1': mydata1,
    }
    return HttpResponse(template.render(context, request))

def promo_post(request, slug):
    mydata = CreateLabel.objects.filter(Url_name=slug).order_by('-timestamp_field')
    mydata2 = PostText1.objects.filter(slug=slug).order_by('-timestamp_field')
    template = loader.get_template('promo_post.html')
    context = {
        'promo_post':mydata2,
        'mydata': mydata,
        'mydata2': mydata2,
    }
    return HttpResponse(template.render(context, request))

def promo_label(request, Url_name):
    mydata = CreateLabel.objects.filter(Url_name=Url_name).order_by('-timestamp_field')
    mydata2 = PostText1.objects.filter(slug=Url_name).order_by('-timestamp_field')
    mydata1 = Review.objects.filter(slug=Url_name).order_by('-timestamp_field')
    mydata3 = CreateLabel.objects.all().order_by('-timestamp_field')
    all_data = list(chain(mydata, mydata2, mydata1, mydata3))
    all_data.sort(key=attrgetter('timestamp_field'), reverse=True)
    template = loader.get_template('promo_label.html')
    context = {
        'promo_label': all_data,
        'mydata':mydata,
        'mydata1':mydata1,
        'PostTextView':mydata2,
        'Createlabel':mydata3,
    }
    return HttpResponse(template.render(context, request))

def promo_clip(request, slug):
    mydata = CreateLabel.objects.filter(Url_name=slug).order_by('-timestamp_field')
    mydata2 = Clips.objects.filter(slug=slug).order_by('-timestamp_field')
    template = loader.get_template('promo_clip.html')
    context = {
        'promo_clip':mydata2,
        'mydata': mydata,
        'mydata2':mydata2,
    }
    return HttpResponse(template.render(context, request))

def publicfeed(request):
    mydata = CreateLabel.objects.all().order_by('-timestamp_field')
    mydata1 = Review.objects.all().order_by('-timestamp_field')
    movies = Movie.objects.all().order_by('-timestamp_field')
    mydata3 = PostText1.objects.all().order_by('-timestamp_field')
    mydata2 = Clips.objects.all().order_by('-timestamp_field')
    recent_movies = RecentMovies.objects.all().order_by('-timestamp_field')
    top_rated_movies = TopRatedMovies.objects.all().order_by('-timestamp_field')

    try:
        movies = Movie.objects.all().order_by('-timestamp_field')
    except Movie.DoesNotExist:
        movies = []
    try:
        mydata = CreateLabel.objects.all().order_by('-timestamp_field')
    except CreateLabel.DoesNotExist:
        mydata = []
    try:
        mydata1 = Review.objects.all().order_by('-timestamp_field')
    except Review.DoesNotExist:
        mydata1 = []
    try:
        mydata3 = PostText1.objects.all().order_by('-timestamp_field')
    except PostText1.DoesNotExist:
        mydata3 = []

    try:
        mydata2 = Clips.objects.all().order_by('-timestamp_field')
    except Clips.DoesNotExist:
        mydata2 = []
    try:
        recent_movies = RecentMovies.objects.all().order_by('-timestamp_field')
    except RecentMovies.DoesNotExist:
        recent_movies = []
    try:
        top_rated_movies = TopRatedMovies.objects.all().order_by('-timestamp_field')
    except TopRatedMovies.DoesNotExist:
        top_rated_movies = []

    Publicfeed = sorted(list(mydata) + list(movies) + list(mydata1) + list(mydata3) + list(mydata2) + list(recent_movies) + list(top_rated_movies),
                        key=lambda x: x.timestamp_field, reverse=True
                        )
    producerDetails = ProducerRegister.objects.all()

    context = {'Publicfeed': Publicfeed,'producerDetails':producerDetails}

    return render(request, 'publicfeed.html', context)

def userreviews(request):
    username = request.user.username
    matching_records = UserInfo.objects.filter(username=username)
    username_exists = matching_records.exists()

    if username_exists:
        userdata = UserInfo.objects.filter(username=username)
    else:
        userdata = User.objects.filter(username=username)

    mydata = Review.objects.all()
    template = loader.get_template('userreviews.html')
    context = {
        'userreviews': mydata,'head': userdata
    }
    return HttpResponse(template.render(context, request))
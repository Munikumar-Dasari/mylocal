from django.urls import path
from django.urls import path, include
from django.contrib import admin
from cinystoreapp import views 
from cinystoreapp.api_views import *
from . import views

app_name = 'labels'

urlpatterns = [
path('', views.index, name='index'),
path('Browsemovies/', views.Browsemovies, name='Browsemovies'),
path('Indianmovies/', views.Indianmovies, name='Indianmovies'),
path('Internationalmovies/', views.Internationalmovies, name='Internationalmovies'),
path('home/', views.Home, name='Home'),
path('promo_label/<str:Url_name>/', views.promo_label, name='promo_label'),
path('promo_post/<str:slug>/', views.promo_post, name='promo_post'), 
path('promo_review/<str:slug>/', views.promo_review, name='promo_review'),
path('promo_clip/<str:slug>/', views.promo_clip, name='promo_clip' ),
path('userreview_label/<str:Movie_name>/', views.userreview_label, name='userreview_label'),
path('review_label/<str:Movie_name>/', views.review_label, name='review_label'),
path('Box_office_label/<str:Movie_name>/', views.Box_office_label, name='Box_office_label'),
path('genBox_office/', views.genBox_office, name='genBox_office'),
path('web_createlabel/', views.web_createlabel, name='web_createlabel'),
path('Labeltmdb/<str:movie_title>/', views.Labeltmdb, name='Labeltmdb'),
path('Label2/<str:movie_title>/', views.Label2, name='Label2'),
path('publicfeed/', views.publicfeed, name='publicfeed'),
path('publiclabel/<str:Movie_name>',views.publiclabel, name='publiclabel'),
path('Clipsview/', views.Clipsview, name='Clipsview'),
path('userreviews/', views.userreviews, name='userreviews'),
]
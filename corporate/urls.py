from django.urls import path
from . import views

app_name = 'corporate'

urlpatterns =[
    path('', views.index, name='index'),
    path('creator/', views.creator, name='creator'),
    path('contact/', views.contact, name='contact'),
    path('FAQ/', views.faq, name='FAQ'),
    path('Privacy/', views.Privacy, name='Privacy'),
    path('reviews/',views.reviews, name='reviews'),
    path('terms/', views.terms, name='terms'),
    path('corporate/', views.corporate, name='corporate'),
    path('allblogs/', views.allblogs, name='allblogs'),
    path('Blog/<str:slug>/', views.blog, name='Blog'),
    ]
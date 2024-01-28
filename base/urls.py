from django.urls import path
from django.urls import path, include
from base import views


app_name = 'base'

urlpatterns = [
    path('', views.index, name='index'),
    path('corporate_base/', views.corporate_base, name='corporate_base'),
    path('admin_base/', views.admin_base, name='admin_base'),
    path('base/', views.base, name='base'),
    path('businessBase/', views.businessBase, name='businessBase'),
    path('corpbase/', views.corpbase, name='corpbase'),
    path('corporateBase/', views.corporateBase, name='corporateBase'),
    path('head/', views.head, name='head'),
    path('keepitshortbase/', views.keepitshortbase, name='keepitshortbase'),
    path('kis_team_base/', views.kis_team_base, name='kis_team_base'),
    path('market_base/', views.market_base, name='market_base'),
    path('market_base_login/', views.market_base_login, name='market_base_login'),
    path('PodBase/', views.PodBase, name='PodBase'),
    path('producer_base/', views.producer_base, name='producer_base'),
    path('producerhead/', views.producerhead, name='producerhead'),
    path('superadmin_base/', views.superadmin_base, name='superadmin_base'),

]
from django.urls import path
from . import views

app_name = 'marketing'


urlpatterns =[
    path('', views.index, name='index'),
    path('market_signup/', views.market_signup, name='market_signup'),
    path('market_login/', views.market_login, name='market_login'),
    path('marketing_dashboard/', views.marketing_dashboard, name='marketing_dashboard'),
    path('market_Logout/', views.market_Logout, name='market_Logout'),
    path('activate_marketing/<uid64>/<token>', views.activate_marketing, name='activate_marketing'),
    path('marketing_dashboard/', views.marketing_dashboard, name='marketing_dashboard'),
    path('blog_label/', views.blog_label, name='blog_label'),
    path('Privacy_form/', views.Privacy_form, name='Privacy_form'),
    path('Terms_form/', views.Terms_form, name='Terms_form'),
    path('Guidelines_form/', views.Guidelines_form, name='Guidelines_form'),
    path('Guidelines/', views.Guidelines, name='Guidelines'),
]
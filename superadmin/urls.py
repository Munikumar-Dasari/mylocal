from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('businessBase/', views.businessBase, name='businessBase'),
    path('corporateBase/', views.corporateBase, name='corporateBase'),
    path('superadmin_account/', views.superadmin_account, name='superadmin_account'),
    path('superadmin_add_clips/', views.superadmin_add_clips, name='superadmin_add_clips'),
    path('superadmin_add_post/', views.superadmin_add_post, name='superadmin_add_post'),
    path('superadmin_base/', views.superadmin_base, name='superadmin_base'),
    path('superadmin_content/', views.superadmin_content, name='superadmin_content'),
    path('superadmin_statistics/', views.superadmin_statistics, name='superadmin_statistics'),
    path('registerPage/', views.registerPage, name='registerPage'),
    path('login/', views.login, name='login'),
    # path('logout/', views.logout, name='logout'),
   
]
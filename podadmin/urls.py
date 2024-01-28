from django.urls import path
from . import views

app_name = 'podadmin'

urlpatterns = [
    path('', views.index, name='index'),
    path('businessBase/', views.businessBase, name='businessBase'),
    path('corporateBase/', views.corporateBase, name='corporateBase'),
    path('admin_account/', views.admin_account, name='admin_account'),
    path('approve_label/<str:Movie_name>/', views.approve_label, name = 'approve_label'),
    path('approve_post/<int:post_id>/', views.approve_post, name = 'approve_post'),
    path('approve_clips/<int:post_id>/', views.approve_clips, name = 'approve_clips'),
    path('reject_label/<str:Movie_name>/', views.reject_label, name = 'reject_label'),
    path('reject_post/<int:post_id>/', views.reject_post, name = 'reject_post'),
    path('reject_clips/<int:post_id>/', views.reject_clips, name = 'reject_clips'),
    path('admin_base/', views.admin_base, name='admin_base'),
    path('admin_content/<str:pod_name>/', views.admin_content, name='admin_content'),
    path('admin_statistics/<str:Movie_name>/', views.admin_statistics, name='admin_statistics'),
    path('register/', views.registerPage, name='registerPage'),
    path('login/', views.podlogin, name='podlogin'),
    path('activatePOD/<uid64>/<token>', views.activatePOD, name='activatePOD'),
    path('logout/', views.PODlogout, name='PODlogout'),
    path('reviewlabel/<str:Movie_name>/', views.reviewlabel, name='reviewlabel'),
    path('podadmin_change_password/', views.podadmin_change_password, name='podadmin_change_password'),

   
]
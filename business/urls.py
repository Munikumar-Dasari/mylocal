from django.urls import path
from . import views 


app_name = 'business'

urlpatterns = [
    path('', views.index, name='index'),
    path('welcomePage/', views.welcome_page, name='welcomePage'),
    path('businessBase/', views.businessBase, name='businessBase'),
    path('corporateBase/', views.corporateBase, name='corporateBase'),
    path('otppage/', views.otp_page, name='otppage'),
    path('producer_account/', views.producer_account, name='producer_account'),
    path('producer_change_password/', views.producer_change_password, name='producer_change_password'),
    path('producer_add_clips/<str:Movie_name>/', views.producer_add_clips, name='producer_add_clips'),
    path('producer_add_post/<str:Movie_name>/', views.producer_add_post, name='producer_add_post'),
    path('producer_base/', views.producer_base, name='producer_base'),
    path('producer_content/<str:production_house>/', views.producer_content, name='producer_content'),
    path('producer_content/<str:production_house>/<str:Movie_name>/', views.producer_content_with_movie, name='producer_content'),
    path('producer_submitlabel/', views.producer_submitlabel, name='producer_submitlabel'),
    path('check_movie_exists/', views.check_movie_exists, name='check_movie_exists'),
    path('producer_statistics/<str:Movie_name>/', views.producer_statistics, name='producer_statistics'),
    path('Register/', views.Registerpage, name='Registerpage'),
    path('producer_check_username/', views.producer_check_username, name='producer_check_username'),
    path('producer_check_email/', views.producer_check_email, name='producer_check_email'),
    path('producerlogin/', views.producerlogin, name='producerlogin'),
    path('activateaccount/<uid64>/<token>', views.activateaccount, name='activateaccount'),
    path('segment/', views.segment, name='segment'),
    path('edit_producer_account/', views.edit_producer_account, name='edit_producer_account'),
    path('logout/', views.Producerlogout, name='Producerlogout'),
    path('business/', views.business, name="business"),
    path('edit_label/<str:Movie_name>/', views.edit_label, name='edit_label'),
    path('edit_post/<int:id>/', views.edit_post, name='edit_post'),
    path('edit_clip/<int:id>/', views.edit_clip, name='edit_clip'),
    path('delete_label/<str:Movie_name>/', views.delete_label, name='delete_label'),
    path('delete_post/<str:post_id>/', views.delete_post, name='delete_post'),
    path('delete_clip/<str:clip_id>/', views.delete_clip, name='delete_clip'),
    path('webseries_label/', views.webseries_label, name='webseries_label'),

    # path('verify_otp/', views.verify_otp, name='verify_otp'),
]
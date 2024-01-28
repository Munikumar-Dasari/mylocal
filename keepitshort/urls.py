from django.urls import path
from django.urls import path, include
from keepitshort import views


app_name = 'keepitshort'

urlpatterns = [
    path('', views.index, name='index'),
    path('keepitshort/', views.keepitshort, name='keepitshort'),
    path('keepitshortbase/', views.keepitshortbase, name='keepitshortbase'),
    path('kis_team_account/', views.kis_team_account, name='kis_team_account'),
    path('kis_team_login/', views.kis_team_login, name='kis_team_login'),   
    path('kis_team_dashboard/', views.kis_team_dashboard, name='kis_team_dashboard'),
    path('kis_team_Logout/', views.kis_team_Logout, name='kis_team_Logout'),    
    path('activate_kis_team/<uid64>/<token>', views.activate_kis_team, name='activate_kis_team'),
    path('kis_team_register/', views.kis_team_register, name='kis_team_register'),
    path('kis_team_reset_password/', views.kis_team_reset_password, name='kis_team_reset_password'),
    path('kis_team_reset_confirm/<uid64>/<token>/', views.kis_team_reset_confirm, name='kis_team_reset_confirm'),
    path('kis_team_change_password/', views.kis_team_change_password, name='kis_team_change_password'),
    path('kis_team_profile/', views.kis_team_profile, name='kis_team_profile'),
    path('kis_team_update_profile/', views.kis_team_update_profile, name='kis_team_update_profile'),
    path('kis_team_content/', views.kis_team_content, name='kis_team_content'),
    path('kis_team_statistics/', views.kis_team_statistics, name='kis_team_statistics'),
    path('kis_team_submitlabel/', views.kis_team_submitlabel, name='kis_team_submitlabel'),
    path('kis_institute_register/', views.kis_institute_register, name='kis_institute_register'),
    path('kis_institute_login/', views.kis_institute_login, name='kis_institute_login'),
    path('kis_institute_details/', views.kis_institute_details, name='kis_institute_details'),
    path('kis_team_dashboard/', views.kis_team_dashboard, name='kis_team_dashboard'),
    path('kis_create_team/', views.kis_create_team, name='kis_create_team'),

]
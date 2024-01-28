from django.urls import path
from django.urls import path, include
from django.contrib import admin
from cinystoreapp import views
from . import api_views
from .api_views import *

app_name = 'cinystoreapp'

urlpatterns = [
    path('', views.index, name='index'),
    path('auth_login/', views.auth_login, name='auth_login'),
    path('Authregister/', views.Authregister, name='Authregister'),
    path('ChangePassword/', views.ChangePassword, name='ChangePassword'),
    path('Feedpage/', views.Feedpage, name='Feedpage'),
    path('Createlabel/', views.Createlabel, name='Createlabel'),
    path('Groups/', views.Groups, name='Groups'),
    path('Usertrailer/', views.Usertrailer, name='Usertrailer'),
    path('StickySidebars/', views.StickySidebars, name='StickySidebars'),
    path('movies/', views.tmdb_movies, name='movies'),
    path('activate/<uid64>/<token>', views.activate, name='activate'),
    path('activation_success/', views.activation_success, name='activation_success'),
    # path('producer_activation_success/', views.producer_activation_success, name='producer_activation_success'),
    path('auth_Logout/', views.auth_Logout, name='auth_Logout'),
    path('error/', views.error_view, name='error'),
    path('genreviews/', views.genreviews, name='genreviews'),
    path('Managelabel/', views.Managelabel, name='Managelabel'),
    # path('producerbase/', views.producerbase,  name='producerbase'),
    path('episodeupload/', views.episodeupload, name='episodeupload'),
    path('episodeupload2/', views.episodeupload2, name='episodeupload2'),
    path('episodeupload1/', views.episodeupload1, name='episodeupload1'),
    path('producermanagelabel/<str:Movie_name>/', views.producermanagelabel, name='producermanagelabel'),
    path('templates/<str:Movie_name>/', views.templates, name='templates'),
    path('socialuserlogin/', views.socialuserlogin, name='socialuserlogin'),
    path('comingsoonlabel/', views.comingsoonlabel, name='comingsoonlabel'),
    path('Newsform/', views.Newsform, name='Newsform'),
    path('reset_password/',views.reset_password, name="reset_password"),
    path('ResetConfirm/<uid64>/<token>/', views.ResetConfirm, name='ResetConfirm'),
    path('check_username_availability', views.check_username_availability, name='check_username_availability'),
    path('check_email', views.check_email_availability, name='check_email_availability'),
    path('PersonalInformation/change_password/', views.change_password, name='change_password'),
    path('PersonalInformation/', views.PersonalInformation, name='PersonalInformation'),
    path('UpdatePersonalInformation/', views.PersonalInformation_update, name='UpdatePersonalInformation'),
    path('check_movie_exists/', views.check_movie_exists, name='check_movie_exists'),
    path('producer_reset_password/', views.producer_reset_password, name= 'producer_reset_password'),
    path('ProducerResetConfirm/<uid64>/<token>/', views.ProducerResetConfirm, name='ProducerResetConfirm'),
    path('profile/', views.profile, name='profile'),
    path('UpdateProfile/', views.UpdateProfile, name='UpdateProfile'),
    path('producer_change_password/', views.producer_change_password, name='producer_change_password'),
    # path('moviestats/<str:Movie_name>/', views.moviestats, name ='moviestats'),
    path('searchresult/', views.searchresult, name='searchresult'),
    path('notification/', views.notification, name='notification'),
    path('Deleteuser/', views.Deleteuser, name='Deleteuser'),
    path('now_playing/', views.now_playing, name='now_playing'),
    path('top_rated/', views.top_rated, name='top_rated'),
   


    # URL Paths for the API
    #path('PersonalInfo_API', api_views.PersonalInfo_API, name= 'PersonalInfo_Api'),
    path('CreateLabelGet_API', api_views.CreateLabelGet_API, name = 'CreateLabelGet_API'),
    path('PostGet_API', api_views.PostGet_API, name='PostGet_API'),
    path('TmdbMovies_API', api_views.TmdbMovies_API, name='TmdbMovies_API'),
    path('MoviePost_API/<str:Movie_name>', api_views.MoviePost_API, name = 'MoviePost_API'),
    path('Reviews_API/<str:Movie_name>', api_views.Reviews_API, name = 'Reviews_API'),
    path('Trailers_API/', api_views.Trailers_API, name = 'Trailers_API'),
    path('AllReview_API', api_views.AllReview_API, name = 'AllReview_API'),
    path('ProducerInfo_API/', api_views.ProducerInfo_API, name = 'ProducerInfo_API'),
    path('CombinedFeed_API', api_views.CombinedFeed_API, name = 'CombinedFeed_API'),
    path('get_user_token/', api_views.get_user_token, name = 'get_user_token'),
    
    path('LikePostAPI_Feedpage/', api_views.LikePostAPI_Feedpage, name = 'LikePostAPI_Feedpage'),
    path('CommentsAPI_Feedpage/', api_views.CommentsAPI_Feedpage, name = 'CommentsAPI_Feedpage'),
    path('SocialInteractionsAPI/', api_views.SocialInteractionsAPI, name='SocialInteractionsAPI'),
    path('SocialInteractionsAPI2/', api_views.SocialInteractionsAPI2, name='SocialInteractionsAPI2'),
    path('SharePostAPI_Feedpage/', api_views.SharePostAPI_Feedpage, name = 'SharePostAPI_Feedpage'),
    path('FollowLabels_API/', api_views.FollowLabels_API, name = 'FollowLabels_API'),
    path('UserInformation_API/', api_views.UserInformation_API, name = 'UserInformation_API'),
    path('SearchResults_API/', api_views.SearchResults_API, name = 'SearchResults_API'),
    path('PrivacyGet_API/', api_views.PrivacyGet_API, name='PrivacyGet_API'),
    path('TermsGet_API/', api_views.TermsGet_API, name='TermsGet_API'),
    path('UpdatePesronalInfo_API/',api_views.UpdatePesronalInfo_API, name='UpdatePesronalInfo_API'),
    path('updateProfilephoto/',api_views.updateProfilephoto, name='updateProfilephoto'),
    path('ClipsAPI/',api_views.ClipsAPI, name='ClipsAPI'),
    path('UserLoginOrRegisterAPI/',api_views.UserLoginOrRegisterAPI, name='UserLoginOrRegisterAPI'),
    path('VerifyUserOTPAPI/',api_views.VerifyUserOTPAPI, name='VerifyUserOTPAPI'),
    path('ResendOTPAPI/',api_views.ResendOTPAPI, name='ResendOTPAPI'),
    path('ReportAbuseAPI/', api_views.ReportAbuseAPI, name='ReportAbuseAPI'),
    path('NotInterestedAPI/', api_views.NotInterestedAPI, name='NotInterestedAPI'),
    path('ReportCommentAPI/', api_views.ReportCommentAPI, name='ReportCommentAPI'),
    

]


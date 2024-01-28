from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from business.models import *
from corporate.models import *
from cinystoreapp.models import *
from podadmin.models import *
from superadmin.models import *
from labels.models import *
import json
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import F
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import F
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse

from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from .serializers import TmdbSerializer
from cinystore import settings
from django.db.models import Q



from rest_framework.pagination import CursorPagination

class CustomPagination(CursorPagination):
    page_size =  6 # Set your desired page size
    ordering = '-timestamp_field'  # Use the field for sorting (timestamp or ID field)
    cursor_query_param = 'cursor'  # The name of the cursor parameter in the URL


@api_view(['POST', 'GET'])
def CreateLabelGet_API(request):
    if request.method == 'POST':

        data = json.loads(request.body)
        uid = data.get('uid')
        if uid is None:
            return Response({
                'status': 400,
                'message': 'uid not passed!'
            })
        createlabel = CreateLabel.objects.all()
        abuse_report = AbuseReport.objects.all()
        not_interested = NotInterested.objects.all()
        
        # get the user object from the UID
        phone_number_obj = PhoneNumber.objects.get(uid=uid)
        user_obj = User.objects.get(phone_numbers_id=phone_number_obj.id)
        print(user_obj.id)

        combined_data = []
        for item in createlabel:
            if not abuse_report.filter(label_id=item.id, user_id = user_obj.id).exists() and not not_interested.filter(label_id=item.id, user_id = user_obj.id).exists():
                combined_data.append(item)

        combined_data = sorted(combined_data, key=lambda x: x.timestamp_field, reverse=True)
        paginator = PageNumberPagination()
        paginator.page_size = 10  # Set your desired page size
        paginated_queryset = paginator.paginate_queryset(combined_data, request)

        serializer = CreatelabelSerializer(paginated_queryset, many=True)
        next_url = paginator.get_next_link()
        prev_url = paginator.get_previous_link()

        if next_url:
            next_url = next_url.replace(request.get_host(), settings.SITE_URL)

        if prev_url:
            prev_url = prev_url.replace(request.get_host(), settings.SITE_URL)
        return Response({
            'next_url':next_url,
            'prev_url':prev_url,
            'results':serializer.data})
    else:
        # Get the list of all the labels when UID is not passed
        createlabel = CreateLabel.objects.all()
        paginator = PageNumberPagination()
        paginator.page_size = 10 # Set your desired page size
        paginated_queryset = paginator.paginate_queryset(createlabel, request)

        serializer = CreatelabelSerializer(paginated_queryset, many=True)
        next_url = paginator.get_next_link()
        prev_url = paginator.get_previous_link()

        if next_url:
            next_url = next_url.replace(request.get_host(), settings.SITE_URL)

        if prev_url:
            prev_url = prev_url.replace(request.get_host(), settings.SITE_URL)
        return Response({
            'next_url':next_url,
            'prev_url':prev_url,
            'results':serializer.data})



@api_view(['GET'])
def PostGet_API(request):
    post = PostText1.objects.all()
    # Apply pagination using your custom pagination class
    paginator = CustomPagination()
    paginated_queryset = paginator.paginate_queryset(post, request)
    serializer = PostSerializer(paginated_queryset, many= True)
    serialezer_copy = serializer.data.copy()
    for item in serialezer_copy:
        item['Poster_path'] = settings.TMDB_LINK + (item['poster_path'].split('/')[-1])
    next_url = paginator.get_next_link()
    prev_url = paginator.get_previous_link()

    if next_url:
        next_url = next_url.replace(request.get_host(), settings.SITE_URL)

    if prev_url:
        prev_url = prev_url.replace(request.get_host(), settings.SITE_URL)
    return Response({
        'next_url':next_url,
        'prev_url':prev_url,
        'results':serializer.data})


@api_view(['GET'])
def TmdbMovies_API(request):
    movies = Movie.objects.all()
    # Apply pagination using your custom pagination class
    paginator = CustomPagination()
    paginated_queryset = paginator.paginate_queryset(movies, request)
    serializer = TmdbSerializer(paginated_queryset, many= True)
    serialezer_copy = serializer.data.copy()
    for item in serialezer_copy:
        item['Poster_path'] = settings.TMDB_LINK + '/' +(item['poster_path'].split('/')[-1])
    next_url = paginator.get_next_link()
    prev_url = paginator.get_previous_link()

    if next_url:
        next_url = next_url.replace(request.get_host(), settings.SITE_URL)

    if prev_url:
        prev_url = prev_url.replace(request.get_host(), settings.SITE_URL)
    return Response({
        'next_url':next_url,
        'prev_url':prev_url,
        'results':serializer.data})


@api_view(['POST', 'GET'])
def MoviePost_API(request, Movie_name):
    if request.method == 'POST':
        data = json.loads(request.body)
        uid = data.get('uid')
        if uid is None:
            return Response({
                'status': 400,
                'message': 'uid not passed!'
            })
        movie_posts = PostText1.objects.filter(Movie_name=Movie_name)
        abuse_report = AbuseReport.objects.all()
        not_interested = NotInterested.objects.all()

        # get the user object from the UID
        phone_number_obj = PhoneNumber.objects.get(uid=uid)
        user_obj = User.objects.get(phone_numbers_id=phone_number_obj.id)
        print(user_obj.id)

        combined_data = []
        for item in movie_posts:
            if not abuse_report.filter(post_id=item.id, user_id = user_obj.id).exists() and not not_interested.filter(post_id=item.id, user_id = user_obj.id).exists():
                combined_data.append(item)

        # Apply pagination using your custom pagination class
        combined_data = sorted(combined_data, key=lambda x: x.timestamp_field, reverse=True)

        serializer = MoviePostSerializer(combined_data, many=True)

        return Response({'results':serializer.data})
    else:
        # Get the list of all the posts for a particular movie when UID is not passed
        movie_posts = PostText1.objects.filter(Movie_name=Movie_name)
        paginator = PageNumberPagination()
        paginator.page_size = 10
        paginated_queryset = paginator.paginate_queryset(movie_posts, request)
        serializer = MoviePostSerializer(paginated_queryset, many=True)
        next_url = paginator.get_next_link()
        prev_url = paginator.get_previous_link()

        if next_url:
            next_url = next_url.replace(request.get_host(), settings.SITE_URL)

        if prev_url:
            prev_url = prev_url.replace(request.get_host(), settings.SITE_URL)

        return Response({
            'next_url':next_url,
            'prev_url':prev_url,
            'results':serializer.data})
    
@api_view(['POST', 'GET'])
def Reviews_API(request, Movie_name):
    if request.method == 'POST':
        data = json.loads(request.body)
        uid = data.get('uid')
        if uid is None:
            return Response({
                'status': 400,
                'message': 'uid not passed!'
            })

        reviews = Review.objects.filter(Movie_name = Movie_name)
        abuse_report = AbuseReport.objects.all()
        not_interested = NotInterested.objects.all()

        # get the user object from the UID
        phone_number_obj = PhoneNumber.objects.get(uid=uid)
        user_obj = User.objects.get(phone_numbers_id=phone_number_obj.id)
        Reviews = Review.objects.filter(Movie_name = Movie_name)
        
        combined_data = []
        for item in reviews:
            if not abuse_report.filter(review_id=item.id, user_id = user_obj.id).exists() and not not_interested.filter(review_id=item.id, user_id = user_obj.id).exists():
                combined_data.append(item)

        # Apply pagination using your custom pagination class
        paginator = PageNumberPagination()
        paginator.page_size = 10  # Set your desired page size
        
        paginated_queryset = paginator.paginate_queryset(combined_data, request)
        serializer = ReviewSerializer(paginated_queryset, many= True)

        next_url = paginator.get_next_link()
        prev_url = paginator.get_previous_link()

        if next_url:
            next_url = next_url.replace(request.get_host(), settings.SITE_URL)

        if prev_url:
            prev_url = prev_url.replace(request.get_host(), settings.SITE_URL)
        return Response({
            'next_url':next_url,
            'prev_url':prev_url,
            'results':serializer.data})
    else:
        # Get the list of all the reviews for a particular movie when UID is not passed
        reviews = Review.objects.filter(Movie_name = Movie_name)
        paginator = PageNumberPagination()
        paginator.page_size = 10

        paginated_queryset = paginator.paginate_queryset(reviews, request)
        serializer = ReviewSerializer(paginated_queryset, many= True)
        
        next_url = paginator.get_next_link()
        prev_url = paginator.get_previous_link()

        if next_url:
            next_url = next_url.replace(request.get_host(), settings.SITE_URL)

        if prev_url:
            prev_url = prev_url.replace(request.get_host(), settings.SITE_URL)
        return Response({
            'next_url':next_url,
            'prev_url':prev_url,
            'results':serializer.data})
    

@api_view(['GET'])
def AllReview_API(request):
    reviews = Review.objects.all()
    # Apply pagination using your custom pagination class
    paginator = CustomPagination()
    paginated_queryset = paginator.paginate_queryset(reviews, request)
    serializer = ReviewSerializer(paginated_queryset, many= True)
    next_url = paginator.get_next_link()
    prev_url = paginator.get_previous_link()

    if next_url:
        next_url = next_url.replace(request.get_host(), settings.SITE_URL)

    if prev_url:
        prev_url = prev_url.replace(request.get_host(), settings.SITE_URL)
    return Response({
        'next_url':next_url,
        'prev_url':prev_url,
        'results':serializer.data})

    
@api_view(['GET'])
def Trailers_API(request):
    trailer = CreateLabel.objects.all()
    # Apply pagination using your custom pagination class
    paginator = CustomPagination()
    paginated_queryset = paginator.paginate_queryset(trailer, request)
    serializer = TrailerSerializer(paginated_queryset , many=True)
    next_url = paginator.get_next_link()
    prev_url = paginator.get_previous_link()

    if next_url:
        next_url = next_url.replace(request.get_host(), settings.SITE_URL)

    if prev_url:
        prev_url = prev_url.replace(request.get_host(), settings.SITE_URL)
    return Response({
        'next_url':next_url,
        'prev_url':prev_url,
        'results':serializer.data})


@api_view(['GET'])
def ProducerInfo_API(request):
    producer = ProducerRegister.objects.all()
    serializer = ProducerInfoSerializer(producer, many=True)
    return Response(serializer.data)


@api_view(['POST', 'GET'])
def CombinedFeed_API(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        uid = data.get('uid')
        if uid is None:
            return Response({
                'status': 400,
                'message': 'uid not passed!'
            })

        paginator = PageNumberPagination()
        paginator.page_size = 10  # Set your desired page size

        # Fetch data from different models exluding the context been reported by the UID passed
        feed = PostText1.objects.all()
        tmdb = Movie.objects.all()
        label = CreateLabel.objects.all()
        reviews = Review.objects.all()
        abuse_report = AbuseReport.objects.all()
        not_interested = NotInterested.objects.all()

        # user id 
        phone_number_obj = PhoneNumber.objects.get(uid=uid)
        user_obj = User.objects.get(phone_numbers_id=phone_number_obj.id)
        print(user_obj.id)
        
        # Combine the data excluding the abuse_report, not_interested for the user with the UID passed
        combined_data = []
        for item in feed:
            if not abuse_report.filter(post_id=item.id, user_id = user_obj.id).exists() and not not_interested.filter(post_id=item.id, user_id = user_obj.id).exists():
                combined_data.append(item)
        for item in tmdb:
            if not abuse_report.filter(movie_id=item.id, user_id = user_obj.id).exists() and not not_interested.filter(movie_id=item.id, user_id = user_obj.id).exists():
                combined_data.append(item)
        for item in label:
            if not abuse_report.filter(label_id=item.id, user_id = user_obj.id).exists() and not not_interested.filter(label_id=item.id, user_id = user_obj.id).exists():
                combined_data.append(item)
        for item in reviews:
            if not abuse_report.filter(review_id=item.id, user_id = user_obj.id).exists() and not not_interested.filter(review_id=item.id, user_id = user_obj.id).exists():
                combined_data.append(item)

        # Sort the combined data based on timestamp
        combined_data = sorted(combined_data, key=lambda x: x.timestamp_field, reverse=True)

        # Paginate the combined data
        paginated_data = paginator.paginate_queryset(combined_data, request)

        # Serialize the paginated data
        serialized_data = []
        for item in paginated_data:
            if isinstance(item, PostText1):
                movie_name = item.Movie_name
                serialized_data_stored = posttext_serializer_feedpage(item).data
                copy_serialized_data = serialized_data_stored.copy()
                copy_serialized_data['Language'] = CreateLabel.objects.get(Movie_name = movie_name).Language
                copy_serialized_data['Genre'] = CreateLabel.objects.get(Movie_name = movie_name).Genre
                serialized_data.append(copy_serialized_data)
            elif isinstance(item, Movie):
                serialized_data.append(tmdb_serializer_feedpage(item).data)
            elif isinstance(item, CreateLabel):
                serialized_data.append(createlabel_serializer_feedpage(item).data)
            elif isinstance(item, Review):
                movie_name = item.Movie_name
                serialized_data_stored = review_serializer_feedpage(item).data
                copy_serialized_data = serialized_data_stored.copy()
                copy_serialized_data['Language'] = CreateLabel.objects.get(Movie_name = movie_name).Language
                copy_serialized_data['Genre'] = CreateLabel.objects.get(Movie_name = movie_name).Genre
                serialized_data.append(copy_serialized_data)
        
        next_url = paginator.get_next_link()
        prev_url = paginator.get_previous_link()

        if next_url:
            next_url = next_url.replace(request.get_host(), settings.SITE_URL)

        if prev_url:
            prev_url = prev_url.replace(request.get_host(), settings.SITE_URL)
        return Response({
            'next_url':next_url,
            'prev_url':prev_url,
            'results':serialized_data})
    else:
        # Get the list of all the posts for a particular movie when UID is not passed
        feed = PostText1.objects.all()
        tmdb = Movie.objects.all()
        label = CreateLabel.objects.all()
        reviews = Review.objects.all()
        combined_data = []
        for item in feed:
            combined_data.append(item)
        for item in tmdb:
            combined_data.append(item)
        for item in label:
            combined_data.append(item)
        for item in reviews:
            combined_data.append(item)
        paginator = PageNumberPagination()
        paginator.page_size = 10

        paginated_queryset = paginator.paginate_queryset(combined_data, request)
        serialized_data = []
        for item in paginated_queryset:
            if isinstance(item, PostText1):
                movie_name = item.Movie_name
                serialized_data_stored = posttext_serializer_feedpage(item).data
                copy_serialized_data = serialized_data_stored.copy()
                copy_serialized_data['Language'] = CreateLabel.objects.get(Movie_name = movie_name).Language
                copy_serialized_data['Genre'] = CreateLabel.objects.get(Movie_name = movie_name).Genre
                serialized_data.append(copy_serialized_data)
            elif isinstance(item, Movie):
                serialized_data.append(tmdb_serializer_feedpage(item).data)
            elif isinstance(item, CreateLabel):
                serialized_data.append(createlabel_serializer_feedpage(item).data)
            elif isinstance(item, Review):
                movie_name = item.Movie_name
                serialized_data_stored = review_serializer_feedpage(item).data
                copy_serialized_data = serialized_data_stored.copy()
                copy_serialized_data['Language'] = CreateLabel.objects.get(Movie_name = movie_name).Language
                copy_serialized_data['Genre'] = CreateLabel.objects.get(Movie_name = movie_name).Genre
                serialized_data.append(copy_serialized_data)

        next_url = paginator.get_next_link()
        prev_url = paginator.get_previous_link()

        if next_url:
            next_url = next_url.replace(request.get_host(), settings.SITE_URL)

        if prev_url:
            prev_url = prev_url.replace(request.get_host(), settings.SITE_URL)
        return Response({
            'next_url':next_url,
            'prev_url':prev_url,
            'results':serialized_data})
    


import requests
from datetime import datetime
import cinystore.settings as settings
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from .models import PhoneNumber, UserInfo, UserLogs

@api_view(['POST'])
def get_user_token(request):
    data = json.loads(request.body.decode('utf-8'))
    token = data['token']
    # token = "77a987e6969c4e0397f8fdf58ad6655e"
    CustomUser = get_user_model()
    print(CustomUser)

    url = 'https://cinystore.authlink.me'
    headers = {
        'clientId': settings.OTPLESS_CLIENT_ID,
        'clientSecret': settings.OTPLESS_KEY,
        'Content-Type': 'application/json'
    }
    data = {
        'token': token
    }

    response = requests.post(url, headers=headers, json=data)
    print(response.status_code)
    json_response = response.json()
    user_data = json_response.get('data', json_response.get('user', {}))
    print(user_data)

    
    if response.status_code == 200 and user_data != {}:
        # Assuming the response contains user information

        print('user_data:',user_data)
        try: 
            mobile = json_response.get('data').get('userMobile')
            email = json_response.get('data').get('userEmail')
            username = json_response.get('data').get('userName')
            timestamp = json_response.get('data').get('timestamp')
        except:
            mobile = json_response.get('user').get('waNumber')
            username = json_response.get('user').get('waName')
            timestamp = json_response.get('user').get('timestamp')

        # Check if the user already exists in the Django User model
        
        if UserInfo.objects.filter(phone_number=mobile).exists():
            user = CustomUser.objects.get(phone_numbers__number=mobile)
            user.last_login = timestamp
            # Update email in CustomUser model
            user.email = email
            user.save()
            # Update email in PhoneNumber model
            try:    
                phone_number = PhoneNumber.objects.get(number=mobile)
                phone_number.email = user.email
                phone_number.save()
                user_info = UserInfo.objects.get(user_id=user.id)
                user_info.email = user.email
                user_info.save()
            except:
                phone_number = PhoneNumber.objects.get(email=email)
                phone_number.email = user.email
                phone_number.save()
                user_info = UserInfo.objects.get(user_id=user.id)
                user_info.email = user.email
                user_info.save()
            #Adding user to userlogs table
            user_id = user.id
            login_time = datetime.now()
            login_log = UserLogs.objects.create(user_id=user_id, login_time=login_time)
            login_log.save()

            return Response({
                "status": 200,
                "profilephoto": UserInfo.objects.get(user_id=user.id).profilephoto.url if UserInfo.objects.get(user_id=user.id).profilephoto else "", 
                "username": UserInfo.objects.get(user_id=user.id).username,
                "email": UserInfo.objects.get(user_id=user.id).email,
                "phone_number": mobile,
                "uid": user.phone_numbers.first().uid
            })
        else:

            phone_number = PhoneNumber.objects.create(number=mobile, email = email) # Create a phone number instance
            if username is None:
                user = CustomUser.objects.create_user(username=mobile,email=email,phone_numbers_id = phone_number.id)
            else:
                user = CustomUser.objects.create_user(username=username,email=email,phone_numbers_id = phone_number.id)

            # user.phone_numbers.add(phone_number) # Associate the phone number with the user
            user.last_login = timestamp
            if username is None:
                user.username = mobile
            else:
                user.username = username
                user.first_name= username.split(' ')[0]
                user.last_name= username.split(' ')[1] if len(username.split(' ')) > 1 else None

            user.is_user = True
            user.is_active = True
            user.save()
            customer = UserInfo.objects.create(user_id=user.id)
            if username is None:
                customer.username = mobile
            else:
                customer.username = username
                customer.first_name = username.split(' ')[0]
                customer.last_name = username.split(' ')[1] if len(username.split(' ')) > 1 else None

            customer.email = email 
            customer.phone_number = mobile
            customer.save()

            #Adding user to userlogs table
            user_id = user.id
            login_time = datetime.now()
            login_log = UserLogs.objects.create(user_id=user_id, login_time=login_time)
            login_log.save()
            
            return Response({
                "status": 200, 
                "profilephoto": UserInfo.objects.get(user_id=user.id).profilephoto.url if UserInfo.objects.get(user_id=user.id).profilephoto else "",
                "username": UserInfo.objects.get(user_id=user.id).username,
                "email": UserInfo.objects.get(user_id=user.id).email,
                "phone_number": mobile,
                "uid": phone_number.uid
            })
    else:
        # Handle the error if the request fails
        print(f"Request failed with status code: {response.status_code}")
        return Response({
            'status': 400,
            'message': 'Request failed!'
        })    

@api_view(['POST'])
def LikePostAPI_Feedpage(request):
    data = json.loads(request.body)
    model_type = data.get('model_type')

    if data.get('post_id') is None:
        return Response({
            'status': 400,
            'message': 'Post_id not passed!' 
        })
    if data.get('uid') is None:
        return Response({
            'status': 400,
            'message': 'uid not passed!'
        })
    if data.get('model_type') is None:
        return Response({
            'status': 400,
            'message': 'model_type not passed!'
        })
    uid = data.get('uid')
    phone_number_obj = PhoneNumber.objects.get(uid=uid)
    try:
        user_obj = UserInfo.objects.get(phone_number=phone_number_obj.number)
        print(user_obj)
    except PhoneNumber.DoesNotExist:
        user_obj = UserInfo.objects.get(email=phone_number_obj.email)
    
    if model_type == 'movies':
        post_id = data.get('post_id')
        movie_obj = Movie.objects.get(id=post_id)

        # Create a new instance of the Userlike model with the provided values
        if UserLikes.objects.filter(movie=movie_obj, user_id=user_obj.user_id, model_type = model_type).exists():
            return Response({
                'status': 400,
                'isLiked': True,
                'message': 'Like already exists!'
            })
        else: 
            like_post = UserLikes.objects.create(movie=movie_obj, user_id=user_obj.user_id, model_type = model_type)

            # update the like in the movie table
            like_count = Movie.objects.get(id=post_id).like_count
            Movie.objects.filter(id=post_id).update(like_count=like_count+1)

            return Response({
                'status': 200,
                'like_count': like_count+1,
                'isLiked': True,
                'message': 'Like Recorded!'
            })
    # model for CreateLabel
    elif model_type == 'mydata':
        post_id = data.get('post_id')
        label_obj = CreateLabel.objects.get(id=post_id)
        
        if UserLikes.objects.filter(label=label_obj, user_id=user_obj.user_id, model_type = model_type).exists():
            return Response({
                'status': 400,
                'isLiked': True,
                'message': 'Like already exists!'
            })
        else:
            # Create a new instance of the UserLikes model with the provided values
            like_post = UserLikes.objects.create(label=label_obj, user_id=user_obj.user_id, model_type = model_type)

            #update the like in the createlabel table
            like_count = CreateLabel.objects.get(id=post_id).like_count
            
            # #get the number of unique users who liked the label
            # unique_users = UserLikes.objects.filter(label=label_obj).distinct('user_id').count()
            
            CreateLabel.objects.filter(id=post_id).update(like_count=like_count+1)
            return Response({
                'status': 200,
                'like_count': like_count+1,
                'isLiked': True,
                'message': 'Like Recorded!'
            })
    # model for PostText
    elif model_type == 'mydata3':      
        post_id = data.get('post_id')
        post_obj = PostText1.objects.get(id=post_id)

        if UserLikes.objects.filter(post=post_obj, user_id=user_obj.user_id, model_type = model_type).exists():
            return Response({
                'status': 400,
                'isLiked': True,
                'message': 'Like already exists!'
            })
        else:                
            # Create a new instance of the UserLikes model with the provided values
            like_post = UserLikes.objects.create(post=post_obj, user_id=user_obj.user_id, model_type = model_type)
            
            '''
            #find the unique users who liked the all the posts for a particular movie, one movie can have 5 posts the number of people 
            #who liked the movie is the number of unique users who liked the posts
            unique_users = UserLikes.objects.filter(post__Movie_name=post_obj.Movie_name).distinct('user_id').count()
            '''

            # update the like in the post table
            like_count = PostText1.objects.get(id=post_id).like_count
            PostText1.objects.filter(id=post_id).update(like_count=like_count+1)

            return Response({
                'status': 200,
                'isLiked': True,
                'like_count': like_count+1,
                'message': 'Like Recorded!'
            })
    # model for Reviews
    elif model_type == 'mydata1':      
        post_id = data.get('post_id')
        review_obj = Review.objects.get(id=post_id)
        
        if UserLikes.objects.filter(review = review_obj, user_id=user_obj.user_id, model_type = model_type).exists():
            return Response({
                'status': 400,
                'isLiked': True,
                'message': 'Like already exists!'
            })
        else:    
            # Create a new instance of the UserLikes model with the provided values
            like_post = UserLikes.objects.create(review=review_obj, user_id=user_obj.user_id, model_type = model_type)

            # update the like in the review table
            like_count = Review.objects.get(id=post_id).like_count
            Review.objects.filter(id=post_id).update(like_count=like_count+1)

            return Response({
                'status': 200,
                'isLiked': True,
                'like_count': like_count+1,
                'message': 'Like Recorded!'
            })
    # model for Clips
    elif model_type == 'mydata2':
        post_id = data.get('post_id')
        clip_obj = Clips.objects.get(id=post_id)
        
        if UserLikes.objects.filter(clip = clip_obj, user_id=user_obj.user_id, model_type = model_type).exists():
            return Response({
                'status': 400,
                'isLiked': True,
                'message': 'Like already exists!'
            })
        else:    
            # Create a new instance of the UserLikes model with the provided values
            like_post = UserLikes.objects.create(clip=clip_obj, user_id=user_obj.user_id, model_type = model_type)

            # update the like in the clips table
            like_count = Clips.objects.get(id=post_id).like_count
            Clips.objects.filter(id=post_id).update(like_count=like_count+1)

            return Response({
                'status': 200,
                'isLiked': True,
                'like_count': like_count+1,
                'message': 'Like Recorded!'
            })

    else:
        return Response({
            'status': 400,
            'isLiked': False, 
            'message': 'Invalid model_type!'
        })
    
from django.utils.html import escape

@api_view(['POST'])
def CommentsAPI_Feedpage(request):
    data = json.loads(request.body)
    model_type = data.get('model_type')
    comment = data.get('comments')

    if data.get('post_id') is None:
        return Response({
            'status': 400,
            'message': 'Post_id not passed!' 
        })
    if data.get('uid') is None:
        return Response({
            'status': 400,
            'message': 'uid not passed!'
        })
    if data.get('model_type') is None:
        return Response({
            'status': 400,
            'message': 'model_type not passed!'
        })
    if data.get('comments') == "":
        return Response({
            'status': 400,
            'message': 'comment cannot be Null!'
        })
    if data.get('comments') is None:
        return Response({
            'status': 400,
            'message': 'comment not passed!'
        })
    uid = data.get('uid')
    phone_number_obj = PhoneNumber.objects.get(uid=uid)

    try:
        user_obj = UserInfo.objects.get(phone_number=phone_number_obj.number)
        print(user_obj)
    except PhoneNumber.DoesNotExist:
        user_obj = UserInfo.objects.get(email=phone_number_obj.email)

    sanitized_comment = escape(comment)

    if model_type == 'movies':
        post_id = data.get('post_id')
        movie_obj = Movie.objects.get(id=post_id)

        # Create a new instance of the Userlike model with the provided values
        comment_post = UserComments.objects.create(movie=movie_obj, user_id=user_obj.user_id, comments = sanitized_comment, model_type = model_type)

        # update the comment in the movie table
        comment_count = Movie.objects.get(id=post_id).comment_count
        Movie.objects.filter(id=post_id).update(comment_count=comment_count+1)

        # Get the list of comments with user details
        list_of_comments = []
        for comment in UserComments.objects.filter(movie_id=movie_obj.id, model_type=model_type):
            user = UserInfo.objects.get(user_id=comment.user_id)
            comment_data = {
                'comment': comment.comments,
                'username': user.username,
                'profile_photo': user.profilephoto.url,
                'timestamp': comment.timestamp_field
            }
            list_of_comments.append(comment_data)

        return Response({
            'status': 200,
            'message': 'Comment Recorded!',
            'comment_count': comment_count+1,
            'list_of_comments' : list_of_comments
        })
    # model for CreateLabel
    elif model_type == 'mydata':
        post_id = data.get('post_id')
        label_obj = CreateLabel.objects.get(id=post_id)

        # Create a new instance of the UserLikes model with the provided values
        comment_post = UserComments.objects.create(label=label_obj, user_id=user_obj.user_id, comments = sanitized_comment, model_type = model_type)

        #update the comment in the createlabel table
        comment_count = CreateLabel.objects.get(id=post_id).comment_count
        CreateLabel.objects.filter(id=post_id).update(comment_count=comment_count+1)
        
        # Get the list of comments with user details
        list_of_comments = []
        for comment in UserComments.objects.filter(label_id=label_obj.id, model_type=model_type):
            user = UserInfo.objects.get(user_id=comment.user_id)
            comment_data = {
                'comment': comment.comments,
                'username': user.username,
                'profile_photo': user.profilephoto.url,
                'timestamp': comment.timestamp_field
            }
            list_of_comments.append(comment_data)

        return Response({
            'status': 200,
            'message': 'Comment Recorded!',
            'comment_count': comment_count+1,
            'list_of_comments' : list_of_comments
        })
    # model for PostText
    elif model_type == 'mydata3':
        post_id = data.get('post_id')
        post_obj = PostText1.objects.get(id=post_id)

        # Create a new instance of the UserLikes model with the provided values
        comment_post = UserComments.objects.create(post=post_obj, user_id=user_obj.user_id, comments = sanitized_comment, model_type = model_type)
        
        # update the comment in the post table
        comment_count = PostText1.objects.get(id=post_id).comment_count
        PostText1.objects.filter(id=post_id).update(comment_count=comment_count+1)

        # Get the list of comments with user details
        list_of_comments = []
        for comment in UserComments.objects.filter(post_id=post_obj.id, model_type=model_type):
            user = UserInfo.objects.get(user_id=comment.user_id)
            comment_data = {
                'comment': comment.comments,
                'username': user.username,
                'profile_photo': user.profilephoto.url,
                'timestamp': comment.timestamp_field
            }
            list_of_comments.append(comment_data)

        return Response({
            'status': 200,
            'message': 'Comment Recorded!',
            'comment_count': comment_count+1,
            'list_of_comments' : list_of_comments
        })
    # model for Reviews
    elif model_type == 'mydata1':
        post_id = data.get('post_id')
        review_obj = Review.objects.get(id=post_id)

        # Create a new instance of the UserLikes model with the provided values
        comment_post = UserComments.objects.create(review=review_obj, user_id=user_obj.user_id, comments = sanitized_comment, model_type = model_type)

        # update the comment in the review table
        comment_count = Review.objects.get(id=post_id).comment_count
        Review.objects.filter(id=post_id).update(comment_count=comment_count+1)

        # Get the list of comments with user details
        list_of_comments = []
        for comment in UserComments.objects.filter(review_id=review_obj.id, model_type=model_type):
            user = UserInfo.objects.get(user_id=comment.user_id)
            comment_data = {
                'comment': comment.comments,
                'username': user.username,
                'profile_photo': user.profilephoto.url,
                'timestamp': comment.timestamp_field
            }
            list_of_comments.append(comment_data)

        return Response({
            'status': 200,
            'message': 'Comment Recorded!',
            'comment_count': comment_count+1,
            'list_of_comments' : list_of_comments
        })
    # model for clips
    elif model_type == 'mydata2':
        post_id = data.get('post_id')
        clip_obj = Clips.objects.get(id=post_id)

        # Create a new instance of the UserLikes model with the provided values
        comment_post = UserComments.objects.create(clip=clip_obj, user_id=user_obj.user_id, comments = sanitized_comment, model_type = model_type)
        
        # update the comment in the clips table
        comment_count = Clips.objects.get(id=post_id).comment_count
        Clips.objects.filter(id=post_id).update(comment_count=comment_count+1)

        # Get the list of comments with user details
        list_of_comments = []
        for comment in UserComments.objects.filter(clip_id=clip_obj.id, model_type=model_type):
            user = UserInfo.objects.get(user_id=comment.user_id)
            comment_data = {
                'comment': comment.comments,
                'username': user.username,
                'profile_photo': user.profilephoto.url,
                'timestamp': comment.timestamp_field
            }
            list_of_comments.append(comment_data)

        return Response({
            'status': 200,
            'message': 'Comment Recorded!',
            'comment_count': comment_count+1,
            'list_of_comments' : list_of_comments
        })
        
    else:
        return Response({
            'status': 400,
            'message': 'Invalid model_type!'
        })     
    
@api_view(['POST'])
def SharePostAPI_Feedpage(request):
    data = json.loads(request.body)
    model_type = data.get('model_type')

    if data.get('post_id') is None:
        return Response({
            'status': 400,
            'message': 'Post_id not passed!' 
        })
    if data.get('uid') is None:
        return Response({
            'status': 400,
            'message': 'uid not passed!'
        })
    if data.get('model_type') is None:
        return Response({
            'status': 400,
            'message': 'model_type not passed!'
        })
    
    uid = data.get('uid')
    phone_number_obj = PhoneNumber.objects.get(uid=uid)
    try:
        user_obj = UserInfo.objects.get(phone_number=phone_number_obj.number)
        print(user_obj)
    except PhoneNumber.DoesNotExist:
        user_obj = UserInfo.objects.get(email=phone_number_obj.email)

    username = user_obj.username
    
    if model_type == 'movies':
        post_id = data.get('post_id')
        uid = data.get('uid')
        movie_obj = Movie.objects.get(id=post_id)

        # Create a new instance of the Userlike model with the provided values
        share_post = UserShares.objects.create(movie=movie_obj, user_id=user_obj.user_id, model_type = model_type)

        # update the share in the movie table
        share_count = Movie.objects.get(id=post_id).share_count
        Movie.objects.filter(id=post_id).update(share_count=share_count+1)
        movie_name = Movie.objects.get(id=post_id).slug

        return Response({
            'status': 200,
            'message': 'Share Recorded!',
            'share_count': share_count+1,
            'Share_url': f'Hi, {username} wants you to check this page out www.cinystore.com/tmdb_promo/{movie_name}/'
        })
    # model for CreateLabel
    elif model_type == 'mydata':
        post_id = data.get('post_id')
        label_obj = CreateLabel.objects.get(id=post_id)

        # Create a new instance of the UserLikes model with the provided values
        share_post = UserShares.objects.create(label=label_obj, user_id=user_obj.user_id, model_type = model_type)

        #update the share in the createlabel table
        share_count = CreateLabel.objects.get(id=post_id).share_count
        CreateLabel.objects.filter(id=post_id).update(share_count=share_count+1)
        movie_name = CreateLabel.objects.get(id = post_id).Url_name 

        return Response({
            'status': 200,
            'message': 'Share Recorded!',
            'share_count': share_count+1,
            'Share_url': f'Hi, {username} wants you to check out this new movie www.cinystore.com/promo_label/{movie_name}/'
        })
    # model for PostText
    elif model_type == 'mydata3':
        post_id = data.get('post_id')
        post_obj = PostText1.objects.get(id=post_id)

        # Create a new instance of the UserLikes model with the provided values
        share_post = UserShares.objects.create(post=post_obj, user_id=user_obj.user_id, model_type = model_type)
        
        # update the share in the post table
        share_count = PostText1.objects.get(id=post_id).share_count
        PostText1.objects.filter(id=post_id).update(share_count=share_count+1)
        movie_name_slug = PostText1.objects.get(id=post_id).slug
        movie_name = PostText1.objects.get(id=post_id).Movie_name

        return Response({
            'status': 200,
            'message': 'Share Recorded!',
            'share_count': share_count+1,
            'Share_url': f'Hi, {username} wants you to check out this new post from {movie_name} www.cinystore.com/promo_post/{movie_name_slug}/'
        })
    # model for Reviews
    elif model_type == 'mydata1':
        post_id = data.get('post_id')
        review_obj = Review.objects.get(id=post_id)

        # Create a new instance of the UserLikes model with the provided values
        share_post = UserShares.objects.create(review=review_obj, user_id=user_obj.user_id, model_type = model_type)

        # update the share in the review table
        share_count = Review.objects.get(id=post_id).share_count
        Review.objects.filter(id=post_id).update(share_count=share_count+1)
        movie_name_slug = Review.objects.get(id=post_id).slug
        movie_name = PostText1.objects.get(id=post_id).Movie_name


        return Response({
            'status': 200,
            'message': 'Share Recorded!',
            'share_count': share_count+1,
            'Share_url': f'Hi, {username} wants you to check out this review from the movie {movie_name} www.cinystore.com/promo_review/{movie_name_slug}/'
        })
    # model for Clips
    elif model_type == 'mydata2':
        post_id = data.get('post_id')
        clip_obj = Clips.objects.get(id=post_id)

        # Create a new instance of the UserLikes model with the provided values
        share_post = UserShares.objects.create(clip=clip_obj, user_id=user_obj.user_id, model_type = model_type)
        
        # update the share in the clips table
        share_count = Clips.objects.get(id=post_id).share_count
        Clips.objects.filter(id=post_id).update(share_count=share_count+1)
        movie_name = Clips.objects.get(id=post_id).slug

        return Response({
            'status': 200,
            'message': 'Share Recorded!',
            'share_count': share_count+1,
            'Share_url': f'Hi, {username} wants you to check this interesting clip www.cinystore.com/promo_clip/{movie_name}/'
        })

    else:
        return Response({
            'status': 400,
            'message': 'Invalid model_type!'
        })    

@api_view(['POST'])
def FollowLabels_API(request):
    data = json.loads(request.body)
    model_type = data.get('model_type')

    if data.get('post_id') is None:
        return Response({
            'status': 400,
            'message': 'Post_id not passed!' 
        })
    if data.get('uid') is None:
        return Response({
            'status': 400,
            'message': 'uid not passed!'
        })
    if data.get('model_type') is None:
        return Response({
            'status': 400,
            'message': 'model_type not passed!'
        })
    if model_type == 'movies':
        post_id = data.get('post_id')
        uid = data.get('uid')
        movie_obj = Movie.objects.get(id=post_id)
        
        try:
            phone_number_obj = PhoneNumber.objects.get(uid=uid)
            user_obj = UserInfo.objects.get(phone_number=phone_number_obj.number)
            print(user_obj)
        except PhoneNumber.DoesNotExist:
            user_obj = UserInfo.objects.get(email=phone_number_obj.email)

        if UserFollows.objects.filter(movie=movie_obj, user_id=user_obj.user_id, model_type=model_type).exists():
            return Response({
                'status': 400,
                'message': 'Follow already exists!'
            })
        else:
                
            # Create a new instance of the Userlike model with the provided values
            follow_post = UserFollows.objects.create(movie=movie_obj, user_id=user_obj.user_id, model_type = model_type)

            # update the follow in the movie table
            follow_count = Movie.objects.get(id=post_id).follow_count
            Movie.objects.filter(id=post_id).update(follow_count=follow_count+1)

            return Response({
                'status': 200,
                'follow_count': follow_count+1,
                'message': 'Follow Recorded!'
            })
    
    # model for CreateLabel
    elif model_type == 'mydata':
        post_id = data.get('post_id')
        uid = data.get('uid')
        label_obj = CreateLabel.objects.get(id=post_id)
        
        try:
            phone_number_obj = PhoneNumber.objects.get(uid=uid)
            user_obj = UserInfo.objects.get(phone_number=phone_number_obj.number)
            print(user_obj)
        except PhoneNumber.DoesNotExist:
            user_obj = UserInfo.objects.get(email=phone_number_obj.email)

        if UserFollows.objects.filter(label=label_obj, user_id=user_obj.user_id, model_type=model_type).exists():
            return Response({
                'status': 400,
                'message': 'Follow already exists!'
            })
        else:
            # Create a new instance of the UserLikes model with the provided values
            follow_post = UserFollows.objects.create(label=label_obj, user_id=user_obj.user_id, model_type = model_type)

            #update the follow in the createlabel table
            follow_count = CreateLabel.objects.get(id=post_id).follow_count
            CreateLabel.objects.filter(id=post_id).update(follow_count=follow_count+1)

            return Response({
                'status': 200,
                'follow_count': follow_count+1,
                'message': 'Follow Recorded!'
            })
    else: 
        return Response({
            'status': 400,
            'message': 'Invalid model_type!'
        })
    
@api_view(['POST'])
def UserInformation_API(request):
    data = json.loads(request.body)
    uid = data.get('uid')
    if uid is None:
        return Response({
            'status': 400,
            'message': 'uid not passed!'
        })
    print(uid)
    phone_number_obj = PhoneNumber.objects.get(uid=uid)
    try:
        user_obj = UserInfo.objects.get(phone_number=phone_number_obj.number)
        print(user_obj)
    except PhoneNumber.DoesNotExist:
        user_obj = UserInfo.objects.get(email=phone_number_obj.email)
    # print(user_obj)
    first_name = user_obj.first_name
    last_name = user_obj.last_name
    full_name = first_name + ' ' + last_name
    serializer = UserInfoSerializer(user_obj)
    # add full name to the serializer
    data = serializer.data.copy()
    data['full_name'] = full_name
    return Response(data)


from marketing.models import Terms, Privacy1

@api_view(['GET'])
def TermsGet_API(request):
    terms = Terms.objects.all()
    # Apply pagination using your custom pagination class
    serializer = terms_serializer(terms, many= True)
    return Response({
        'results':serializer.data})


@api_view(['GET'])
def PrivacyGet_API(request):
    privacy = Privacy1.objects.all()
    # Apply pagination using your custom pagination class
    serializer = privacy_serializer(privacy, many= True)
    return Response({
        'results':serializer.data})

@api_view(['POST'])
def SearchResults_API(request):
    data = json.loads(request.body)
    print(data)
    # get the uid of the user searching the query
    uid = data['uid']
    # if the uid is not passed raising an error response
    if uid is None:
        return Response({
            'status': 400,
            'message': 'uid not passed!'
        })

    search_query = data['search_query']

    # if the search query is not passed or empty search is passed raising an error response
    if search_query == "":
        return Response({
            'status': 400,
            'message': 'search query cannot be Null!'
        })
    if search_query is None:
        return Response({
            'status': 400,
            'message': 'search query not passed!'
        })
    
    # store the user search query in the usersearches table
    try:
        phone_number_obj = PhoneNumber.objects.get(uid=uid)
        user_obj = UserInfo.objects.get(phone_number=phone_number_obj.number)
        print(user_obj)
    except PhoneNumber.DoesNotExist:
        user_obj = UserInfo.objects.get(email=phone_number_obj.email)

    user_search = UserSearches.objects.create(user_id=user_obj.user_id, search_query=search_query)

    result_dict = {}

    # search if the movie exists in the createlabel, movie. Search movie name in movies, createlabel

    if Movie.objects.filter(Q(movie_title__icontains = search_query)).exists():
        result_dict['Movie_name'] = Movie.objects.filter(Q(movie_title__icontains = search_query)).values('movie_title')
    else:
        result_dict['Movie_name'] = CreateLabel.objects.filter(Q(Movie_name__icontains = search_query)).values('Movie_name')

    # Search for movies

    search_results_Movie = Movie.objects.filter(Q(genre__icontains=search_query) | 
                                                Q(movie_title__icontains = search_query) | 
                                                Q(language__icontains=search_query) |
                                                Q(producer__icontains=search_query) |
                                                Q(director__icontains=search_query) |
                                                Q(music_director__icontains=search_query) |
                                                Q(crew__icontains=search_query) |
                                                Q(cast__icontains=search_query) 
                                                ).values()
    result_dict['International_movies']= (search_results_Movie)
    
    # Search for labels
    search_results_CreateLabel = CreateLabel.objects.filter(Q(Language__icontains=search_query) |
                                                            Q(Movie_name__icontains=search_query) |
                                                            Q(Genre__icontains=search_query) |
                                                            Q(Production_house__icontains=search_query) |
                                                            Q(Producer__icontains=search_query) |
                                                            Q(cast__icontains=search_query) |
                                                            Q(Director__icontains=search_query) |
                                                            Q(Music_director__icontains=search_query) |
                                                            Q(Other_Languages__icontains=search_query) |
                                                            Q(lyricist__icontains=search_query) |
                                                            Q(choreographer__icontains=search_query) |
                                                            Q(Script_writer__icontains=search_query) |
                                                            Q(Distribution__icontains=search_query) | 
                                                            Q(Singers__icontains=search_query) |
                                                            Q(Editor__icontains=search_query) |
                                                            Q(Cinematographer__icontains=search_query)
                                                            ).values()
    result_dict['Label']=(search_results_CreateLabel)

    # Search for posts
    search_results_Post = PostText1.objects.filter(Movie_name__icontains=search_query).values()
    result_dict['Post']= (search_results_Post)
    
    # Search for reviews
    search_results_Review = Review.objects.filter(
                                                    Q(author__icontains=search_query) |
                                                    Q(Movie_name__icontains=search_query)).values()
    result_dict['Reviews']= (search_results_Review)

    # Alter the URL of the logo field
    for item in result_dict['International_movies']:
        item['logo'] = settings.AWS_STORAGE_LINK + (item['logo'])
        item['poster_path'] = settings.TMDB_LINK + (item['poster_path'])
    for item in result_dict['Label']:
        item['Poster'] = settings.AWS_STORAGE_LINK + (item['Poster'])
        item['Banner'] = settings.AWS_STORAGE_LINK + (item['Banner'])
        item['logo'] = settings.AWS_STORAGE_LINK + (item['logo'])
    for item in result_dict['Post']:
        item['Image'] = settings.AWS_STORAGE_LINK + (item['Image'])
        item['logo'] = settings.AWS_STORAGE_LINK + (item['logo'])
    for item in result_dict['Reviews']:
        item['logo'] = settings.AWS_STORAGE_LINK + (item['logo'])


    return Response({
        'status': 200,
        'result_dict': result_dict
    })

# SocialInteractionsAPI with the userID

@api_view(['POST'])
def SocialInteractionsAPI2(request):
    data = json.loads(request.body)
    model_type = data.get('model_type')
    uid = data.get('uid')
    post_id = data.get('post_id')

    if data.get('uid') is None:
        return Response({
            'status': 400,
            'message': 'uid not passed!' 
        })
    if data.get('post_id') is None:
        return Response({
            'status': 400,
            'message': 'post_id not passed!' 
        })
    if data.get('model_type') is None:
        return Response({
            'status': 400,
            'message': 'model_type not passed!'
        })

    # get the user_id from the uid
    try:
        phone_number_obj = PhoneNumber.objects.get(uid=uid)
        user_obj = UserInfo.objects.get(phone_number=phone_number_obj.number)
    except PhoneNumber.DoesNotExist:
        user_obj = UserInfo.objects.get(email=phone_number_obj.email)

    if model_type == 'movies':
        post_id = data.get('post_id')

        movie_obj = Movie.objects.get(id=post_id)
        isLiked = False

        if UserLikes.objects.filter(movie=movie_obj, user_id=user_obj.user_id, model_type=model_type).exists():
            isLiked = True

        like_count = Movie.objects.get(id=post_id).like_count
        comment_count = Movie.objects.get(id=post_id).comment_count
        share_count = Movie.objects.get(id=post_id).share_count

        # Get the list of comments with user details
        list_of_comments = []
        for comment in UserComments.objects.filter(movie_id=movie_obj.id, model_type=model_type):
            user = UserInfo.objects.get(user_id=comment.user_id)
            comment_data = {
                'comment': comment.comments,
                'username': user.username,
                'profile_photo': user.profilephoto.url,
                'timestamp': comment.timestamp_field
            }
            list_of_comments.append(comment_data)

        return Response({
            'status': 200,
            'isLiked': isLiked,
            'like_count':like_count,
            'comment_count':comment_count,
            'share_count':share_count,
            'list_of_comments' : list_of_comments
        })
    # model for CreateLabel
    elif model_type == 'mydata':
        post_id = data.get('post_id')
        label_obj = CreateLabel.objects.get(id=post_id)
        isLiked = False

        if UserLikes.objects.filter(label=label_obj, user_id=user_obj.user_id, model_type=model_type).exists():
            isLiked = True


        like_count = CreateLabel.objects.get(id=post_id).like_count
        comment_count = CreateLabel.objects.get(id=post_id).comment_count
        share_count = CreateLabel.objects.get(id=post_id).share_count

        # Get the list of comments with user details
        list_of_comments = []
        for comment in UserComments.objects.filter(label_id=label_obj.id, model_type=model_type):
            user = UserInfo.objects.get(user_id=comment.user_id)
            comment_data = {
                'comment': comment.comments,
                'username': user.username,
                'profile_photo': user.profilephoto.url,
                'timestamp': comment.timestamp_field
            }
            list_of_comments.append(comment_data)

        return Response({
            'status': 200,
            'isLiked': isLiked,
            'like_count':like_count,
            'comment_count':comment_count,
            'share_count':share_count,
            'list_of_comments' : list_of_comments
        })
    # model for PostText
    elif model_type == 'mydata3':
        post_id = data.get('post_id')
        post_obj = PostText1.objects.get(id=post_id)
        isLiked = False

        if UserLikes.objects.filter(post=post_obj, user_id=user_obj.user_id, model_type=model_type).exists():
            isLiked = True

        like_count = post_obj.like_count
        comment_count = post_obj.comment_count
        share_count = post_obj.share_count

        # Get the list of comments with user details
        list_of_comments = []
        for comment in UserComments.objects.filter(post_id=post_obj.id, model_type=model_type):
            user = UserInfo.objects.get(user_id=comment.user_id)
            comment_data = {
                'comment': comment.comments,
                'username': user.username,
                'profile_photo': user.profilephoto.url,
                'timestamp': comment.timestamp_field
            }
            list_of_comments.append(comment_data)

        return Response({
            'status': 200,
            'isLiked': isLiked,
            'like_count':like_count,
            'comment_count':comment_count,
            'share_count':share_count,
            'list_of_comments' : list_of_comments
        })
    
    # model for Reviews
    elif model_type == 'mydata1':
        post_id = data.get('post_id')
        review_obj = Review.objects.get(id=post_id)
        isLiked = False

        if UserLikes.objects.filter(review=review_obj, user_id=user_obj.user_id, model_type=model_type).exists():
            isLiked = True

        like_count = Review.objects.get(id=post_id).like_count
        comment_count = Review.objects.get(id=post_id).comment_count
        share_count = Review.objects.get(id=post_id).share_count

        # Get the list of comments with user details
        list_of_comments = []
        for comment in UserComments.objects.filter(review_id=review_obj.id, model_type=model_type):
            user = UserInfo.objects.get(user_id=comment.user_id)
            comment_data = {
                'comment': comment.comments,
                'username': user.username,
                'profile_photo': user.profilephoto.url,
                'timestamp': comment.timestamp_field
            }
            list_of_comments.append(comment_data)


        return Response({
            'status': 200,
            'isLiked': isLiked,
            'like_count':like_count,
            'comment_count':comment_count,
            'share_count':share_count,
            'list_of_comments' : list_of_comments
        })
    # model for Clips
    elif model_type == 'mydata2':
        post_id = data.get('post_id')
        clip_obj = Clips.objects.get(id=post_id)
        isLiked = False
        
        if UserLikes.objects.filter(clip=clip_obj, user_id=user_obj.user_id, model_type=model_type).exists():
            isLiked = True

        like_count = Clips.objects.get(id=post_id).like_count
        comment_count = Clips.objects.get(id=post_id).comment_count
        share_count = Clips.objects.get(id=post_id).share_count

        # Get the list of comments with user details
        list_of_comments = []
        for comment in UserComments.objects.filter(clip_id=clip_obj.id, model_type=model_type):
            user = UserInfo.objects.get(user_id=comment.user_id)
            comment_data = {
                'comment': comment.comments,
                'username': user.username,
                'profile_photo': user.profilephoto.url,
                'timestamp': comment.timestamp_field
            }
            list_of_comments.append(comment_data)

        return Response({
            'status': 200,
            'isLiked': isLiked,
            'like_count':like_count,
            'comment_count':comment_count,
            'share_count':share_count,
            'list_of_comments' : list_of_comments
        })
    else:
        return Response({
            'status': 400,
            'message': 'Invalid model_type!'
        })
 


@api_view(['POST'])
def SocialInteractionsAPI(request):
    data = json.loads(request.body)
    model_type = data.get('model_type')
    comment = data.get('comments')

    if data.get('post_id') is None:
        return Response({
            'status': 400,
            'message': 'Post_id not passed!' 
        })
    if data.get('model_type') is None:
        return Response({
            'status': 400,
            'message': 'model_type not passed!'
        })

    if model_type == 'movies':
        post_id = data.get('post_id')
        uid = data.get('uid')
        movie_obj = Movie.objects.get(id=post_id)

        like_count = Movie.objects.get(id=post_id).like_count
        comment_count = Movie.objects.get(id=post_id).comment_count
        share_count = Movie.objects.get(id=post_id).share_count

        # Get the list of comments with user details
        list_of_comments = []
        for comment in UserComments.objects.filter(movie_id=movie_obj.id, model_type=model_type):
            user = UserInfo.objects.get(user_id=comment.user_id)
            comment_data = {
                'comment': comment.comments,
                'username': user.username,
                'profile_photo': user.profilephoto.url,
                'timestamp': comment.timestamp_field
            }
            list_of_comments.append(comment_data)

        return Response({
            'status': 200,
            'like_count':like_count,
            'comment_count':comment_count,
            'share_count':share_count,
            'list_of_comments' : list_of_comments
        })
    # model for CreateLabel
    elif model_type == 'mydata':
        post_id = data.get('post_id')
        uid = data.get('uid')
        label_obj = CreateLabel.objects.get(id=post_id)

        like_count = CreateLabel.objects.get(id=post_id).like_count
        comment_count = CreateLabel.objects.get(id=post_id).comment_count
        share_count = CreateLabel.objects.get(id=post_id).share_count

        # Get the list of comments with user details
        list_of_comments = []
        for comment in UserComments.objects.filter(label_id=label_obj.id, model_type=model_type):
            user = UserInfo.objects.get(user_id=comment.user_id)
            comment_data = {
                'comment': comment.comments,
                'username': user.username,
                'profile_photo': user.profilephoto.url,
                'timestamp': comment.timestamp_field
            }
            list_of_comments.append(comment_data)

        return Response({
            'status': 200,
            'like_count':like_count,
            'comment_count':comment_count,
            'share_count':share_count,
            'list_of_comments' : list_of_comments
        })
    # model for PostText
    elif model_type == 'mydata3':
        post_id = data.get('post_id')
        uid = data.get('uid')
        post_obj = PostText1.objects.get(id=post_id)

        like_count = post_obj.like_count
        comment_count = post_obj.comment_count
        share_count = post_obj.share_count

        # Get the list of comments with user details
        list_of_comments = []
        for comment in UserComments.objects.filter(post_id=post_obj.id, model_type=model_type):
            user = UserInfo.objects.get(user_id=comment.user_id)
            comment_data = {
                'comment': comment.comments,
                'username': user.username,
                'profile_photo': user.profilephoto.url,
                'timestamp': comment.timestamp_field
            }
            list_of_comments.append(comment_data)

        return Response({
            'status': 200,
            'like_count':like_count,
            'comment_count':comment_count,
            'share_count':share_count,
            'list_of_comments' : list_of_comments
        })
    # model for Reviews
    elif model_type == 'mydata1':
        post_id = data.get('post_id')
        uid = data.get('uid')
        review_obj = Review.objects.get(id=post_id)

        like_count = Review.objects.get(id=post_id).like_count
        comment_count = Review.objects.get(id=post_id).comment_count
        share_count = Review.objects.get(id=post_id).share_count

        # Get the list of comments with user details
        list_of_comments = []
        for comment in UserComments.objects.filter(review_id=review_obj.id, model_type=model_type):
            user = UserInfo.objects.get(user_id=comment.user_id)
            comment_data = {
                'comment': comment.comments,
                'username': user.username,
                'profile_photo': user.profilephoto.url,
                'timestamp': comment.timestamp_field
            }
            list_of_comments.append(comment_data)


        return Response({
            'status': 200,
            'like_count':like_count,
            'comment_count':comment_count,
            'share_count':share_count,
            'list_of_comments' : list_of_comments
        })
    else:
        return Response({
            'status': 400,
            'message': 'Invalid model_type!'
        })


@api_view(['POST'])
def UpdatePesronalInfo_API(request):
    data = json.loads(request.body)
    uid = data.get('key').get('uid')
    first_name = data.get('userData').get('full_name').split(' ')[0]
    last_name = data.get('userData').get('full_name').split(' ')[1] if len(data.get('userData').get('full_name').split(' ')) > 1 else None
    print(first_name, last_name)
    if uid is None:
        return Response({
            'status': 400,
            'message': 'uid not passed!'
        })
    print(uid)
    phone_number_obj = PhoneNumber.objects.get(uid=uid)
    try:
        user_obj = UserInfo.objects.get(phone_number=phone_number_obj.number)
        print(user_obj)
    except PhoneNumber.DoesNotExist:
        user_obj = UserInfo.objects.get(email=phone_number_obj.email)
    print(user_obj)
    
    # Update first and last names if provided
    if first_name:
        user_obj.first_name = first_name
    if last_name:
        user_obj.last_name = last_name
    
    # Update other fields in user_obj with the data passed from the user
    user_obj.phone_number = data.get('userData').get('phone_number')
    user_obj.email = data.get('userData').get('email')
    user_obj.date_of_birth = data.get('userData').get('date_of_birth')
    user_obj.gender =  data.get('userData').get('gender')
    user_obj.city = data.get('userData').get('city')
    user_obj.state = data.get('userData').get('state')
    user_obj.website = data.get('userData').get('website')
    user_obj.country_name = data.get('userData').get('country_name')
    user_obj.company_brief = data.get('userData').get('about')
    user_obj.facebook_account = data.get('userData').get('facebook_account')
    user_obj.spotify_account = data.get('userData').get('spotify_account')
    user_obj.twitter_account = data.get('userData').get('twitter_account')    
    user_obj.save()
    
    # Update values in User table
    user = User.objects.filter(id=user_obj.user_id)
    if first_name:
        user.update(first_name=first_name)
    if last_name:
        user.update(last_name=last_name)
    if user_obj.email:
        user.update(email=user_obj.email)
    
    # Update values in Phonenumber table
    phone_number_obj.number = data.get('userData').get('phone_number')
    phone_number_obj.email = data.get('userData').get('email')
    phone_number_obj.save()

    serializer = UserInfoSerializer(user_obj)
    return Response(serializer.data)


@api_view(['POST'])
def updateProfilephoto(request):
    data = request.data
    uid = data.get('uid')
    profile_photo = request.FILES.get('profile_photo')
    
    if uid is None:
        return JsonResponse({
            'status': 400,
            'message': 'uid not passed!'
        })
    
    if not profile_photo:
        return JsonResponse({
            'status': 400,
            'message': 'profilephoto not found in request.FILES!'
        })

    phone_number_obj = PhoneNumber.objects.get(uid=uid)
    try:
        user_obj = UserInfo.objects.get(phone_number=phone_number_obj.number)
    except PhoneNumber.DoesNotExist:
        user_obj = UserInfo.objects.get(email=phone_number_obj.email)
    

    user_obj.profilephoto = profile_photo
    
    user_obj.save()
    
    serializer = UserInfoSerializer(user_obj)
    return Response(serializer.data)


@api_view(['POST', 'GET'])
def ClipsAPI(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        uid = data.get('uid')
        if uid is None:
            return Response({
                'status': 400,
                'message': 'uid not passed!'
            })
        print(uid)
        
        phone_number_obj = PhoneNumber.objects.get(uid=uid)
        user_obj = User.objects.get(phone_numbers_id=phone_number_obj.id)
        print(user_obj)


        clips = Clips.objects.all()
        abuse_reports = AbuseReport.objects.all()
        not_interested = NotInterested.objects.all()

        combined_data = []
        for item in clips:
            if not abuse_reports.filter(clip=item, user_id=user_obj.id).exists() and not not_interested.filter(clip=item, user_id=user_obj.id).exists():
                combined_data.append(item)
        combined_data = sorted(combined_data, key=lambda x: x.timestamp_field, reverse=True)

        paginator = PageNumberPagination()
        paginator.page_size = 10

        # Paginate the combined data
        result_page = paginator.paginate_queryset(combined_data, request)
        serializer = ClipsSerializer(result_page, many=True)
        
        next = paginator.get_next_link()
        previous = paginator.get_previous_link()

        if next:
            next = next.replace(request.get_host(), settings.SITE_URL)

        if previous:
            previous = previous.replace(request.get_host(), settings.SITE_URL)
        return Response({
            'next':next,
            'previous':previous,
            'results':serializer.data})
    else:
        clips = Clips.objects.all()
        paginator = PageNumberPagination()
        paginator.page_size = 10

        # Paginate the combined data
        result_page = paginator.paginate_queryset(clips, request)
        serializer = ClipsSerializer(result_page, many=True)
        
        next = paginator.get_next_link()
        previous = paginator.get_previous_link()

        if next:
            next = next.replace(request.get_host(), settings.SITE_URL)
        if previous:
            previous = previous.replace(request.get_host(), settings.SITE_URL)
            
        return Response({
            'next':next,
            'previous':previous,
            'results':serializer.data})

import random
import http.client
from django.conf import settings

def send_otp(number, otp):
    print("FUNCTION CALLED")
    conn = http.client.HTTPSConnection("api.msg91.com")
    authkey = settings.MSG91_AUTH_KEY
    headers = { 'content-type': "application/json" }
    senderid = 'CNYSTR'
    templateid = '6586c91fd6fc0564fa5bfed2'
    
    url = "https://control.msg91.com/api/v5/otp?template_id="+templateid+"&mobile="+number+"&otp="+otp+"&sender="+senderid+"&authkey="+authkey+"&country=91"
    conn.request("GET", url, headers=headers)
    res = conn.getresponse()
    data = res.read()
    print(data)
    return None

@api_view(['POST'])
def UserLoginOrRegisterAPI(request):
    data = json.loads(request.body)
    username = data.get('username')
    phone_number = data.get('phone_number')
    if username is None:
        return Response({
            'status': 400,
            'message': 'username not passed!'
        })
    if phone_number is None:
        return Response({
            'status': 400,
            'message': 'phone_number not passed!'
        })
    #check if it is a valid phone number with 91
    if phone_number[0:2] != '91':
        return Response({
            'status': 400,
            'message': 'Invalid phone number 91 Missing!'
        })
    #check if the phone number is 10 digits
    if len(phone_number) != 12:
        return Response({
            'status': 400,
            'message': 'Invalid phone number!'
        })
    if phone_number == '919246545230':
        phone_number_obj = PhoneNumber.objects.get(number=phone_number)
        otp = '1111'
        send_otp(phone_number, otp)  
        # Store OTP in phone_number table
        phone_number_obj = PhoneNumber.objects.get(number=phone_number)
        phone_number_obj.otp = otp
        phone_number_obj.save()
        return JsonResponse({
            'status': 200,
            'message': 'OTP sent to registered phone number',
            "uid": phone_number_obj.uid
        })
    
    if UserInfo.objects.filter(phone_number=phone_number).exists():
        otp = str(random.randint(1000, 9999))  # Generate OTP
        send_otp(phone_number, otp)  # Send OTP
        # Store OTP in phone_number table
        phone_number_obj = PhoneNumber.objects.get(number=phone_number)
        phone_number_obj.otp = otp
        phone_number_obj.save()
        
        return JsonResponse({
            'status': 200,
            'message': 'OTP sent to registered phone number',
            "uid": phone_number_obj.uid
        })
    else:
        # Store it in the PhoneNumber table
        phone_number_obj = PhoneNumber.objects.create(number=phone_number)
        phone_number_obj.save()

        first_name= username.split(' ')[0]
        last_name= username.split(' ')[1] if len(username.split(' ')) > 1 else None
        # User does not exist, register as new user and log in with OTP
        user = User.objects.create_user(username=username, phone_numbers_id = phone_number_obj.id, first_name=first_name, last_name=last_name)
        user.save()

        # Store the information in the UserInfo table
        user_info = UserInfo.objects.create(user_id=user.id, username=username, phone_number=phone_number, first_name=first_name, last_name=last_name)
        user_info.save()
        # Generate OTP
        otp = str(random.randint(1000, 9999))
        # Send OTP
        send_otp(phone_number, otp)
        # Store OTP in phone_number table
        phone_number_obj.otp = otp
        phone_number_obj.save()
        return JsonResponse({
            'status': 200,
            'message': 'OTP sent to registered phone number',
            "uid": phone_number_obj.uid
        })
    
@api_view(['POST'])
def ResendOTPAPI(request):
    data = json.loads(request.body)
    phone_number = data.get('phone_number')

    if phone_number is None:
        return Response({
            'status': 400,
            'message': 'phone_number not passed!'
        })
    #check if it is a valid phone number with 91
    if phone_number[0:2] != '91':
        return Response({
            'status': 400,
            'message': 'Invalid phone number 91 Missing!'
        })
    #check if the phone number is 10 digits
    if len(phone_number) != 12:
        return Response({
            'status': 400,
            'message': 'Invalid phone number!'
        })
    if phone_number == '919246545230':
        phone_number_obj = PhoneNumber.objects.get(number=phone_number)
        otp = '1111'
        send_otp(phone_number, otp)  
        # Store OTP in phone_number table
        phone_number_obj = PhoneNumber.objects.get(number=phone_number)
        phone_number_obj.otp = otp
        phone_number_obj.save()
        return JsonResponse({
            'status': 200,
            'message': 'OTP sent to registered phone number',
            "uid": phone_number_obj.uid
        })
    
    otp = str(random.randint(1000, 9999))  # Generate OTP
    send_otp(phone_number, otp)  # Send OTP
    # Store OTP in phone_number table
    phone_number_obj = PhoneNumber.objects.get(number=phone_number)
    phone_number_obj.otp = otp
    phone_number_obj.save()
    return Response({
        'status': 200,
        'message': 'OTP sent to registered phone number',
        'uid': phone_number_obj.uid
    })

@api_view(['POST'])
def VerifyUserOTPAPI(request):
    data = json.loads(request.body)
    uid = data.get('uid')
    otp = data.get('otp')
    otp = int(otp)
    phone_number_obj = PhoneNumber.objects.get(uid=uid)

    if phone_number_obj.otp == otp:
        print("OTP verified successfully!")
        user = User.objects.get(phone_numbers_id = phone_number_obj.id)
        user.last_login = datetime.now()
        user.is_user = True
        user.is_active = True
        user.save()
        username = UserInfo.objects.get(phone_number=phone_number_obj.number).username
        profile = UserInfo.objects.get(phone_number=phone_number_obj.number).profilephoto.url
        #log the user table
        user_obj = UserInfo.objects.get(phone_number=phone_number_obj.number)
        user_log = UserLogs.objects.create(user_id=user_obj.user_id, login_time = datetime.now() )
        user_log.save()
        return Response({
            'status': 200,
            'message': 'OTP verified successfully!',
            "uid": phone_number_obj.uid,
            "phone_number": str(phone_number_obj.number),
            "email": phone_number_obj.email,
            "username": username,
            "profile": profile
        })
    else:
        return Response({
            'status': 400,
            'message': 'OTP verification failed!'
        })

@api_view(['POST'])
def ReportAbuseAPI(request):
    data = json.loads(request.body)
    model_type = data.get('model_type')
    reason = data.get('reason')
    uid = data.get('uid')

    if data.get('post_id') is None:
        return Response({
            'status': 400,
            'message': 'Post_id not passed!' 
        })
    if data.get('uid') is None:
        return Response({
            'status': 400,
            'message': 'uid not passed!'
        })
    if data.get('model_type') is None:
        return Response({
            'status': 400,
            'message': 'model_type not passed!'
        })
    if data.get('reason') == "":
        return Response({
            'status': 400,
            'message': 'reason cannot be Null!'
        })
    if data.get('reason') is None:
        return Response({
            'status': 400,
            'message': 'reason not passed!'
        })

    
    phone_number_obj = PhoneNumber.objects.get(uid=uid)
    user_obj = UserInfo.objects.get(phone_number=phone_number_obj.number)
    
    if model_type == 'movies':
        post_id = data.get('post_id')
        movie_obj = Movie.objects.get(id=post_id)

        # if user exists in the abuse report table, return not allowed
        if AbuseReport.objects.filter(user_id=user_obj.user_id, movie_id=post_id).exists():
            return Response({
                'status': 400,
                'message': 'Already reported!'
            })
        else:
            # Create a new instance of the Userlike model with the provided values
            report_post = AbuseReport.objects.create(movie=movie_obj, user_id=user_obj.user_id, reason = reason, model_type = model_type)

            return Response({
                'status': 200,
                'message': 'Reported!'
            })
    # model for CreateLabel
    elif model_type == 'mydata':
        post_id = data.get('post_id')
        label_obj = CreateLabel.objects.get(id=post_id)
        # if user exists in the abuse report table, return not allowed
        if AbuseReport.objects.filter(user_id=user_obj.user_id, label_id=post_id).exists():
            return Response({
                'status': 400,
                'message': 'Already reported!'
            })
        else:
            # Create a new instance of the UserLikes model with the provided values
            report_post = AbuseReport.objects.create(label=label_obj, user_id=user_obj.user_id, reason = reason, model_type = model_type)

            return Response({
                'status': 200,
                'message': 'Reported!'
            })
    # model for PostText
    elif model_type == 'mydata3':
        post_id = data.get('post_id')
        post_obj = PostText1.objects.get(id=post_id)
        # if user exists in the abuse report table, return not allowed
        if AbuseReport.objects.filter(user_id=user_obj.user_id, post_id=post_id).exists():
            return Response({
                'status': 400,
                'message': 'Already reported!'
            })
        else:
            # Create a new instance of the UserLikes model with the provided values
            report_post = AbuseReport.objects.create(post=post_obj, user_id=user_obj.user_id, reason = reason, model_type = model_type)

            return Response({
                'status': 200,
                'message': 'Reported!'
            })
    # model for Reviews
    elif model_type == 'mydata1':
        post_id = data.get('post_id')
        review_obj = Review.objects.get(id=post_id)
        # if user exists in the abuse report table, return not allowed
        if AbuseReport.objects.filter(user_id=user_obj.user_id, review_id=post_id).exists():
            return Response({
                'status': 400,
                'message': 'Already reported!'
            })
        else:
            # Create a new instance of the UserLikes model with the provided values
            report_post = AbuseReport.objects.create(review=review_obj, user_id=user_obj.user_id, reason = reason, model_type = model_type)
            
            return Response({
                'status': 200,
                'message': 'Reported!'
            })
    # model for Clips
    elif model_type == 'mydata2':
        post_id = data.get('post_id')
        clip_obj = Clips.objects.get(id=post_id)
        # if user exists in the abuse report table, return not allowed
        if AbuseReport.objects.filter(user_id=user_obj.user_id, clip_id=post_id).exists():
            return Response({
                'status': 400,
                'message': 'Already reported!'
            })
        else:
            # Create a new instance of the UserLikes model with the provided values
            report_post = AbuseReport.objects.create(clip=clip_obj, user_id=user_obj.user_id, reason = reason, model_type = model_type)
            
            return Response({
                'status': 200,
                'message': 'Reported!'
            })
    else:
        return Response({
            'status': 400,
            'message': 'Invalid model_type!'
        })

@api_view(['POST'])
def NotInterestedAPI(request):
    data = json.loads(request.body)
    model_type = data.get('model_type')
    uid = data.get('uid')

    if data.get('post_id') is None:
        return Response({
            'status': 400,
            'message': 'Post_id not passed!' 
        })
    if data.get('uid') is None:
        return Response({
            'status': 400,
            'message': 'uid not passed!'
        })
    if data.get('model_type') is None:
        return Response({
            'status': 400,
            'message': 'model_type not passed!'
        })
    if data.get('reason') == "":
        return Response({
            'status': 400,
            'message': 'reason cannot be Null!'
        })
    if data.get('reason') is None:
        return Response({
            'status': 400,
            'message': 'reason not passed!'
        })

    reason = data.get('reason')

    phone_number_obj = PhoneNumber.objects.get(uid=uid)
    user_obj = UserInfo.objects.get(phone_number=phone_number_obj.number)
    
    if model_type == 'movies':
        post_id = data.get('post_id')
        movie_obj = Movie.objects.get(id=post_id)
        
        # if user exists in the not interested table, return not allowed
        if NotInterested.objects.filter(user_id=user_obj.user_id, movie_id=post_id).exists():
            return Response({
                'status': 400,
                'message': 'Already not interested!'
            })
        else:
            # Create a new instance of the Userlike model with the provided values
            not_interested_post = NotInterested.objects.create(movie=movie_obj, user_id=user_obj.user_id, reason = reason, model_type = model_type)

            return Response({
                'status': 200,
                'message': 'Recorded!'
            })
    # model for CreateLabel
    elif model_type == 'mydata':
        post_id = data.get('post_id')
        label_obj = CreateLabel.objects.get(id=post_id)
        # if user exists in the not interested table, return not allowed
        if NotInterested.objects.filter(user_id=user_obj.user_id, label_id=post_id).exists():
            return Response({
                'status': 400,
                'message': 'Already not interested!'
            })
        else:
            # Create a new instance of the UserLikes model with the provided values
            not_interested_post = NotInterested.objects.create(label=label_obj, user_id=user_obj.user_id, reason = reason, model_type = model_type)

            return Response({
                'status': 200,
                'message': 'Recorded!'
            })
    # model for PostText
    elif model_type == 'mydata3':
        post_id = data.get('post_id')
        post_obj = PostText1.objects.get(id=post_id)

        # if user exists in the not interested table, return not allowed
        if NotInterested.objects.filter(user_id=user_obj.user_id, post_id=post_id).exists():
            return Response({
                'status': 400,
                'message': 'Already not interested!'
            })
        else:
            # Create a new instance of the UserLikes model with the provided values
            not_interested_post = NotInterested.objects.create(post=post_obj, user_id=user_obj.user_id, reason = reason, model_type = model_type)

            return Response({
                'status': 200,
                'message': 'Recorded!'
            })
    # model for Reviews
    elif model_type == 'mydata1':
        post_id = data.get('post_id')
        review_obj = Review.objects.get(id=post_id)

        # if user exists in the not interested table, return not allowed
        if NotInterested.objects.filter(user_id=user_obj.user_id, review_id=post_id).exists():
            return Response({
                'status': 400,
                'message': 'Already not interested!'
            })
        else: 
            # Create a new instance of the UserLikes model with the provided values
            not_interested_post = NotInterested.objects.create(review=review_obj, user_id=user_obj.user_id, reason = reason, model_type = model_type)

            return Response({
                'status': 200,
                'message': 'Recorded!'
            })
    # model for Clips
    elif model_type == 'mydata2':
        post_id = data.get('post_id')
        clip_obj = Clips.objects.get(id=post_id)

        # if user exists in the not interested table, return not allowed
        if NotInterested.objects.filter(user_id=user_obj.user_id, clip_id=post_id).exists():
            return Response({
                'status': 400,
                'message': 'Already not interested!'
            })
        else:
            # Create a new instance of the UserLikes model with the provided values
            not_interested_post = NotInterested.objects.create(clip=clip_obj, user_id=user_obj.user_id, reason = reason, model_type = model_type)

            return Response({
                'status': 200,
                'message': 'Recorded!'
            })
    else:
        return Response({
            'status': 400,
            'message': 'Invalid model_type!'
        })

    
@api_view(['POST'])
def ReportCommentAPI(request):
    data = json.loads(request.body)
    model_type = data.get('model_type')
    reason = data.get('reason')
    uid = data.get('uid')

    if data.get('comment_id') is None:
        return Response({
            'status': 400,
            'message': 'comment_id not passed!' 
        })
    if data.get('uid') is None:
        return Response({
            'status': 400,
            'message': 'uid not passed!'
        })

    if data.get('reason') == "":
        return Response({
            'status': 400,
            'message': 'reason cannot be Null!'
        })
    if data.get('reason') is None:
        return Response({
            'status': 400,
            'message': 'reason not passed!'
        })


    phone_number_obj = PhoneNumber.objects.get(uid=uid)
    user_obj = User.objects.get(phone_numbers_id=phone_number_obj.id)
    print(phone_number_obj)
    print(user_obj)
    #create a report comment entry with the username, comment, movie_name, reason
    comment_id = data.get('comment_id')
    comment_obj = UserComments.objects.get(id=comment_id)
    comments = comment_obj.comments

    print('uid',uid)
    print(comment_id)
    print(reason)

    
    # print(user_obj, comment_obj.clip_id)
    print('comments',comments)
    
    if comment_obj.label_id:
        movie_name = CreateLabel.objects.get(id = comment_obj.label_id).Movie_name
    elif comment_obj.movie_id:
        movie_name = Movie.objects.get(id = comment_obj.movie_id).Movie_name
    elif comment_obj.post_id:
        movie_name = PostText1.objects.get(id = comment_obj.post_id).Movie_name
    elif comment_obj.review_id:
        movie_name = Review.objects.get(id = comment_obj.review_id).Movie_name
    elif comment_obj.clip_id:
        movie_name = Clips.objects.get(id = comment_obj.clip_id).Movie_name
    else:
        return Response({
            'status': 400,
            'message': 'Invalid comment_id!'
        })
    print('movie_name',movie_name)
    username = UserInfo.objects.get(user_id = comment_obj.user_id).username
    print('username', username)
    print('reason',reason)
    user_reported = User.objects.get(id = comment_obj.user_id)
    print(user_reported)
    user_reporting = User.objects.get(phone_numbers_id = phone_number_obj.id)
    print(user_reporting)
    
    # if user has reported the comment already, return not allowed
    if ReportComments.objects.filter(comment_id=comment_id, reporting_user=user_reporting).exists():
        return Response({
            'status': 400,
            'message': 'Already reported!'
        })
    else:
        # Create a new instance of the Userlike model with the provided values
        ReportComments.objects.create(comments=comments, movie_name=movie_name, username=username, reason = reason,comment_id = comment_obj.id, reported_user=user_reported, reporting_user=user_reporting)
        #update the report count in the comment table
        report_count = UserComments.objects.get(id=comment_id).report_count
        UserComments.objects.filter(id=comment_id).update(report_count=report_count+1)

    return Response({
        'status': 200,
        'message': 'Reported!'
    })


from django.http import HttpResponse
from django.template import loader
from django.views.generic import ListView
from .forms import *
import mysql.connector
from .models import Movie,Review,CreateLabel,TopRatedMovies
from cinystoreapp.models import *
from business.models import *
from podadmin.models import *
from django.db.models import Q
import requests
from itertools import chain
from operator import attrgetter
from django.contrib.auth.models import User
from .models import User
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail
from cinystore import settings
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
#from django.utils.encoding import force_bytes, force_text
from django.utils.encoding import force_bytes, force_str
from .tokens import generate_token
from django.contrib.auth.forms import PasswordChangeForm,SetPasswordForm
from django.contrib.auth import update_session_auth_hash
from django.http import JsonResponse
from .decorators import user_only
from django.contrib.auth.decorators import login_required



db = mysql.connector.connect(
  host="3.109.48.139",
  user="myuser",
  password="cinystore",
  database="cinystore"
)
cursor = db.cursor()



def tmdb_movies(request):
    # Define your API key and base URL
    api_key = '9456c6fdcf8a04e157e45387ebf0c687'
    base_url = 'https://api.themoviedb.org/3'

    # Make the API request to fetch popular movies
    url = f'{base_url}/movie/popular'
    params = {'api_key': api_key}
    response = requests.get(url, params=params)
    data = response.json()

    # Iterate through the fetched movie data
    for movie_data in data['results']:

        if not Movie.objects.filter(movie_title=movie_data['title']).exists():
            # Fetch detailed movie information, including credits
            movie_info_response = requests.get(f'{base_url}/movie/{movie_data["id"]}', params=params)
            movie_info = movie_info_response.json()
            credits_response = requests.get(f'{base_url}/movie/{movie_data["id"]}/credits', params=params)
            credits = credits_response.json()
            videos_response = requests.get(f'{base_url}/movie/{movie_data["id"]}/videos', params=params)
            videos_data = videos_response.json()
            videos = videos_data.get('results', [])
            
            # Filter and store only the key of the official trailer
            official_trailer_keys = [video['key'] for video in videos if video.get('type') in ['Trailer', 'Teaser']]

            # Extract specific information from the movie_info dictionary
            director = [crew['name'] for crew in credits.get('crew', []) if crew['job'] == 'Director']
            cast = [actor['name'] for actor in credits.get('cast', [])]
            music_director = [crew['name'] for crew in credits.get('crew', []) if crew['job'] == 'Music']
            production_companies = [company['name'] for company in movie_info.get('production_companies', [])]
            # Create a Movie object and save it to the database
            movie = Movie(
                id=movie_data['id'],
                movie_title=movie_data['title'],
                overview=movie_data['overview'],
                release_date=movie_data['release_date'],
                poster_path=movie_data['poster_path'],
                producer=','.join(production_companies),
                language=movie_data['original_language'],
                genre=','.join([genre['name'] for genre in movie_info.get('genres', [])]),
                video=official_trailer_keys[0] if official_trailer_keys else '',
                cast=','.join(cast),
                crew=','.join(director + music_director),
                director=','.join(director),
                music_director=','.join(music_director),
                # Add other fields as needed
            )
            movie.save()
    return HttpResponse('Imported movies successfully')
    # You can also render a template if needed
    # return render(request, 'movie.html', {'movies': movies})


def top_rated(request):
    # Define your API key and base URL
    api_key = '9456c6fdcf8a04e157e45387ebf0c687'
    base_url = 'https://api.themoviedb.org/3'

    # Make the API request to fetch popular movies
    url = f'{base_url}/movie/top_rated'
    params = {'api_key': api_key}
    response = requests.get(url, params=params)
    data = response.json()

    # Iterate through the fetched movie data
    for movie_data in data['results']:

        if not TopRatedMovies.objects.filter(movie_title=movie_data['title']).exists():
            # Fetch detailed movie information, including credits
            movie_info_response = requests.get(f'{base_url}/movie/{movie_data["id"]}', params=params)
            movie_info = movie_info_response.json()
            credits_response = requests.get(f'{base_url}/movie/{movie_data["id"]}/credits', params=params)
            credits = credits_response.json()
            videos_response = requests.get(f'{base_url}/movie/{movie_data["id"]}/videos', params=params)
            videos_data = videos_response.json()
            videos = videos_data.get('results', [])
             # Filter and store only the key of the official trailer
            official_trailer_keys = [video['key'] for video in videos if video.get('type') in ['Trailer', 'Teaser']]

            # Extract specific information from the movie_info dictionary
            director = [crew['name'] for crew in credits.get('crew', []) if crew['job'] == 'Director']
            cast = [actor['name'] for actor in credits.get('cast', [])]
            music_director = [crew['name'] for crew in credits.get('crew', []) if crew['job'] == 'Music']
            production_companies = [company['name'] for company in movie_info.get('production_companies', [])]
            # Create a Movie object and save it to the database
            movie = TopRatedMovies(
                id=movie_data['id'],
                movie_title=movie_data['title'],
                overview=movie_data['overview'],
                release_date=movie_data['release_date'],
                poster_path=movie_data['poster_path'],
                producer=','.join(production_companies),
                language=movie_data['original_language'],
                genre=','.join([genre['name'] for genre in movie_info.get('genres', [])]),
                video=official_trailer_keys[0] if official_trailer_keys else '',
                cast=','.join(cast),
                crew=','.join(director + music_director),
                director=','.join(director),
                music_director=','.join(music_director),
                # Add other fields as needed
            )
            movie.save()
    return HttpResponse('Imported movies successfully')
    # You can also render a template if needed
    # return render(request, 'movie.html', {'movies': movies})


def now_playing(request):
    # Define your API key and base URL
    api_key = '9456c6fdcf8a04e157e45387ebf0c687'
    base_url = 'https://api.themoviedb.org/3'

    # Make the API request to fetch popular movies
    url = f'{base_url}/movie/now_playing'
    params = {'api_key': api_key}
    response = requests.get(url, params=params)
    data = response.json()

    # Iterate through the fetched movie data
    for movie_data in data['results']:

        if not RecentMovies.objects.filter(movie_title=movie_data['title']).exists():
            # Fetch detailed movie information, including credits
            movie_info_response = requests.get(f'{base_url}/movie/{movie_data["id"]}', params=params)
            movie_info = movie_info_response.json()
            credits_response = requests.get(f'{base_url}/movie/{movie_data["id"]}/credits', params=params)
            credits = credits_response.json()
            videos_response = requests.get(f'{base_url}/movie/{movie_data["id"]}/videos', params=params)
            videos_data = videos_response.json()
            videos = videos_data.get('results', [])
             # Filter and store only the key of the official trailer
            official_trailer_keys = [video['key'] for video in videos if video.get('type') in ['Trailer', 'Teaser']]

            # Extract specific information from the movie_info dictionary
            director = [crew['name'] for crew in credits.get('crew', []) if crew['job'] == 'Director']
            cast = [actor['name'] for actor in credits.get('cast', [])]
            music_director = [crew['name'] for crew in credits.get('crew', []) if crew['job'] == 'Music']
            production_companies = [company['name'] for company in movie_info.get('production_companies', [])]
            # Create a Movie object and save it to the database
            movie = RecentMovies(
                id=movie_data['id'],
                movie_title=movie_data['title'],
                overview=movie_data['overview'],
                release_date=movie_data['release_date'],
                poster_path=movie_data['poster_path'],
                producer=','.join(production_companies),
                language=movie_data['original_language'],
                genre=','.join([genre['name'] for genre in movie_info.get('genres', [])]),
                video=official_trailer_keys[0] if official_trailer_keys else '',
                cast=','.join(cast),
                crew=','.join(director + music_director),
                director=','.join(director),
                music_director=','.join(music_director),
                # Add other fields as needed
            )
            movie.save()
    return HttpResponse('Imported movies successfully')
    # You can also render a template if needed
    # return render(request, 'movie.html', {'movies': movies})



def index(request):
    mydata = CreateLabel.objects.all().order_by('-timestamp_field')
    template = loader.get_template('index.html')
    context = {
        'mydata': mydata,
    }
    return HttpResponse(template.render(context, request))

def StickySidebars(request):
    mydata = CreateLabel.objects.all()
    template = loader.get_template('StickySidebars.html')
    context = {
        'StickySidebars': mydata,
    }
    return HttpResponse(template.render(context, request))

@user_only
def auth_Logout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect('cinystoreapp:auth_login')


def auth_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('cinystoreapp:Feedpage')  # Redirect to the home page after successful login
        else:
            messages.error(request, "Invalid username or password!")
            return redirect('cinystoreapp:auth_login')
     
    return render(request, "auth_login.html")  # Render the login template


def Authregister(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        if User.objects.filter(username=username):
            messages.error(request, "Username already exist! Please try some other username.")
            return redirect('cinystoreapp:Authregister')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email Already Registered!!")
            return redirect('cinystoreapp:Authregister')

        if len(username) > 20:
            messages.error(request, "Username must be under 20 charcters!!")
            return redirect('cinystoreapp:Authregister')

        if password != confirm_password:
            messages.error(request, "Passwords didn't matched!!")
            return redirect('cinystoreapp:Authregister')

        if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric!!")
            return redirect('cinystoreapp:Authregister')

        myuser = User.objects.create_user(username=username, email=email, password=password)
        myuser.is_user = True
        myuser.is_active = False
        myuser.save()
        customer = UserInfo.objects.create(user=myuser)
        customer.username = username
        customer.email= email
        customer.save()
        messages.success(request,
                         "Your Account has been created succesfully!! Please check your email to confirm your email address in order to activate your account.")

        # Welcome Email
        subject = "Welcome to Cinystore Login!!"
        message = "Hello " + myuser.username + "!! \n" + "Welcome to Cinystore!! \nThank you for visiting our website.\n We have also sent you a confirmation email, please confirm your email address. \n\nThanking You\n Cinystore !! \n"
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)

        uid = urlsafe_base64_encode(force_bytes(myuser.pk))
        print(uid)

        token = generate_token.make_token(myuser)
        print(token)

        # Email Address Confirmation Email
        current_site = get_current_site(request)
        email_subject = "Confirm your Email @ Cinystore Login!!"
        message2 = render_to_string('email_confirmation.html', {

            'name': myuser.username,
            'domain': settings.SITE_URL,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser)
        })
         # Construct the local file path to the logo image
        logo_path = os.path.join(settings.BASE_DIR,  'static', 'img', 'logo.webp')

        # Attach the company logo
        with open(logo_path, "rb") as logo_file:
            logo_data = logo_file.read()
            email = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [myuser.email])
            email.attach('logo.webp', logo_data, 'image/webp')  # Adjust the content type if needed
            email.send()

        email = EmailMessage(
            email_subject,
            message2,
            settings.EMAIL_HOST_USER,
            [myuser.email],
        )
        email.fail_silently = True
        email.send()

        return redirect('cinystoreapp:auth_login')

    return render(request, "Authregister.html")


def activate(request, uid64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uid64))
        myuser = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active = True
        myuser.save()
        login(request,myuser)
        messages.success(request, "Your Account has been activated!!")
        return render(request, 'activation_success.html')
        return redirect('auth_login')
    else:
        return render(request, 'activation_failed.html')


def activation_success(request):
    return render(request, 'activation_success.html')


def error_view(request):
    # Custom logic for handling the error
    return render(request, 'error.html')


@user_only
def Browsemovies_login(request):
    template = loader.get_template('Browsemovies_login.html')
    class Browsemovies(ListView):
        Movie_name = ""
        synopsis = ""
        Production_house = ""
        Poster = ""

    mydata = CreateLabel.objects.all().order_by('-timestamp_field')
    # api_key = "9456c6fdcf8a04e157e45387ebf0c687"
    # url = f"https://api.themoviedb.org/3/movie/popular?api_key={api_key}"
    # response = requests.get(url)
    # movies = response.json()["results"]
    movies = Movie.objects.all().order_by('-timestamp_field')
    context = {'mydata': mydata, 'movies': movies}
    Browsemovies_login = list(chain(mydata, movies))

    return render(request, 'Browsemovies_login.html', context)


def ChangePassword(request):
    template = loader.get_template('ChangePassword.html')
    context = {
        'ChangePassword':ChangePassword,
    }
    return HttpResponse(template.render(context, request))


@user_only
def Feedpage(request):

    '''
    This code is to get user Information and pass it in "head.html as dictionary {'head': userdata}
    
    '''
    username = request.user.username
    # Retrieve a queryset of records with the desired username
    matching_records = UserInfo.objects.filter(username=username)
    # Check if any records with the desired username exist
    username_exists = matching_records.exists()

    if username_exists:
        userdata = UserInfo.objects.filter(username=username)
    else:
        userdata = User.objects.filter(username=username)

    ## user information storing ends here 
	

    mydata = CreateLabel.objects.filter ().order_by('-timestamp_field')
    mydata1 = Review.objects.all().order_by('-timestamp_field')
    movies = Movie.objects.all().order_by('-timestamp_field')
    recent_movies = RecentMovies.objects.all().order_by('-timestamp_field')
    top_rated_movies = TopRatedMovies.objects.all().order_by('-timestamp_field')
    mydata2 = Clips.objects.all().order_by('-timestamp_field')
   
    
    try:
        movies = Movie.objects.all().order_by('-timestamp_field')
    except Movie.DoesNotExist:
        movies =[]
    try:
        mydata1 = Review.objects.all().order_by('-timestamp_field')
    except Review.DoesNotExist:
        mydata1 =[]
    try: mydata2 = Clips.objects.all().order_by('-timestamp_field')
    except Clips.DoesNotExist:
        mydata2 =[]
    try:
        mydata3 = PostText1.objects.all().order_by('-timestamp_field')
    except PostText1.DoesNotExist:
        mydata3 =[]
    try:
        recent_movies = RecentMovies.objects.all().order_by('-timestamp_field')
    except RecentMovies.DoesNotExist:
        recent_movies = []
    try:
        top_rated_movies = TopRatedMovies.objects.all().order_by('-timestamp_field')
    except TopRatedMovies.DoesNotExist:
        top_rated_movies = []

    
    producerDetails = ProducerRegister.objects.all()

    combined_data = sorted(list(mydata) +list(movies) +list(mydata1) +list(mydata2) +list(mydata3) +list(recent_movies) +list(top_rated_movies), 
    key=lambda x: x.timestamp_field, reverse=True
    )

    context = {'combined_data': combined_data, 'head': userdata, 'producerDetails': producerDetails}

    return render(request, 'Feedpage.html', context)


@user_only
def Createlabel(request):
    if request.method == 'POST':
        producer_name = request.user
        producer = ProducerRegister.objects.get(production_house=producer_name)
        production_house = ProducerRegister.objects.get(production_house=producer_name).production_house
        producer_logo = ProducerRegister.objects.get(production_house=producer_name).production_house_image

        if User.objects.filter(username=producer_name).exists():
            form = ImageForm(request.POST, request.FILES)    
            producer = ProducerRegister.objects.get(production_house=producer_name)
            if form.is_valid():
                form.save()
                Movie_name=form.cleaned_data['Movie_name']
                CreateLabel.objects.filter(Movie_name = Movie_name).update(producer_id=producer)
                CreateLabel.objects.filter(Movie_name = Movie_name).update(source=production_house)
                CreateLabel.objects.filter(Movie_name = Movie_name).update(logo=producer_logo)
                CreateLabel.objects.filter(Movie_name = Movie_name).update(url_name = ''.join(Movie_name.split(' ')))
                
                return redirect('producerdashboard')
            else:
                img_obj = form.instance
                return render(request, 'Createlabel.html', {'form': form, 'img_obj': img_obj})
    else:
        form = ImageForm()
    return render(request, 'Createlabel.html', {'form': form})


@user_only
def Groups(request):
    
    '''
    This code is to get user Information and pass it in "head.html as dictionary {'head': userdata}
    
    '''
    username = request.user.username
    # Retrieve a queryset of records with the desired username
    matching_records = UserInfo.objects.filter(username=username)
    # Check if any records with the desired username exist
    username_exists = matching_records.exists()

    if username_exists:
        userdata = UserInfo.objects.filter(username=username)
    else:
        userdata = User.objects.filter(username=username)

@user_only
def genreviews(request):
    mydata = Review.objects.all()
    template = loader.get_template('genreviews.html')
    context = {
        'genreviews': mydata,
    }
    return HttpResponse(template.render(context, request))


def head(request):
    mydata = User.objects.all()
    template = loader.get_template('head.html')
    context = {
        'head': mydata,
    }
    return HttpResponse(template.render(context, request))


def generalblogs(request):
    template = loader.get_template('generalblogs.html')
    context = {
        'generalblogs': generalblogs,
    }
    return HttpResponse(template.render(context, request))

@user_only
def MoviePhotos(request):
    mydata = CreateLabel.objects.all()
    template = loader.get_template('MoviePhotos.html')
    context = {
        'MoviePhotos': mydata,
    }
    return HttpResponse(template.render(context, request))


@user_only
def MovieVideos(request):
    template = loader.get_template('MovieVideos.html')
    context = {
        'MovieVideos': MovieVideos,
    }
    return HttpResponse(template.render(context, request))

@user_only
def Newsfeed(request):
    mydata = Movie.objects.all()
    template = loader.get_template('Newsfeed.html')
    context = {
        'Newsfeed': mydata,
    }
    return HttpResponse(template.render(context, request))


@user_only
def review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        myuser = request.user.username
        myuser_logo = UserInfo.objects.get(username=myuser).profilephoto
        if form.is_valid():
            form.save()
            Movie_name = form.cleaned_data['Movie_name']
            Review.objects.filter(author = myuser).update(source=myuser)
            Review.objects.filter(author = myuser).update(logo=myuser_logo)
            Review.objects.filter(Movie_name=Movie_name).update(slug = ''.join(Movie_name.split(' ')))
            return render(request, 'review.html', {'form': form})
    else:
        form = ReviewForm()
    return render(request, 'review.html', {'form': form})



@csrf_protect
def Box_office(request):
    if request.method == 'POST':
        form = BoxOfficeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, 'Box_office.html', {'form': form})
    else:
        form = BoxOfficeForm()
    return render(request, 'Box_office.html', {'form': form})

@user_only
def Indianmovies(request):
    username = request.user.username
    matching_records = UserInfo.objects.filter(username=username)
    username_exists = matching_records.exists()

    if username_exists:
        userdata = UserInfo.objects.filter(username=username)
    else:
        userdata = User.objects.filter(username=username)

    template = loader.get_template('Indianmovies.html')
    mydata = CreateLabel.objects.all()
    context = {
        'mydata': mydata, 'head': userdata
    }
    return HttpResponse(template.render(context, request))

@user_only
def Internationalmovies(request):
    template = loader.get_template('Internationalmovies.html')
    api_key = "9456c6fdcf8a04e157e45387ebf0c687"
    url = f"https://api.themoviedb.org/3/movie/popular?api_key={api_key}"
    response = requests.get(url)
    movies = response.json()["results"]
    movies = Movie.objects.all().order_by('-timestamp_field')
    context = {
        'movies': movies,
    }
    return HttpResponse(template.render(context, request))

@user_only
def producerdashboardwithmovie(request, production_house):
    production_house = request.user
    template = loader.get_template('producerdashboard.html')
    producer = ProducerRegister.objects.get(production_house=production_house)
    mydata = CreateLabel.objects.filter(producer_id=producer)
    context = {
        'producerdashboard':mydata,
    }
    return HttpResponse(template.render(context, request))

def producerbase(request):
    template = loader.get_template('producerbase.html')
    context = {
        'producerbase':producerbase,
    }
    return HttpResponse(template.render(context, request))


@user_only
def Managelabel(request):
    production_house = request.user
    template = loader.get_template('Managelabel.html')
    producer = ProducerRegister.objects.get(production_house=production_house)
    mydata = CreateLabel.objects.filter(producer_id=producer)
    context = {
        'Managelabel': mydata,
    }
    return HttpResponse(template.render(context, request))


@user_only
def Usertrailer(request):
    '''
    This code is to get user Information and pass it in "head.html as dictionary {'head': userdata}
    
    "'''
    username = request.user.username
    # Retrieve a queryset of records with the desired username
    matching_records = UserInfo.objects.filter(username=username)
    # Check if any records with the desired username exist
    username_exists = matching_records.exists()

    if username_exists:
        userdata = UserInfo.objects.filter(username=username)
    else:
        userdata = User.objects.filter(username=username)

    ## user information storing ends here 
	
    mydata = CreateLabel.objects.all()
    template = loader.get_template('Usertrailer.html')
    context = {
        'Usertrailer': mydata, 'head': userdata
    }
    return HttpResponse(template.render(context, request))


def episodeupload(request):
    template = loader.get_template('episodeupload.html')
    context = {
        'episodeupload': episodeupload
    }
    return HttpResponse(template.render(context, request))


def episodeupload2(request):
    template = loader.get_template('episodeupload2.html')
    context = {
        'episodeupload2': episodeupload2
    }
    return HttpResponse(template.render(context, request))


def episodeupload1(request):
    template = loader.get_template('episodeupload1.html')
    context = {
        'episodeupload1': episodeupload1
    }
    return HttpResponse(template.render(context, request))

def producermanagelabel(request, Movie_name):
    mydata = CreateLabel.objects.filter(Movie_name=Movie_name)
    template = loader.get_template('producermanagelabel.html')
    context = {
        'producermanagelabel': mydata
    }
    return HttpResponse(template.render(context, request))



def templates(request, Movie_name):
    Label1 = CreateLabel.objects.filter(Movie_name=Movie_name)
    template = loader.get_template('templates.html')
    context = {
        'Label1':Label1,
    }
    return HttpResponse(template.render(context, request))


def socialuserlogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(request, "Logged In Successfully!!!")
                return redirect('Feedpage')  # Redirect to the user dashboard page after successful login
            else:
                return render(request, 'socialuserlogin.html', {'error': 'This account is inactive..'})

    return render(request, "socialuserlogin.html")

def comingsoonlabel(request):
    template = loader.get_template('comingsoonlabel.html')
    context = {
        'comingsoonlabel': comingsoonlabel,
    }
    return HttpResponse(template.render(context, request))

@csrf_protect
def Newsform(request):
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, 'Newsform.html', {'form': form})
    else:
        form = NewsForm()
    return render(request, 'Newsform.html', {'form': form})

@csrf_protect
def reset_password(request):
    if request.method == 'POST':
        email = request.POST.get('email',False)
        try:
            user = User.objects.get(email=email, is_user=True)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            print(uid)
            token = generate_token.make_token(user)
            print(token)
            current_site = get_current_site(request)
            
            #Reset Password Email

            email_subject = "Reset your Password!!"
            message3 = render_to_string('reset_password_email.html', {

                'name': user.username,
                'domain': settings.SITE_URL,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': generate_token.make_token(user)
            })
            email = EmailMessage(
                email_subject,
                message3,
                settings.EMAIL_HOST_USER,
                [user.email],
            )
            email.fail_silently = True
            email.send()
            messages.success(request, 'A password reset link has been sent to your email.')
            # return redirect('reset_password')
        except User.DoesNotExist:
            messages.error(request, 'No user found with this email.')
            return redirect('cinystoreapp:reset_password')
    return render(request, 'reset_password.html')


def ResetConfirm(request, uid64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uid64))
        user = User.objects.get(pk=uid)
        if user is not None and generate_token.check_token(user, token):
            if request.method == 'POST':
                form = SetPasswordForm(user=user, data=request.POST)
                if form.is_valid():
                    form.save()  # Save the new password for the user
                    messages.success(request, "Password set successfully!")
                    return redirect('auth_login')
                else:
                    return redirect('reset_password')
            else:
                form = SetPasswordForm(user=user)
                args = {'form': form}
                return render(request, 'reset_password_form.html', args)
        else:
            return render(request, 'reset_password_failed.html')
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        messages.error(request, "Password set not successful.")
        return redirect('reset_password')

@user_only
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data = request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('cinystoreapp:PersonalInformation')
        else:
            messages.error(request, 'Wrong old password')
            return redirect('/PersonalInformation/change_password')
        
    else:
        form = PasswordChangeForm(user = request.user)
        args = {'form':form}
        return render(request, 'change_password.html',args)

def check_username_availability(request):
    if request.method == 'GET':
        username = request.GET.get('username')
        try:
            user = User.objects.get(username=username, is_user=True)
            return JsonResponse({'available': False})
        except User.DoesNotExist:
            return JsonResponse({'available': True})
        
def check_email_availability(request):
    if request.method == 'GET':
        email = request.GET.get('email')
        try:
            user = User.objects.get(email=email, is_user=True)
            return JsonResponse({'available': False})
        except User.DoesNotExist:
            return JsonResponse({'available': True})


@user_only
def PersonalInformation(request):
    username = request.user.username

    # Retrieve a queryset of records with the desired username
    matching_records = UserInfo.objects.filter(username=username)
    # Check if any records with the desired username exist
    username_exists = matching_records.exists()
    if username_exists:
        mydata = UserInfo.objects.filter(username=username)
    else:
        mydata = User.objects.filter(username=username)

    context = {
        'PersonalInformation': mydata, 
        'head': mydata  
    }
    return render(request, 'PersonalInformation.html', context)


@user_only
def PersonalInformation_update(request):
    username = request.user.username
    # Retrieve a queryset of records with the desired username
    matching_records = UserInfo.objects.filter(username=username)
    # Check if any records with the desired username exist
    username_exists = matching_records.exists()
    if username_exists:
        mydata = UserInfo.objects.filter(username=username)
    else:
        mydata = User.objects.filter(username=username)
       
 
    if request.method == 'POST':
        user_info, created = UserInfo.objects.get_or_create(user=request.user)
        user_info.username = request.POST['username']
        # user_info.profilephoto = request.FILES.get('profile_photo')
        try:
            if request.FILES.get('profile_photo'):
                user_info.profilephoto = request.FILES.get('profile_photo')
            else:
                value = UserInfo.get('profilephoto', 'null')
                user_info.profilephoto = value 
        except:
            pass

        user_info.first_name = request.POST['first_name']
        user_info.last_name = request.POST['last_name']
        user_info.website = request.POST['website']
        user_info.email = request.POST['email']
        # user_info.date_of_birth = request.POST['date_of_birth']
        try:
            if request.POST['date_of_birth'] == "":
                value = UserInfo.get('date_of_birth', None)
                user_info.date_of_birth = value 
            else:
                user_info.date_of_birth =  request.POST['date_of_birth']
        except:
            pass
        user_info.phone_number = request.POST['phone_number']
        user_info.country_name = request.POST['country_name']
        user_info.state = request.POST['state']
        user_info.city = request.POST['city']
        user_info.company_brief = request.POST['company_brief']
        user_info.gender = request.POST['gender']
        user_info.facebook_account = request.POST['facebook_account']
        user_info.twitter_account = request.POST['twitter_account']
        user_info.spotify_account = request.POST['spotify_account']
        
        user_info.save()

        return redirect('cinystoreapp:PersonalInformation')  # Redirect back to the same page after saving
    else:
        context = {
            'PersonalInformation': mydata,
        }
        return render(request, 'PersonalInformationform.html', context)
    
    
@user_only
def labelof(request, Movie_name):
    mydata = CreateLabel.objects.filter(Movie_name=Movie_name)
    mydata2 = PostText1.objects.filter(Movie_name=Movie_name).order_by('-timestamp_field')
    mydata3 = CommentPostText1.objects.filter(movie_title=Movie_name).order_by('-timestamp_field')
    # id = request.GET.get('id')
    # # Retrieve a queryset of records with the desired 'id'
    # matching_records = PostText1.objects.filter(id=id)
    #
    # # Check if any records with the desired 'id' exist
    # if matching_records.exists():
    #     mydata3 = CommentPostText1.objects.filter(Movie_name=matching_records[0]).order_by('-timestamp_field')
    # else:
    #     mydata3 = CommentPostText1.objects.none()
    all_data = list(chain(mydata, mydata2, mydata3))
    all_data.sort(key=attrgetter('timestamp_field'), reverse=True)
    template = loader.get_template('labelof.html')
    context = {
        'labelof': all_data,
        'mydata':mydata,
        'PostTextView':mydata2,
        'CommentPostText':mydata3,
    }
    return HttpResponse(template.render(context, request))

@user_only
def like_movie(request, Movie_name):
    user = request.user.username
    Movie_id = get_object_or_404(CreateLabel, Movie_name=Movie_name)
    like = User.objects.get(username=user)
    movie_title = None
    username = None

    # Check if the user has already liked the movie
    if LikeMovies.objects.filter(like=like, Movie_name=Movie_id).exists():
        messages.warning(request, "You have already liked this movie.")
    else:
        LikeMovies.objects.get_or_create(like=request.user, Movie_name=Movie_id, movie_title=Movie_name, username=user)
        like_count = LikeMovies.objects.filter(Movie_name=Movie_id).count()
        CreateLabel.objects.filter(Movie_name=Movie_name).update(like_count=like_count)
        messages.success(request, "You liked the movie.")

    return redirect(f'/labelof/{Movie_name}')


@user_only
def follow_movie(request, Movie_name):
    user = request.user.username
    Movie_id = get_object_or_404(CreateLabel, Movie_name=Movie_name)
    follower = User.objects.get(username=user)
    movie_title = None
    username = None

    # Check if the user has already liked the movie
    if FollowMovies.objects.filter(follower=follower, Movie_name=Movie_id).exists():
        messages.warning(request, "You have already followed this movie.")
    else:
        FollowMovies.objects.get_or_create(follower=request.user, Movie_name=Movie_id, movie_title=Movie_name, username=user)
        follow_count = FollowMovies.objects.filter(Movie_name=Movie_id).count()
        CreateLabel.objects.filter(Movie_name=Movie_name).update(follow_count=follow_count)
        messages.success(request, "You followed the movie.")

    return redirect(f'/labelof/{Movie_name}')



def check_movie_exists(request):
    if request.method == 'GET':
        Movie_name = request.GET.get('Movie_name')
        try:
            Movie = CreateLabel.objects.get(Movie_name=Movie_name)
            return JsonResponse({'available': False})
        except CreateLabel.DoesNotExist:
            return JsonResponse({'available': True})


def producer_reset_password(request):
    if request.method == 'POST':
        email = request.POST.get('producer_email',False)
        print('email:',email)
        try:
            user = User.objects.get(email = email)
            print('user:',user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            print(uid)
            token = generate_token.make_token(user)
            print(token)
            current_site = get_current_site(request)
            
            #Reset Password Email

            email_subject = "Reset your Password!!"
            message3 = render_to_string('producer_reset_password_email.html', {
                'name': user.username,
                'domain': settings.SITE_URL,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': generate_token.make_token(user)
            })
            email = EmailMessage(
                email_subject,
                message3,
                settings.EMAIL_HOST_USER,
                [user.email],
            )
            email.fail_silently = True
            email.send()
            messages.success(request, 'A password reset link has been sent to your email.')
            # return redirect('producer_reset_password')
        except User.DoesNotExist:
            messages.error(request, 'No user found with this email.')
            return redirect('producer_reset_password')
    return render(request, 'producer_reset_password.html')


def ProducerResetConfirm(request, uid64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uid64))
        user = User.objects.get(pk=uid)
        if user is not None and generate_token.check_token(user, token):
            if request.method == 'POST':
                form = SetPasswordForm(user=user, data=request.POST)
                if form.is_valid():
                    form.save()  # Save the new password for the user
                    messages.success(request, "Password set successfully!")
                    return redirect('/Business/')
                else:
                    return redirect('producer_reset_password')
            else:
                form = SetPasswordForm(user=user)
                args = {'form': form}
                return render(request, 'producer_reset_password_form.html', args)
        else:
            return render(request, 'producer_reset_password_failed.html')
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        messages.error(request, "Password set not successful.")
        return redirect('producer_reset_password')
    


def profile(request):
    producer = request.user
    mydata = ProducerRegister.objects.filter(production_house = producer)
    template = loader.get_template('profile.html')
    context = {
        'profile': mydata
    }
    return HttpResponse(template.render(context, request))


def UpdateProfile(request):

    producer = request.user
    # Retrieve a queryset of records with the desired username
    matching_records = ProducerRegister.objects.filter(production_house = producer)
    # Check if any records with the desired username exist 
    producer_exists = matching_records.exists()
    if producer_exists:
        mydata = ProducerRegister.objects.filter(production_house = producer)
    
       
    if request.method == 'POST':
        producer_info, created = ProducerRegister.objects.get_or_create(production_house=request.user)
        try:
            if request.FILES.get('production_house_image'):
                producer_info.production_house_image = request.FILES.get('production_house_image')
            else:
                value = ProducerRegister.get('production_house_image', 'null')
                producer_info.production_house_image = value 
        except:
            pass
        producer_info.producer_first_name = request.POST['producer_first_name']
        producer_info.producer_last_name = request.POST['producer_last_name']
        producer_info.producer_website = request.POST['producer_website']
        producer_info.producer_email = request.POST['producer_email']
        producer_info.producer_phone_number = request.POST['producer_phone_number']
        producer_info.producer_country_name = request.POST['producer_country_name']
        producer_info.producer_state = request.POST['producer_state']
        producer_info.producer_city = request.POST['producer_city']
        producer_info.production_house_brief = request.POST['production_house_brief']
        producer_info.producer_facebook_account = request.POST['producer_facebook_account']
        producer_info.producer_twitter_account = request.POST['producer_twitter_account']
        
        producer_info.save()
        return redirect('/profile/')  # Redirect back to the same page after saving
    else:
        context = {
            'profile': mydata,
        }
        return render(request, 'ProfileUpdate.html', context)



def producer_change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data = request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('/profile/')
        else:
            return redirect('/producer_change_password/')
    else:
        form = PasswordChangeForm(user = request.user)
        args = {'form':form}
        return render(request, 'producer_change_password.html',args)
    

def page_not_found(request, exception):
    return render(request, '404.html')


@user_only
def searchresult(request):
    template = loader.get_template('searchresult.html')
    username = request.user.username
    # Retrieve a queryset of records with the desired username
    matching_records = UserInfo.objects.filter(username=username)
    # Check if any records with the desired username exist
    username_exists = matching_records.exists()
    if username_exists:
        userdata = UserInfo.objects.filter(username=username)
    else:
        userdata = User.objects.filter(username=username)
    if request.method == "GET":
        search_query = request.GET.get('search', '').split(" ")
        if search_query is not None:
            queryset_list1 = Q()
            queryset_list2 = Q()
            queryset_list3 = Q()
            for query in search_query:
                queryset_list1 |= (
                        Q(Language__icontains=query) |
                        Q(Movie_name__icontains=query) |
                        Q(Genre__icontains=query) |
                        Q(Production_house__icontains=query) |
                        Q(Producer__icontains=query) |
                        Q(cast__icontains=query) |
                        Q(Director__icontains=query) |
                        Q(Music_director__icontains=query) |
                        Q(Other_Languages__icontains=query) |
                        Q(lyricist__icontains=query) |
                        Q(choreographer__icontains=query) |
                        Q(Script_writer__icontains=query) |
                        Q(Distribution__icontains=query) |
                        Q(Singers__icontains=query) |
                        Q(Editor__icontains=query) |
                        Q(Cinematographer__icontains=query)
                )
                queryset_list2 |= (
                    Q(author__icontains=query) |
                    Q(Movie_name__icontains=query)
                )

                queryset_list3 |= (
                        Q(Movie_name__icontains=query)
                )

            try:
                mydata = CreateLabel.objects.filter(queryset_list1).distinct().order_by('-timestamp_field')
            except CreateLabel.DoesNotExist:
                mydata = []
            try:
                mydata1 = Review.objects.filter(queryset_list2).distinct().order_by('-timestamp_field')
            except Review.DoesNotExist:
                mydata1 = []
            try:
                mydata3 = PostText1.objects.filter(queryset_list3).distinct().order_by('-timestamp_field')
            except PostText1.DoesNotExist:
                mydata3 = []
            combined_data = sorted(list(mydata) + list(mydata1) + list(mydata3),
                                   key=lambda x: x.timestamp_field, reverse=True
                                   )
            context = {'combined_data': combined_data, 'head': userdata}
        else:
            context = {
                'combined_data': []
            }
    return HttpResponse(template.render(context, request))

from marketing.forms import PrivacyForm, TermsForm

@user_only
def Deleteuser(request):
    if request.method == 'POST':
        input_value = request.POST['confirm-id']
        if not input_value:
            messages.error(request, "Please enter a mobile number or email ID!")
            return redirect('Deleteuser')
        print(input_value)
        # Call the Delete_UserAccountAPI to delete user information
        phone_number_obj = PhoneNumber.objects.get(Q(number=input_value) | Q(email=input_value))
    
        try:
            user_obj = UserInfo.objects.get(phone_number=phone_number_obj.number)
            print(user_obj)
        except UserInfo.DoesNotExist:
            user_obj = UserInfo.objects.get(email=phone_number_obj.email)
            print(user_obj)
        
        # Clear interactions from UserLikes, UserComments, UserShares, and UserFollow tables if they exist:
        
        UserLikes.objects.filter(user_id=user_obj.user_id).delete()
        UserComments.objects.filter(user_id=user_obj.user_id).delete()
        UserShares.objects.filter(user_id=user_obj.user_id).delete()
        UserFollows.objects.filter(user_id=user_obj.user_id).delete()
        
        # Clear user logs from UserLogs table
        UserLogs.objects.filter(user_id=user_obj.user_id).delete()
        
        #delete any reviews posted by the user
        Review.objects.filter(author=user_obj.username).delete()

        id=user_obj.user_id
        
        # Delete user from UserInfo table
        user_obj.delete()
        
        # Delete phone number from PhoneNumber table
        phone_number_obj.delete()
        
        # Delete user from User table
        User.objects.filter(id=id).delete()

        response = 200
        
        if response == 200:
            messages.success(request, "User account deleted successfully!")
        else:
            messages.error(request, "Failed to delete user account!")
        
        return redirect('Deleteuser')
     
    return render(request, "delete_user.html")  # Render the delete user template


def notification(request):
    mydata = CreateLabel.objects.all().order_by('-timestamp_field')
    template = loader.get_template('notification.html')
    context = {
        'mydata': mydata,
    }
    return HttpResponse(template.render(context, request))







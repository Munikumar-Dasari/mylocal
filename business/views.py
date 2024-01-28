from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail
from cinystore import settings
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from cinystoreapp.tokens import generate_token
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from cinystoreapp.models import *
from business.models import *
from podadmin.models import *
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.views import View
import random
import http.client
from django.conf import settings
from django.urls import reverse
from itertools import chain
from operator import attrgetter
from cinystoreapp.models import *
from business.forms import *
from .models import SubmitLabel
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.db.models import Q
import mysql.connector 
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .decorators import producer_only



db = mysql.connector.connect(
  host="3.109.48.139",
  user="myuser",
  password="cinystore",
  database="cinystore"
)
cursor = db.cursor()


def index(request):
    return render(request, 'welcomePage.html')

def producer_check_username(request):
    print('producer check username')
    if request.method == 'GET':
        username = request.GET.get('username')
        try:
            user = User.objects.get(username=username, is_producer=True)
            return JsonResponse({'available': False})
        except User.DoesNotExist:
            return JsonResponse({'available': True})
        
def producer_check_email(request):
    print('producer check email')
    if request.method == 'GET':
        email = request.GET.get('email')
        try:
            user = User.objects.get(email=email, is_producer=True)
            return JsonResponse({'available': False})
        except User.DoesNotExist:
            return JsonResponse({'available': True})

def Registerpage(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if User.objects.filter(email=email).exists():
            if User.objects.get(email=email).is_producer == True:
                messages.error(request, "Email Already Registered!!")
                return redirect('business:Registerpage')

        if len(username) > 20:
            messages.error(request, "Username must be under 20 characters!!")
            return redirect('business:Registerpage')

        if password != confirm_password:
            print('passwords didnt matched')
            messages.error(request, "Passwords didn't matched!!")
            return redirect('business:Registerpage')
            
        myuser = User.objects.create_user(username=username, email=email, password=password)
        myuser.is_producer = True
        myuser.is_active = False
        myuser.save()

        producer = ProducerRegister.objects.create(producer=myuser,
                                                   producer_email = email,
                                                   production_house=username)
        producer.save()
        producer.is_active = False
        producer.is_agency = False
        producer.is_corporate = False
        producer.is_individual = False
        producer.is_ott = False
        producer.save()
        print('user created')
        messages.success(request,
                         "Your Account has been created successfully!! Please check your email to confirm your email address in order to activate your account.")

        # Welcome Email
        subject = "Welcome to Cinystore Login!!"
        message = "Hello " + producer.production_house + "!! \n" + "Welcome to Cinystore!! \nThank you for visiting our website.\n We have also sent you a confirmation email, please confirm your email address. \n\nThanking You\n Cinystore !! \n"


        from_email = settings.EMAIL_HOST_USER
        to_list = [producer.producer_email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)

        uid = urlsafe_base64_encode(force_bytes(producer.pk))
        print(uid)

        token = generate_token.make_token(producer)
        print(token)

        # Email Address Confirmation Email
        current_site = get_current_site(request)
        email_subject = "Confirm your Email @ Cinystore Login!!"
        message2 = render_to_string('producer_email.html', {

            'name': producer.production_house,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(producer.pk)),
            'token': generate_token.make_token(producer)
        })
        # Construct the local file path to the logo image
        logo_path = os.path.join(settings.BASE_DIR, 'cinystoreapp', 'static', 'img', 'logo.webp')

        # Attach the company logo
        with open(logo_path, "rb") as logo_file:
            logo_data = logo_file.read()
            email = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [producer.producer_email])
            email.attach('logo.webp', logo_data, 'image/webp')  # Adjust the content type if needed
            email.send()

        email = EmailMessage(
            email_subject,
            message2,
            settings.EMAIL_HOST_USER,
            [producer.producer_email],
        )
        email.fail_silently = True
        email.send()
        return redirect('/business/producerlogin/')

    return render(request, 'Register.html')


def send_otp(number, otp):
    print("FUNCTION CALLED")
    conn = http.client.HTTPSConnection("api.msg91.com")
    authkey = settings.AUTH_KEY
    headers = { 'content-type': "application/json" }
    senderid = 'cinystore'
    templateid = '6583eebdd6fc0518e471ba43'
    
    url = "https://control.msg91.com/api/v5/otp?template_id="+templateid+"&mobile="+number+"&otp="+otp+"&sender="+senderid+"&authkey="+authkey+"&country=91"
    conn.request("GET", url, headers=headers)
    res = conn.getresponse()
    data = res.read()
    print(data)
    return None

def verify_otp(request):
    print("Verify FUNCTION CALLED")
    conn = http.client.HTTPSConnection("api.msg91.com")
    number = request.session['number']
    otp = request.POST.get('otp')

    url = "https://control.msg91.com/api/v5/otp/verify?otp="+ otp +"mobile="+ number

    headers = {
        "accept": "application/json",
        "authkey": "412276AiWQwTv6v6586caa4P1"
    }

    response = request.get(url, headers=headers)
    print(response.text)
    return None

def otp_page(request):

    template = loader.get_template('otppage.html')
    context = {
        'otp_page': otp_page,
    }
    return HttpResponse(template.render(context, request))

    # number = request.session['number']
    # context = {'number': number}
    # if request.method == 'POST':
    #     otp = request.POST.get('otp')
    #     profile = PhoneNumber.objects.filter(number=number).first()
    #     if otp == profile.otp:
    #         return redirect('select_page')
    #     else:
    #         print('Wrong')
    #         context = {'message': 'Wrong OTP', 'class': 'danger', 'number': number}
    #         return render(request, 'otpPage.html', context)

    # return render(request, 'otpPage.html', context)

# def verify_otp(request):

#the register form takes the phonenumber and sends the otp to the user and this happens inside the register form
#the user enters the otp and then the otp is verified here




def activateaccount(request, uid64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uid64))
        producer = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        producer = None

    if producer is not None and generate_token.check_token(producer, token):
        producer.is_active = True
        producer.save()
        
        my_producer = ProducerRegister.objects.get(producer=producer)
        my_producer.is_active = True
        
        login(request,producer)
        messages.success(request, "Your Account has been activated!!")
        return redirect('/business/producerlogin')
    else:
        return HttpResponse("Activation link is invalid!, Get in contact with the customer Support Team.")
    

def producerlogin(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        #check if user exists
        if User.objects.filter(email=email).exists():
            username = User.objects.get(email=email).username
            user = authenticate(request, username = username, password=password)
            if user is not None:
                print('user logged in')
                login(request, user)
                producer_info = ProducerRegister.objects.get(producer = user)
                production_house = producer_info.production_house
                if producer_info.is_agency == True:
                    return redirect(f'/business/producer_content/{production_house}/')
                elif producer_info.is_corporate == True:
                    return redirect(f'/business/producer_content/{production_house}/')
                elif producer_info.is_individual == True:
                    return redirect(f'/business/producer_content/{production_house}/')
                elif producer_info.is_ott == True:
                    return redirect(f'/business/producer_content/{production_house}/')
                else:
                    return redirect('/business/segment/')
        else:
            print('user not logged in')
            messages.error(request, "Email ID Not Registered!!")
            return redirect('business:producerlogin')
        
        messages.error(request, "Invalid Credentials!!")
        return redirect('business:producerlogin')
        
    return render(request, 'producerlogin.html')


def business(request):
    if request.method == 'POST':
        username = request.POST['production_house']
        producer_password = request.POST['producer_password']
        try:
            users = User.objects.get(Q(username=username) | Q(email=username))
            myproducer = authenticate(request, username = users, password=producer_password)
        except:
            messages.error(request, "User Does not exist, Please Register")
            return redirect('business')
        if myproducer is not None:
            login(request, myproducer)
            producer_info = ProducerRegister.objects.get(producer = myproducer)
            producer_first_name = producer_info.producer_first_name
            return redirect(f'/producerdashboard/{producer_info.production_house}/')
        else:
            messages.error(request, "Invalid Credentials!!")
            return redirect('business')
    return render(request, "business.html")

@producer_only
def segment(request):
    if request.method == 'POST':
        first_name = request.POST['first-name']
        last_name = request.POST['last-name']
        production_house = request.POST['production-name']
        website = request.POST['website']
        country_name = request.POST['country']
        state = request.POST['state']
        city = request.POST['city']
        company_brief = request.POST['about-production']
        phone_number = request.POST['phone-number']
        selection = request.POST['selection']

        print(request.user)

        user = User.objects.get(username=request.user)

        producer = ProducerRegister.objects.get(producer=request.user)
        producer.producer_first_name = first_name
        producer.producer_last_name = last_name
        producer.production_house = production_house
        producer.producer_website = website
        producer.producer_country_name = country_name
        producer.producer_state = state
        producer.producer_city = city
        producer.production_house_brief = company_brief
        producer.producer_phone_number = int(phone_number)
        producer.save()
        print(type(phone_number))
        phone_number = phone_number
        

        if selection == 'individual':
            individual_user = IndividualRegister.objects.create(
                producer=user,
                first_name=first_name,
                last_name=last_name,
                production_house=production_house,
                website=website,
                country_name=country_name,
                state=state,
                city=city,
                phone_number=phone_number,
                company_brief=company_brief,
                is_active=True  # Set to True by default, you can modify this based on your requirements
            )
            individual_user.save()
            producer.is_individual = True
            producer.save()
            return redirect(f'/business/producer_content/{producer.production_house}')
        elif selection == 'corporate':
            corporate_user = CorporateRegister.objects.create(
                producer=user,
                first_name=first_name,
                last_name=last_name,
                production_house=production_house,
                website=website,
                country_name=country_name,
                state=state,
                city=city,
                phone_number=phone_number,
                company_brief=company_brief,
                is_active=True  # Set to True by default, you can modify this based on your requirements
            )
            corporate_user.save()
            producer.is_corporate = True
            producer.save()
            return redirect(f'/business/producer_content/{producer.production_house}')
        elif selection == 'ott':

            ott_user = OttRegister.objects.create(
                producer=user,
                first_name=first_name,
                last_name=last_name,
                production_house=production_house,
                website=website,
                country_name=country_name,
                state=state,
                city=city,
                company_brief=company_brief,
                phone_numebr= phone_number,
                is_active=True  # Set to True by default, you can modify this based on your requirements
            )
            ott_user.save()
            producer.is_ott = True
            producer.save()
            return redirect(f'/business/producer_content/{producer.production_house}')
        elif selection == 'agency':
            agency_user = AgencyRegister.objects.create(
                producer=user,
                first_name=first_name,
                last_name=last_name,
                production_house=production_house,
                website=website,
                country_name=country_name,
                state=state,
                city=city,
                company_brief=company_brief,
                phone_numebr=phone_number,
                is_active=True  # Set to True by default, you can modify this based on your requirements
            )
            agency_user.save()
            producer.is_agency = True
            producer.save()
            return redirect(f'/business/producer_content/{producer.production_house}')
    return render(request, 'segment.html')


        
def producer_activation_success(request):
    return render(request, 'producer_activation_success.html')

@producer_only
def Producerlogout(request):
    logout(request)
    # messages.success(request, "Logged Out Successfully!!")
    return redirect('/business')



def welcome_page(request):
    template = loader.get_template('welcomePage.html')
    context = {
        'welcome_page': welcome_page,
    }
    return HttpResponse(template.render(context, request))


def businessBase(request):
    template = loader.get_template('businessBase.html')
    context = {
        'businessBase': businessBase,
    }
    return HttpResponse(template.render(context, request))


def corporateBase(request):
    template = loader.get_template('corporateBase.html')
    context = {
        'corporateBase': corporateBase,
    }
    return HttpResponse(template.render(context, request))

@producer_only
def producer_account(request):
    # Retrieve a queryset of records with the desired production_house
    matching_records = ProducerRegister.objects.filter(producer=request.user)
    # Check if any records with the desired production_house exist
    username_exists = matching_records.exists()

    
    if username_exists:
        userdata = matching_records
    else:
        # Handle the case where no matching records are found
        userdata = None

    template = loader.get_template('producer_account.html')
    context = {
        
        'producer_account': userdata,
        'producer_base': userdata
    }
    return HttpResponse(template.render(context, request))

@producer_only
def producer_change_password(request):
    if request.method == 'POST':
        oldpassword = request.POST['oldPassword']
        password = request.POST['password']
        confirmpassword = request.POST['confirmPassword']
        user = request.user
        #check if the old password is corrct from the stored passwords
        if user.check_password(oldpassword):
            #check if the new password and confirm password are same
            if password == confirmpassword:
                user.set_password(password)
                user.save()
                update_session_auth_hash(request, user)
                messages.success(request, "Password Changed Successfully!!")
                return redirect('business:producer_account')
            else:
                messages.error(request, "New Password and Confirm Password didn't matched!!")
                return redirect('business:producer_account')
        else:
            messages.error(request, "Old Password is incorrect!!")
            return redirect('business:producer_account')

@producer_only
def edit_producer_account(request):
    # Retrieve a queryset of records with the desired production_house
    matching_records = ProducerRegister.objects.filter(producer=request.user)
     # Check if any records with the desired username exist 
    producer_exists = matching_records.exists()

    if producer_exists:
        userdata = ProducerRegister.objects.filter(production_house = request.user)
    template = loader.get_template('producer_account.html')

    # the data needs to be edited in the modal form
    if request.method == 'POST':
        producer_account, created = ProducerRegister.objects.get_or_create(production_house=request.user)
        try:
            if request.FILES.get('profileImage'):
                print(request.FILES.get('profileImage'))
                print('image')
                producer_account.production_house_image = request.FILES.get('profileImage')
                producer_account.save()
            else:
                print('no image')
                value = ProducerRegister.get('production_house_image', 'null')
                producer_account.production_house_image = value 
        except:
            pass
        producer_account, created = ProducerRegister.objects.get_or_create(producer=request.user)
        producer_account.production_house = request.POST['production_house']
        producer_account.producer_first_name = request.POST['producer_first_name']
        producer_account.producer_last_name = request.POST['producer_last_name']
        producer_account.producer_email = request.POST['producer_email']
        producer_account.producer_phone_number = request.POST['producer_phone_number']
        producer_account.producer_website = request.POST['producer_website']
        producer_account.producer_country_name = request.POST['producer_country_name']
        producer_account.producer_state = request.POST['producer_state']
        producer_account.producer_city = request.POST['producer_city']
        producer_account.production_house_brief = request.POST['production_house_brief']
        producer_account.producer_facebook_account = request.POST['producer_facebook_account']
        producer_account.producer_twitter_account = request.POST['producer_twitter_account']
        producer_account.save()

        Useraccount, created = User.objects.get_or_create(username=request.user)
        Useraccount.username = request.POST['production_house']
        Useraccount.first_name = request.POST['producer_first_name']
        Useraccount.last_name = request.POST['producer_last_name']
        Useraccount.email = request.POST['producer_email']
        Useraccount.save()

        if producer_account.is_agency == True:
            agency = AgencyRegister.objects.get(producer=request.user)
            agency.username = request.POST['production_house']
            agency.first_name = request.POST['producer_first_name']
            agency.last_name = request.POST['producer_last_name']
            agency.email = request.POST['producer_email']
            agency.production_house = request.POST['production_house']
            agency.website = request.POST['producer_website']
            agency.country_name = request.POST['producer_country_name']
            agency.state = request.POST['producer_state']
            agency.city = request.POST['producer_city']
            agency.company_brief = request.POST['production_house_brief']
            agency.phone_number = request.POST['producer_phone_number']
            agency.facebook_account = request.POST['producer_facebook_account']
            agency.twitter_account = request.POST['producer_twitter_account']
            agency.save()

        elif producer_account.is_corporate == True:
            corporate = CorporateRegister.objects.get(producer=request.user)
            corporate.username = request.POST['production_house']
            corporate.first_name = request.POST['producer_first_name']
            corporate.last_name = request.POST['producer_last_name']
            corporate.email = request.POST['producer_email']
            corporate.production_house = request.POST['production_house']
            corporate.website = request.POST['producer_website']
            corporate.country_name = request.POST['producer_country_name']
            corporate.state = request.POST['producer_state']
            corporate.city = request.POST['producer_city']
            corporate.company_brief = request.POST['production_house_brief']
            corporate.phone_number = request.POST['producer_phone_number']
            corporate.facebook_account = request.POST['producer_facebook_account']
            corporate.twitter_account = request.POST['producer_twitter_account']
            corporate.save()

        elif producer_account.is_individual == True:
            individual = IndividualRegister.objects.get(producer=request.user)
            individual.username = request.POST['production_house']
            individual.first_name = request.POST['producer_first_name']
            individual.last_name = request.POST['producer_last_name']
            individual.email = request.POST['producer_email']
            individual.production_house = request.POST['production_house']
            individual.website = request.POST['producer_website']
            individual.country_name = request.POST['producer_country_name']
            individual.state = request.POST['producer_state']
            individual.city = request.POST['producer_city']
            individual.company_brief = request.POST['production_house_brief']
            individual.phone_number = request.POST['producer_phone_number']
            individual.facebook_account = request.POST['producer_facebook_account']
            individual.twitter_account = request.POST['producer_twitter_account']
            individual.save()

        elif producer_account.is_ott == True:
            ott = OttRegister.objects.get(producer=request.user)
            ott.username = request.POST['production_house']
            ott.first_name = request.POST['producer_first_name']
            ott.last_name = request.POST['producer_last_name']
            ott.email = request.POST['producer_email']
            ott.production_house = request.POST['production_house']
            ott.website = request.POST['producer_website']
            ott.country_name = request.POST['producer_country_name']
            ott.state = request.POST['producer_state']
            ott.city = request.POST['producer_city']
            ott.company_brief = request.POST['production_house_brief']
            ott.phone_number = request.POST['producer_phone_number']
            ott.facebook_account = request.POST['producer_facebook_account']
            ott.twitter_account = request.POST['producer_twitter_account']
            ott.save()
        else:
            return redirect('business:producer_account')
        
    context = {
        'producer_base':userdata,
        'producer_account': userdata,
    }

    return HttpResponse(template.render(context, request))


@producer_only
def producer_add_post(request, Movie_name):
    
    '''
    This code is to get user Information and pass it in "head.html as dictionary {'producer_base': userdata}
    
    '''
    production_house = request.user.username
    # Retrieve a queryset of records with the desired username
    matching_records = ProducerRegister.objects.filter(production_house=production_house)
    # Check if any records with the desired username exist
    username_exists = matching_records.exists()

    if username_exists:
        userdata = ProducerRegister.objects.filter(production_house=production_house)
    
    ## user information storing ends here 

    template = loader.get_template('producer_add_post.html')
    mydata = CreateLabel.objects.filter(Movie_name=Movie_name)
    context = {
        'producer_add_post': producer_add_post,
        'producer_base': userdata,
        'mydata': mydata,
    }
    if request.method == 'POST':
        form = SubmitPostForm(request.POST, request.FILES)
        production_house_name = request.user
        print('production house name', production_house_name)
        producer = ProducerRegister.objects.get(production_house=production_house_name)
        production_house = ProducerRegister.objects.get(production_house=production_house_name).production_house
        producer_logo = ProducerRegister.objects.get(production_house=production_house_name).production_house_image
        # list of movies produced by the production house
        movies = CreateLabel.objects.filter(producer_id=producer)
        movie_list = [movie.Movie_name for movie in movies]    
        print(movie_list, 'movie names', production_house_name, 'production house name')

        # if the movie name is not in the list of movies produced by the production house
        # then return an error message and if the movie name is in the list of movies produced by the production house
        # then save the form and update the production house name
        if form.is_valid():
            Movie_name = form.cleaned_data['Movie_name']
            # Check if the movie exists in CreateLabel database
            if CreateLabel.objects.filter(Movie_name=Movie_name).exists() and Movie_name in movie_list:
                form.save()  # Save the post if the movie exists
                SubmitPost.objects.filter(Movie_name = Movie_name).update(source=production_house)
                SubmitPost.objects.filter(Movie_name = Movie_name).update(logo=producer_logo)
                SubmitPost.objects.filter(Movie_name = Movie_name).update(slug = ''.join(Movie_name.split(' ')))
                return redirect(f'/business/producer_content/{production_house}')  # Redirect to a success view
            elif Movie_name not in movie_list:
                messages.error(request, "You have not produced this movie!!")
                print('error occured while posting text')
                return redirect(f'/business/producer_content/{producer.production_house}/')
            else:
                messages.error(request, "Create A Label For The Movie To Post!")
                return render(request, 'producer_add_post.html', {'form': form, 'message': messages.error})
            
    return HttpResponse(template.render(context, request))


@producer_only
def producer_add_clips(request, Movie_name):
    
    '''
    This code is to get user Information and pass it in "head.html as dictionary {'producer_base': userdata}
    
    '''
    production_house = request.user.username
    # Retrieve a queryset of records with the desired username
    matching_records = ProducerRegister.objects.filter(production_house=production_house)
    # Check if any records with the desired username exist
    username_exists = matching_records.exists()

    if username_exists:
        userdata = ProducerRegister.objects.filter(production_house=production_house)
    
    template = loader.get_template('producer_add_clips.html')
    mydata = CreateLabel.objects.filter(Movie_name=Movie_name)
    context = {
        'producer_add_clips': producer_add_clips,
        'producer_base': userdata,
        'mydata': mydata,
    }
    if request.method == 'POST' and request.FILES:
        form = VideoClipsForm(request.POST, request.FILES)
        production_house_name = request.user
        print('production house name', production_house_name)
        producer = ProducerRegister.objects.get(production_house=production_house_name)
        production_house = ProducerRegister.objects.get(production_house=production_house_name).production_house
        producer_logo = ProducerRegister.objects.get(production_house=production_house_name).production_house_image
        # list of movies produced by the production house
        movies = CreateLabel.objects.filter(producer_id=producer)
        movie_list = [movie.Movie_name for movie in movies] 
        print(movie_list, 'movie names')
        if form.is_valid():
            print('form is valid')
            Movie_name = form.cleaned_data['Movie_name']
            print(Movie_name, 'movie name')
            # Check if the movie exists in CreateLabel database
            if CreateLabel.objects.filter(Movie_name=Movie_name).exists() and Movie_name in movie_list:
                print('movie exists')
                form.save()  # Save the post if the movie exists
                SubmitClips.objects.filter(Movie_name = Movie_name).update(source=production_house)
                SubmitClips.objects.filter(Movie_name = Movie_name).update(logo=producer_logo)
                SubmitClips.objects.filter(Movie_name = Movie_name).update(slug = ''.join(Movie_name.split(' ')))
                return redirect(f'/business/producer_content/{production_house}')  # Redirect to a success view
            elif Movie_name not in movie_list:
                messages.error(request, "You have not produced this movie!!")
                print('error occured while posting text')
                return redirect(f'producer_add_clips/{Movie_name}/')
            else:
                print('movie does not exist')
                messages.error(request, "Create A Label For The Movie To Post!")
                return render(request, 'producer_add_clips.html', {'form': form, 'message': messages.error})
        else:
            print('form is not valid')
            return render(request, 'producer_add_clips.html', {'form': form, 'message': messages.error})
    return HttpResponse(template.render(context, request))


def producer_base(request):
    mydata = ProducerRegister.objects.all()
    template = loader.get_template('producer_base.html')
    context = {
        'producer_base': mydata,
        
    }
    return HttpResponse(template.render(context, request))

def corporateHome(request):
    template = loader.get_template('corporateHome.html')
    context = {
        'corporateHome': corporateHome,
    }
    return HttpResponse(template.render(context, request))


@producer_only
def producer_submitlabel(request):
    production_house = request.user.username
    # Retrieve a queryset of records with the desired username
    matching_records = ProducerRegister.objects.filter(production_house=production_house)
    # Check if any records with the desired username exist
    username_exists = matching_records.exists()

    if username_exists:
        userdata = ProducerRegister.objects.filter(production_house=production_house)

    context = {
        'producer_base': userdata,
        }
    
    ## user information storing ends here 
    if request.method == 'POST':
        producer_name = request.user
        producer = ProducerRegister.objects.get(production_house=producer_name)
        production_house = ProducerRegister.objects.get(production_house=producer_name).production_house
        producer_logo = ProducerRegister.objects.get(production_house=producer_name).production_house_image

        if User.objects.filter(username=producer_name).exists():
            form = Submitform(request.POST, request.FILES)    
            producer = ProducerRegister.objects.get(production_house=producer_name).producer_id
            #if the movie already exists in the database then return an error message else save the form and update the producer_id, source and logo
            #if the releae date is less than the current date then return an error message else save the form and update the producer_id, source and logo

            if request.POST['Release_date'] < str(datetime.today()):
                messages.error(request, "Release Date should be greater than the current date!!")
                return render(request, 'producer_submitlabel.html', {'form': form, 'producer_base': userdata})

            if CreateLabel.objects.filter(Movie_name=request.POST['Movie_name']).exists():
                messages.error(request, "Movie Already Exists!!")
                return render(request, 'producer_submitlabel.html', {'form': form, 'message': messages.error})
            else:
                if form.is_valid():
                    form.save()
                    Movie_name=form.cleaned_data['Movie_name']
                    SubmitLabel.objects.filter(Movie_name = Movie_name).update(producer_id=producer)
                    SubmitLabel.objects.filter(Movie_name = Movie_name).update(source=production_house)
                    SubmitLabel.objects.filter(Movie_name = Movie_name).update(logo=producer_logo)
                    
                    return redirect('business:producer_content', production_house=production_house)
                else:
                    return render(request, 'producer_submitlabel.html', {'form': form, 'producer_base': userdata})
    else:
        form = Submitform()
        # return HttpResponse('form page shown')
        return render(request, 'producer_submitlabel.html', {'form': form})
    
    return render(request, 'producer_submitlabel.html', context)

def check_movie_exists(request):
    if request.method == 'GET':
        movie_name = request.GET.get('Movie_name')
        try:
            movie = CreateLabel.objects.get(Movie_name=movie_name)
            return JsonResponse({'available': False})
        except CreateLabel.DoesNotExist:
            return JsonResponse({'available': True})
 
@producer_only
def producer_content(request, production_house):
    
    production_house = request.user.username
    # Retrieve a queryset of records with the desired username
    matching_records = ProducerRegister.objects.filter(production_house=production_house)
    # Check if any records with the desired username exist
    username_exists = matching_records.exists()

    if username_exists:
        userdata = ProducerRegister.objects.filter(production_house=production_house)
    
    ## user information storing ends here 
	

    production_house = request.user
    template = loader.get_template('producer_content.html')
    producer = ProducerRegister.objects.get(production_house=production_house)
    mydata = CreateLabel.objects.filter(producer_id=producer)
    edit_label = CreateLabel.objects.filter(producer_id=producer)
    # print(mydata,'mydata')
    mydata1 = PostText1.objects.filter(source=production_house)
    mydata2 = Clips.objects.filter(source=production_house)
    movie_list = [movie.Movie_name for movie in mydata]    
    # print(movie_list, 'movie names', production_house, 'production house name')
    Movie_label = CreateLabel.objects.filter(Movie_name__in=movie_list)
    # print(Movie_label)
    #labels = CreateLabel.objects.filter(Movie_name=production_house.Movie_name)
    all_data = list(chain(mydata, mydata1, mydata2))
    all_data.sort(key=attrgetter('timestamp_field'), reverse=True)

    
    context = {
        'producer_content': all_data,
        'producerdashboard':mydata,
        'Posts':mydata1,
        'Clips':mydata2,
        'producer_base': userdata,
        'Movie_label': Movie_label,
        'edit_label': edit_label
   
    }
    return HttpResponse(template.render(context, request))
 


@producer_only
def producer_content_with_movie(request, production_house, Movie_name):
    '''
    This code is to get user Information and pass it in "head.html as dictionary {'producer_base': userdata}
    '''
    # Retrieve a queryset of records with the desired production house
    matching_records = ProducerRegister.objects.filter(production_house=production_house)
    # Check if any records with the desired production house exist
    username_exists = matching_records.exists()

    if username_exists:
        userdata = matching_records
    else:
        # Handle the case where no matching records are found
        userdata = None

    template = loader.get_template('producer_content.html')
    producer = ProducerRegister.objects.get(production_house=production_house)
    mydata = CreateLabel.objects.filter(producer_id=producer, Movie_name=Movie_name)
    mydata1 = PostText1.objects.filter(source=production_house)
    mydata2 = Clips.objects.filter(source=production_house)

    context = {
        'producerdashboard': mydata,
        'Posts': mydata1,
        'Clips': mydata2,
        'producer_base': userdata,
    }
    return HttpResponse(template.render(context, request))


@producer_only
def edit_label(request, Movie_name):
    production_house =request.user
    print(Movie_name)

    matching_records = CreateLabel.objects.filter(Movie_name = Movie_name)
    # Check if any records with the desired username exist 
    movie_exists = matching_records.exists()
    if movie_exists:
        mydata = CreateLabel.objects.filter(Movie_name = Movie_name)
    
       
    if request.method == 'POST':
        producer_createlabel, created = CreateLabel.objects.get_or_create(Movie_name=Movie_name)
    
        producer_createlabel.Movie_name = request.POST['Movie_name']		
        producer_createlabel.Language = request.POST['Language']
        producer_createlabel.Genre = request.POST['Genre']
        producer_createlabel.cast = request.POST['cast']
        producer_createlabel.Production_house = request.POST['Production_house']
        producer_createlabel.Producer = request.POST['Producer']
        producer_createlabel.Director = request.POST['Director']
        producer_createlabel.Music_director = request.POST['Music_director']
        #producer_createlabel.Poster = request.POST['Poster']
        try:
            if request.FILES.get('Poster'):
                producer_createlabel.Poster = request.FILES.get('Poster')
            else:
                value = CreateLabel.get('Poster', 'null')
                producer_createlabel.Poster = value 
        except:
            pass
        
        try:
            if request.POST['Release_date'] == "":
                value = CreateLabel.get('Release_date', None)
                producer_createlabel.Release_date = value 
            else:
                producer_createlabel.Release_date =  request.POST['Release_date']
        except:
            pass				
        producer_createlabel.synopsis = request.POST['synopsis']
        producer_createlabel.trailer = request.POST['trailer']
        #producer_createlabel.Banner = request.POST['Banner']
        try:
            if request.FILES.get('Banner'):
                producer_createlabel.Banner = request.FILES.get('Banner')
            else:
                value = CreateLabel.get('Banner', 'null')
                producer_createlabel.Banner = value 
        except:
            pass

        producer_createlabel.Url_name = request.POST['Url_name']
        producer_createlabel.Other_Languages = request.POST['Other_Languages']
        producer_createlabel.lyricist = request.POST['lyricist']
        producer_createlabel.choreographer = request.POST['choreographer']
        producer_createlabel.Script_writer = request.POST['Script_writer']					
        producer_createlabel.Running_Time = request.POST['Running_Time']
        producer_createlabel.Maturity = request.POST['Maturity']
        producer_createlabel.Budget = request.POST['Budget']
        producer_createlabel.Distribution = request.POST['Distribution']
        producer_createlabel.Recording_studio = request.POST['Recording_studio']
        producer_createlabel.Graphic_designer = request.POST['Graphic_designer']
        producer_createlabel.Singers = request.POST['Singers']
        producer_createlabel.Editor	= request.POST['Editor']
        producer_createlabel.Cinematographer = request.POST['Cinematographer']	
        producer_createlabel.save()

        return redirect(f'/business/producer_content/{production_house}')  # Redirect back to the same page after saving
    else:
        context = {
            'edit_label': mydata,
        }
        return render(request, 'producer_content.html', context)
    

@producer_only
def edit_post(request, id):
    
    # producer = request.user
    # # Retrieve a queryset of records with the desired username
    matching_records = PostText1.objects.filter(id = id)
    # Check if any records with the desired username exist 
    movie_exists = matching_records.exists()
    if movie_exists:
        mydata = PostText1.objects.filter(id = id)
        
    if request.method == 'POST':
        producer_post, created = PostText1.objects.get_or_create(id=id)
        producer_post.Movie_name = request.POST['Movie_name']		
        producer_post.Language = request.POST['Language']
        producer_post.Genre = request.POST['Genre']
        producer_post.Heading = request.POST['Heading']
        producer_post.text = request.POST['text']
        try:
            if request.FILES.get('Image'):
                producer_post.Image = request.FILES.get('Image')
            else:
                value = PostText1.get('Image', 'null')
                producer_post.Image = value 
        except:
            pass
        producer_post.save()
        return redirect('producerdashboard')  # Redirect back to the same page after saving
    else:
        context = {
            'edit_post': mydata,
        }
        return render(request, 'producer_content.html', context)

@producer_only
def edit_clip(request, id):
    
    # producer = request.user
    # # Retrieve a queryset of records with the desired username
    matching_records = Clips.objects.filter(id = id)
    # Check if any records with the desired username exist 
    movie_exists = matching_records.exists()
    if movie_exists:
        mydata = Clips.objects.filter(id = id)
        
    if request.method == 'POST':
        producer_clip, created = Clips.objects.get_or_create(id=id)
        producer_clip.Movie_name = request.POST['Movie_name']		
        producer_clip.Language = request.POST['Language']
        producer_clip.Genre = request.POST['Genre']
        producer_clip.Heading = request.POST['Heading']
        producer_clip.text = request.POST['text']
        try:
            if request.FILES.get('Image'):
                producer_clip.Image = request.FILES.get('Image')
            else:
                value = Clips.get('Image', 'null')
                producer_clip.Image = value 
        except:
            pass
        try:
            if request.FILES.get('Video'):
                producer_clip.Video = request.FILES.get('Video')
            else:
                value = Clips.get('Video', 'null')
                producer_clip.Video = value 
        except:
            pass

        producer_clip.save()
        return redirect('producerdashboard')  # Redirect back to the same page after saving
    else:
        context = {
            'edit_clip': mydata,
        }
        return render(request, 'producer_content.html', context)
    
    
@producer_only
def producer_statistics(request, Movie_name):
    '''
    This code is to get user Information and pass it in "head.html as dictionary {'producer_base': userdata}
    
    '''
    production_house = request.user.username
    # Retrieve a queryset of records with the desired username
    matching_records = ProducerRegister.objects.filter(production_house=production_house)
    # Check if any records with the desired username exist
    username_exists = matching_records.exists()

    if username_exists:
        userdata = ProducerRegister.objects.filter(production_house=production_house)
    
    ## user information storing ends here 
    posts = PostText1.objects.filter(Movie_name=Movie_name)

    # Count all the likes for the filtered posts
    total_likes = posts.aggregate(Sum('like_count'))['like_count__sum'] or 0

    # Count all the follows for the filtered posts
    total_follows = posts.aggregate(Sum('follow_count'))['follow_count__sum'] or 0

    
    # Count all the share for the filtered posts
    total_shares = posts.aggregate(Sum('share_count'))['share_count__sum'] or 0


    # Count all the comment for the filtered posts
    total_comments = posts.aggregate(Sum('comment_count'))['comment_count__sum'] or 0
    
    mydata = CreateLabel.objects.filter(Movie_name=Movie_name)
    mydata1 = Clips.objects.filter(Movie_name=Movie_name).order_by('-like_count')
    mydata3 = PostText1.objects.filter(Movie_name=Movie_name).order_by('-like_count')
    all_data = list(chain(mydata, mydata1, mydata3))
    all_data.sort(key=attrgetter('timestamp_field'), reverse=True)
    template = loader.get_template('producer_statistics.html')
    context = {
        'producer_statistics': all_data,
        'label': mydata,
        'total_likes':total_likes,
        'total_follows':total_follows,
        'total_shares': total_shares,
        'total_comments': total_comments,
        'posts':mydata3,
        'producer_base': userdata,
        'clips': mydata1,
    }
    return HttpResponse(template.render(context, request))

@producer_only
def delete_label(request, Movie_name):
    label = get_object_or_404(CreateLabel, Movie_name=Movie_name)

    if request.method == 'POST':
        label.delete()
        messages.success(request, "Label Deleted Successfully!!")
        #return JsonResponse({'message': f'Movie with name {Movie_name} deleted successfully.'})

    return render(request, 'producer_content.html', {'movie': label})

@producer_only
def delete_post(request, post_id):
    post = get_object_or_404(PostText1, id=post_id)
    if request.method == 'POST':
        post.delete()
        messages.success(request, "Post Deleted Successfully!!")
        #return JsonResponse({'message': f'Post with id {post_id} deleted successfully.'})

    return render(request, 'producer_content.html', {'post': post})

@producer_only
def delete_clip(request, clip_id):
    clip = get_object_or_404(Clips, id=clip_id)
    if request.method == 'POST':
        clip.delete()
        messages.success(request, "Clip Deleted Successfully!!")
        #return JsonResponse({'message': f'Clip with id {clip_id} deleted successfully.'})
    return render(request, 'producer_content.html', {'clip': clip})


def PostTextView(request):
    mydata = PostText1.objects.all()
    template = loader.get_template('PostTextView.html')
    context = {
        'PostTextView': mydata,
    }
    return HttpResponse(template.render(context, request))


@producer_only
def webseries_label(request):
    if request.method == 'POST':
        producer_name = request.user
        if User.objects.filter(username=producer_name).exists():
            form = WebseriesForm(request.POST, request.FILES)
            producer = ProducerRegister.objects.get(production_house=producer_name)
            if form.is_valid():
                form.save()
                webseries_name=form.cleaned_data['webseries_name']
                WebSeriesLabel.objects.filter(webseries_name= webseries_name).update(producer_id=producer)
                WebSeriesLabel.objects.filter(webseries_name = webseries_name).update(slug = ''.join(webseries_name.split(' ')))
                return redirect('producerdashboard')
            else:
                img_obj = form.instance
                return render(request, 'WebSeries.html', {'form': form, 'img_obj': img_obj})
    else:
        form = WebseriesForm()
    return render(request, 'WebSeries.html', {'form': form})



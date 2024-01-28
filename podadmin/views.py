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
from django.contrib.auth import authenticate, login, logout
from django.views import View
import random
import http.client
from django.conf import settings
import mysql.connector
from .models import *
from itertools import chain
from operator import attrgetter
from .decorators import podadmin_only
from django.db.models import Q
from cinystoreapp.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import update_session_auth_hash



db = mysql.connector.connect(
  host="3.109.48.139",
  user="myuser",
  password="cinystore",
  database="cinystore"
)
cursor = db.cursor()



def index(request):
    return render(request, 'login.html')


def admin_account(request):
    # Retrieve a queryset of records with the desired production_house
    matching_records = PodAdmin.objects.filter(pod_name=request.user)
    # Check if any records with the desired production_house exist
    username_exists = matching_records.exists()
    if username_exists:
        userdata = matching_records
    else:
        # Handle the case where no matching records are found
        userdata = None

    template = loader.get_template('admin_account.html')
    context = {
        'admin_account': userdata,
    }
    return HttpResponse(template.render(context, request))


def admin_add_clips(request):
    template = loader.get_template('admin_add_clips.html')
    context = {
        'admin_add_clips': admin_add_clips,
    }
    return HttpResponse(template.render(context, request))


def admin_add_post(request):
    template = loader.get_template('admin_add_post.html')
    context = {
        'admin_add_post': admin_add_post,
    }
    return HttpResponse(template.render(context, request))


def admin_base(request):
    mydata = PodAdmin.objects.all()
    template = loader.get_template('admin_base.html')
    context = {
        'PodAdmin': mydata,
        
    }
    return HttpResponse(template.render(context, request))
    return render(request, 'admin_base.html')



def admin_statistics(request, Movie_name):
    template = loader.get_template('admin_statistics.html')
    context = {
        'admin_statistics': admin_statistics,
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


def podlogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print(username, password)
        if User.objects.filter(username=username).exists():
            user_obj = User.objects.get(Q(username=username)|Q(email=username))
            if user_obj.is_podadmin:
                print('admin')
                authenticated_user = authenticate(username = user_obj.username, password=password)
                if authenticated_user is not None:
                    print('authenticated_user', authenticated_user)
                    login(request, authenticated_user)
                    return redirect(f'/podadmin/admin_content/{username}')
                else:
                    print('not authenticated_user')
                    messages.info(request, 'Username or Password is incorrect')
                    return redirect('podadmin:podlogin')
            else:
                print('not admin')
                messages.info(request, 'You are not an admin')
                return redirect('podadmin:podlogin')
        else:
            messages.info(request, 'The Account is not registered')
            return redirect('podadmin:podlogin')
    else:
        return render(request, 'login.html')




def registerPage(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password =request.POST['confirm_password']
        print(username, email, password)

        if User.objects.filter(username=username):
            print('Username Taken')
            messages.error(request, 'Username Taken')
            return redirect('poddmin:registerPage')
        
        if User.objects.filter(email=email).exists():
            print('Email Taken')
            if email == 'admin@cinystore.com':
                pass
            else:
                messages.error(request, 'Email Taken')
                return redirect('podadmin:registerPage')
        
        if password != confirm_password:
            print('Password not matching')
            messages.error(request, 'Password not matching')
            return redirect('podadmin:registerPage')

        print('criteria passed')
        # create a user for pod admin with the values received from the form
        # hash the password and save the user
        password = make_password(password)
        user = User.objects.create(username=username, email=email, password=password)
        user.is_podadmin = True
        user.is_active = False
        user.save()
        print('user created')
        my_admin = PodAdmin.objects.create(pod=user, pod_name=username, pod_email=email)
        my_admin.pod_is_active = False
        my_admin.save()
        print('admin added')

        messages.success(request,
                         "Your Account has been created successfully!! Please check your email to confirm your email address in order to activate your account.")

        # Welcome Email
        subject = "Welcome to Cinystore Login!!"
        message = "Hello " + my_admin.pod_name + "!! \n" + "Welcome to Cinystore!! \nThank you for visiting our website.\n We have also sent you a confirmation email, please confirm your email address. \n\nThanking You\n Cinystore !! \n"


        from_email = settings.EMAIL_HOST_USER
        to_list = [my_admin.pod_email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)

        uid = urlsafe_base64_encode(force_bytes(my_admin.pk))
        print(uid)

        token = generate_token.make_token(my_admin)
        print(token)

        # Email Address Confirmation Email
        current_site = get_current_site(request)
        email_subject = "Confirm your Email @ Cinystore Login!!"
        message2 = render_to_string('email_confirmation_pod.html', {

            'name': my_admin.pod_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(my_admin.pk)),
            'token': generate_token.make_token(my_admin)
        })
        # Construct the local file path to the logo image
        logo_path = os.path.join(settings.BASE_DIR, 'cinystoreapp', 'static', 'img', 'logo.webp')

        # Attach the company logo
        with open(logo_path, "rb") as logo_file:
            logo_data = logo_file.read()
            email = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [my_admin.pod_email])
            email.attach('logo.webp', logo_data, 'image/webp')  # Adjust the content type if needed
            email.send()

        email = EmailMessage(
            email_subject,
            message2,
            settings.EMAIL_HOST_USER,
            [my_admin.pod_email],
        )
        email.fail_silently = True
        email.send()
        messages.success(request,
                         "Your Account has been created successfully!! Please check your email to confirm your email address in order to activate your account.")
        return redirect('/podadmin/login/')
    else:
        return render(request, 'registerPage.html')
    
def activatePOD(request, uid64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uid64))
        admin = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        admin = None

    if admin is not None and generate_token.check_token(admin, token):
        admin.is_active = True
        admin.save()
        
        my_admin = PodAdmin.objects.get(pod=admin)
        my_admin.pod_is_active = True
        my_admin.save()
        
        login(request,admin)
        messages.success(request, "Your Account has been activated!!")
        return redirect('podadmin:podlogin')
    else:
        return render(request, 'activation_failed.html')
    

def PODlogout(request):
    logout(request)
    return redirect('podadmin:podlogin')


@podadmin_only
def admin_content(request, pod_name):

    '''
    This code is to get user Information and pass it in "head.html as dictionary {'producer_base': userdata}
    '''
    Username= request.user.username
    # Retrieve a queryset of records with the desired production house
    matching_records = PodAdmin.objects.filter(pod_name=Username)
    # Check if any records with the desired production house exist
    username_exists = matching_records.exists()

    if username_exists:
        userdata = matching_records
    else:
        # Handle the case where no matching records are found
        userdata = None

    template = loader.get_template('admin_content.html')
    admin = PodAdmin.objects.get(pod_name=Username)
    mydata = SubmitLabel.objects.all()
    mydata1 = SubmitPost.objects.all()
    mydata2 = SubmitClips.objects.all()

    context = {
        'labelcontent': mydata,
        'Posts': mydata1,
        'Clips': mydata2,
        'admin_account': userdata,
    }
    return HttpResponse(template.render(context, request))


@podadmin_only
def podadmin_change_password(request):
    if request.method == 'POST':
        oldpassword = request.POST['oldPassword']
        password = request.POST['password']
        confirmpassword = request.POST['confirmPassword']
        user = request.user
        #check if the user is a podadmin
        if user.is_podadmin:
            #check if the old password is corrct from the stored passwords
            if user.check_password(oldpassword):
                #check if the new password and confirm password are same
                if password == confirmpassword:
                    if password == oldpassword:
                        messages.error(request, "New Password and Old Password are same!!")
                        return redirect('podadmin:admin_account')
                    else:
                        user.set_password(password)
                        user.save()
                        update_session_auth_hash(request, user)
                        messages.success(request, "Password Changed Successfully!!")
                        return redirect('business:admin_account')
                else:
                    messages.error(request, "New Password and Confirm Password didn't matched!!")
                    return redirect('podadmin:admin_account')
            else:
                messages.error(request, "Old Password is incorrect!!")
                return redirect('podadmin:admin_account')
        else:
            messages.error(request, "Some error Occured, contact the Support!!")
            return redirect('podadmin:admin_account')

@podadmin_only
def approve_label(request, Movie_name):
    pod_name = request.user.username
    print('apporved', Movie_name)
    #store values from SubmitLabel to CreateLabel
    data = SubmitLabel.objects.filter(Movie_name__iexact=Movie_name)
    producer = SubmitLabel.objects.get(Movie_name=Movie_name).producer_id
    Producer_id = ProducerRegister.objects.get(producer_id = producer)
    for i in range(len(data)):
        Labels = CreateLabel.objects.create(producer_id = Producer_id,
                             Movie_name = data[i].Movie_name,
                             Language = data[i].Language,
                             Genre = data[i].Genre,
                             Production_house = data[i].Production_house,
                             Producer = data[i].Producer,
                             cast = data[i].cast,
                             Director = data[i].Director,
                             Music_director = data[i].Music_director,
                             Poster = data[i].Poster,
                             Banner = data[i].Banner,
                             Release_date = data[i].Release_date,
                             synopsis = data[i].synopsis,
                             trailer = data[i].trailer,
                             timestamp_field=data[i].timestamp_field,
                             model_type = data[i].model_type,
                             Url_name = data[i].Url_name,
                             Other_Languages = data[i].Other_Languages,
                             lyricist =data[i].lyricist,
                             choreographer = data[i].choreographer,
                             Script_writer = data[i].Script_writer,
                             Running_Time =data[i].Running_Time,
                             Maturity = data[i].Maturity,
                             Budget = data[i].Budget,
                             Distribution = data[i].Distribution,
                             Recording_studio = data[i].Recording_studio,
                             Graphic_designer = data[i].Graphic_designer,
                             Singers = data[i].Singers,
                             Editor = data[i].Editor,
                             Cinematographer = data[i].Cinematographer,
                             source = data[i].source,
                             logo = data[i].logo,
                             )
        Labels.save()
        #delete the record from SubmitLabel
        data[i].delete()
        return redirect(f'/podadmin/admin_content/{pod_name}')


    return render(request, 'admin_content.html')

@podadmin_only
def reject_label(request, Movie_name):
    pod_name = request.user.username
    print('rejected', Movie_name)
    data = SubmitLabel.objects.get(Movie_name__iexact=Movie_name)
    data.status = 'rejected'
    data.save()
    return redirect(f'/podadmin/admin_content/{pod_name}')

@podadmin_only
def approve_post(request, post_id):
    pod_name = request.user.username
    print('approved', post_id)
    data = SubmitPost.objects.filter(id=post_id)
    for i in range(len(data)):
        Posts = PostText1.objects.create(
                             Movie_name = data[i].Movie_name,
                             Language = data[i].Language,
                             Genre = data[i].Genre,
                             Heading = data[i].Heading,
                             text = data[i].text,
                             Image = data[i].Image,
                             timestamp_field=data[i].timestamp_field,
                             model_type = data[i].model_type,
                             source = data[i].source,
                             logo = data[i].logo,
                             slug = data[i].slug,
                             )
        Posts.save()
        #delete the record from SubmitPost
        data[i].delete()
        return redirect(f'/podadmin/admin_content/{pod_name}')
    return render(request, 'admin_content.html')

@podadmin_only
def reject_post(request, post_id):
    pod_name = request.user.username
    print('rejected', post_id)
    data = SubmitPost.objects.get(id=post_id)
    data.status = 'rejected'
    data.save()
    return redirect(f'/podadmin/admin_content/{pod_name}')


@podadmin_only
def approve_clips(request, post_id):
    pod_name = request.user.username
    print('approved', post_id)
    data = SubmitClips.objects.filter(id=post_id)
    for i in range(len(data)):
        videoClips = Clips.objects.create(
                             Movie_name = data[i].Movie_name,
                             Language = data[i].Language,
                             Genre = data[i].Genre,
                             Heading = data[i].Heading,
                             text = data[i].text,
                             Image = data[i].Image,
                             Video = data[i].Video,
                             timestamp_field=data[i].timestamp_field,
                             model_type = data[i].model_type,
                             source = data[i].source,
                             logo = data[i].logo,
                             slug = data[i].slug,
                             )
        videoClips.save()
        #delete the record from SubmitClips
        data[i].delete()
        return redirect(f'/podadmin/admin_content/{pod_name}')
    return render(request, 'admin_content.html')

@podadmin_only
def reject_clips(request, post_id):
    pod_name = request.user.username
    print('rejected', post_id)
    data = SubmitClips.objects.get(id=post_id)
    data.status = 'rejected'
    data.save()
    return redirect(f'/podadmin/admin_content/{pod_name}')

@podadmin_only
def reviewlabel(request, Movie_name):
    mydata = CreateLabel.objects.filter(Movie_name=Movie_name)
    mydata2 = PostText1.objects.filter(Movie_name=Movie_name).order_by('-timestamp_field')
    mydata3 = CommentPostText1.objects.filter(movie_title=Movie_name).order_by('-timestamp_field')
    all_data = list(chain(mydata, mydata2, mydata3))
    all_data.sort(key=attrgetter('timestamp_field'), reverse=True)
    template = loader.get_template('reviewlabel.html')
    context = {
        'labelof': all_data,
        'mydata':mydata,
        'PostTextView':mydata2,
        'CommentPostText':mydata3,
    }
    return HttpResponse(template.render(context, request))


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
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
import mysql.connector
from django.db.models import Q
from .models import * 
from .decorators import marketing_only
from django.views.decorators.csrf import csrf_protect
from .forms import PrivacyForm, TermsForm, GuidelinesForm



db = mysql.connector.connect(
  host="3.109.48.139",
  user="myuser",
  password="cinystore",
  database="cinystore"
)
cursor = db.cursor()



def index(request):
   return render(request, 'market_login.html')

@marketing_only
def marketing_dashboard(request):
    mydata = Blog.objects.all()
    template = loader.get_template('marketing_dashboard.html')
    context = {
        'marketing_dashboard': mydata,
    }
    return HttpResponse(template.render(context, request))


def market_signup(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        number = request.POST['phone_number']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']

        if User.objects.filter(username=username):
            messages.error(request, "Username already exist! Please try some other username.")
            return redirect('marketing:market_signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email Already Registered!!")
            return redirect('marketing:market_signup')

        if len(username) > 20:
            messages.error(request, "Username must be under 20 characters!!")
            return redirect('marketing:market_signup')

        if password != confirm_password:
            messages.error(request, "Passwords didn't matched!!")
            return redirect('marketing:market_signup')

        if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric!!")
            return redirect('marketing:market_signup')
        if not number:
            messages.error(request, "Please enter your phone number!")
            return redirect('marketing:market_signup')
        if not number.isdigit():
            messages.error(request, "Please enter a valid phone number!")
            return redirect('marketing:market_signup')
        if len(number) != 10 and not number.startswith('+'):
            messages.error(request, "Please enter a valid phone number!")
            return redirect('marketing:market_signup')
        if len(number) == 10:
            phone_number = '+91' + number  # Add the country code if it's not present
            if PhoneNumber.objects.filter(number=phone_number).exists():
                messages.error(request, "User already exists with this phone number!")
                return redirect('marketing:market_signup')

        myuser = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
        phone_number = PhoneNumber.objects.create(number=number, email=email)
        myuser.phone_numbers_id = phone_number.id
        myuser.save()
        
        myuser.is_marketing = True
        myuser.is_active = False
        myuser.save()
        marketing = MarketingRegister.objects.create(marketing=myuser,
                                                   email = email,
                                                   phone_number = number,
                                                   username=username, 
                                                   first_name=first_name, 
                                                   last_name=last_name)
        marketing.save()
        messages.success(request,
                         "Your Account has been created successfully!! Please check your email to confirm your email address in order to activate your account.")

        # Welcome Email
        subject = "Welcome to Cinystore Marketing Login!!"
        message = "Hello " + myuser.username + "!! \n" + "Welcome to Cinystore!! \nThank you for being a member of marketing team of our website.\n We have also sent you a confirmation email, please confirm your email address. \n\nThanking You\n Team Cinystore !! \n"


        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)

        uid = urlsafe_base64_encode(force_bytes(myuser.pk))
        print(uid)

        token = generate_token.make_token(myuser)
        print(token)

        # Email Address Confirmation Email
        current_site = get_current_site(request)
        email_subject = "Confirm your Email @ Cinystore Marketing Login!!"
        message2 = render_to_string('marketing_account_email_confirmation.html', {

            'name': myuser.username,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser)
        })
        # Construct the local file path to the logo image
        logo_path = os.path.join(settings.BASE_DIR, 'cinystoreapp', 'static', 'img', 'logo.webp')

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
        return redirect('marketing:market_login')
    return render(request, "market_signup.html")



def activate_marketing(request, uid64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uid64))
        mymarketing = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, mymarketing.DoesNotExist):
        mymarketing = None

    if mymarketing is not None and generate_token.check_token(mymarketing, token):
        mymarketing.is_active = True
        mymarketing.save()
        login(request, mymarketing)
        return redirect('marketing:market_login')
    else:
        return HttpResponse('Your acocunt has not been activated, Contact the Support Team.')
    

def marketing_account_activation_success(request):
    return render(request, 'marketing_account_activation_success.html')

     
@marketing_only
def market_Logout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect('marketing:market_login')


def market_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        username = User.objects.filter(Q(username=username)|Q ( email = username)).first()
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('marketing:marketing_dashboard')  # Redirect to the home page after successful login
        else:
            messages.error(request, "Invalid username or password!")
            return redirect('marketing:market_login')
     
    return render(request, "market_login.html")  # Render the login template





from django.shortcuts import render, redirect
from .models import Blog


@marketing_only
def blog_label(request):
    user = request.user
    userdata = MarketingRegister.objects.get(marketing=user)

    if request.method == 'POST':
        # Get form data from POST request
        
        author = MarketingRegister.objects.get(marketing=user)
        blog_name = request.POST.get('Blog_name')
        Introduction = request.POST.get('Introduction')
        heading1 = request.POST.get('heading1')
        heading2 = request.POST.get('heading2')
        heading3 = request.POST.get('heading3')
        heading4 = request.POST.get('heading4')
        description1 = request.POST.get('description1')
        description2 = request.POST.get('description2')
        description3 = request.POST.get('description3')
        description4 = request.POST.get('description4')
        Conclusion = request.POST.get('Conclusion')
        image1 = request.FILES.get('Image1')
        image2 = request.FILES.get('Image2')

        # Create a new instance of the Blog model
        blog_instance = Blog.objects.create(
            Author=author,
            username = user.username,
            Introduction=Introduction,
            Blog_name=blog_name,
            heading1=heading1,
            heading2=heading2,
            heading3=heading3,
            heading4=heading4,
            description1=description1,
            description2=description2,
            description3=description3,
            description4=description4,
            Conclusion=Conclusion,
            Image1=image1,
            Image2=image2,
            slug = blog_name.replace(" ", "-")
        )
        return redirect('marketing:marketing_dashboard')
    else:
        return render(request, 'blog_label.html', {'userdata': userdata})
    


@csrf_protect
def Privacy_form(request):
    if request.method == 'POST':
        form = PrivacyForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, 'Privacy_form.html', {'form': form})
        else:
            form = PrivacyForm()
    return render(request, 'Privacy_form.html')



@csrf_protect
def Terms_form(request):
    if request.method == 'POST':
        form = TermsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, 'Terms_form.html', {'form': form})
        else:
            form = TermsForm()
    return render(request, 'Terms_form.html')




@csrf_protect
def Guidelines_form(request):
    if request.method == 'POST':
        form = GuidelinesForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, 'Guidelines_form.html', {'form': form})
        else:
            form = GuidelinesForm()
    return render(request, 'Guidelines_form.html')



def Guidelines(request):
    mydata = Guidelines.objects.all().order_by('timestamp_field')
    template = loader.get_template('Guidelines.html')
    context = {
        'Guidelines': mydata,
    }
    return HttpResponse(template.render(context, request))



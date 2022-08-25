import logging
from django.shortcuts import render,redirect
from .forms import RegisterForm, LoginForm
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from .token import account_activation_token
from django.views.decorators.cache import never_cache
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from social_django.models import UserSocialAuth



logger = logging.getLogger(__name__)


def signup(request):
    form =RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        to_mail = request.POST.get('email')
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request).domain
            subject = "Activate Your Account"
            
            message = render_to_string('Populus/account_activation_email.html',
                                       {
            'user' : user,
            'domain':current_site,
            'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
            'token' : account_activation_token.make_token(user),
                                       })
            email = EmailMessage(
                subject, message, to=[to_mail]
            )
            email.send()
            return render(request, "Populus/account_activation_sent.html",{'user':user})
    return render(request, "Populus/signup.html", {'form':form})

def activate(request, uidb64, token, backend = 'django.contrib.auth.backends.ModelBackend'):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk = uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
       
        return render(request, 'Populus/account_activation_success.html')
    else:
        return render(request,"Populus/account_activation_invalid.html")
            
    

def signin(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username = username, password=password)          
            
            
            if user is not None:
                if user.is_active:                                     
                    logger.info(REDIRECT_FIELD_NAME)
                    login(request,user) 
                    return redirect('porro:gateway')
                else:
                    messages.info(request, "Please activate your account.")
            else:
                messages.info(request,"Please check your information.")
    else:
        form = LoginForm()
        
    return render(request,"Populus/signin.html", {'form':form})

@never_cache
def logout_user(request):  
    logout(request)
    return redirect('porro:gateway')



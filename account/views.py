from django.shortcuts import render,HttpResponse,redirect
from .forms import RegisterForm,LoginForm
from django.contrib import messages
from .models import CustomUser
from django.contrib.auth import authenticate, login as auth_login , logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from account.models import CustomUser
from carts.models import Cart,CartItem
from carts.views import _cart_id
import requests

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            subject = 'Please activate your account'
            template = 'account/account_varification_email.html'
            send_link(request,user,subject,template)
            return redirect('/accounts/login/?command=verification&email='+user.email)
        else:
            
            return render(request, 'account/register.html', {'form': form})
    else:
        form = RegisterForm()
    return render(request,'account/register.html',{'form':form})

def send_link(request,user,subject,template):
    current_site = get_current_site(request)
    mail_subject = subject
    message = render_to_string(template,{
        'user':user,
        'domain':current_site.domain,
        'uid':urlsafe_base64_encode(force_bytes(user.pk)),
        'token':default_token_generator.make_token(user),
    })
    to_email = user.email 
    send_mail = EmailMessage(mail_subject , message, to=[to_email])
    send_mail.send()

def activate(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = CustomUser._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,CustomUser.DoesNotExist):
        user=None
    if user is not None and default_token_generator.check_token(user,token):
        user.is_active = True
        user.save()
        messages.success(request,'Congrates,Your account is activated')
        return redirect('login')
    else:
        messages.error(request,'Invalid activation link')
        return redirect('register')


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            user = authenticate(request, email=email, password=password)

            if user is not None:
                if user.is_active:
                    try:
                        session_cart = Cart.objects.get(cart_id=_cart_id(request))
                    except Cart.DoesNotExist:
                        session_cart = None

                    user_cart, created = Cart.objects.get_or_create(user=user)

                    if session_cart:
                        session_items = CartItem.objects.filter(cart=session_cart)

                        for session_item in session_items:
                            
                            session_variations = set(session_item.variation.all())
                            user_items = CartItem.objects.filter(cart=user_cart, product=session_item.product)

                            merged = False
                            for user_item in user_items:
                                if session_variations == set(user_item.variation.all()):
                                    user_item.quantity += session_item.quantity
                                    user_item.save()
                                    merged = True
                                    break

                            if not merged:
                                session_item.cart = user_cart
                                session_item.save(update_fields=["cart"])

                        if session_cart != user_cart:
                            session_cart.delete()

                    auth_login(request, user)
                    messages.success(request, 'You are now logged in!')
                    url = request.META.get('HTTP_REFERER')
                    try:
                        query = requests.utils.urlparse(url).query
                        params = dict(x.split('=') for x in query.split('&'))
                        if 'next' in params:
                            nextPage = params['next']
                            return redirect(nextPage)
                    except:
                            return redirect('dashboard')

                else:
                    messages.error(request, 'Your account is inactive!')
            else:
                messages.error(request, 'Invalid email or password')
    else:
        form = LoginForm()

    return render(request, 'account/login.html', {'form': form})



@login_required(login_url='login')
def logout(request):
    auth_logout(request)
    messages.success(request,'Successfully loggedout')
    return redirect('login')
@login_required(login_url='login')
def dashboard(request):
    return render(request,'account/dashboard.html')

def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if CustomUser.objects.filter(email=email).exists():
            user = CustomUser.objects.get(email=email)
            subject = 'Reset Your Password'
            template = 'account/reset_password_email.html'

            send_link(request,user,subject,template)
            messages.success(request,'Password reset email has been sent to your email address.')
            return redirect('login')
        else:
            messages.error(request,'User with this email does not exist!')
            return redirect('forgotPassword')
    return render(request,'account/forgotPassword.html')

def resetpassword_validate(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = CustomUser._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,CustomUser.DoesNotExist):
        user=None
    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid']=uid 
        messages.success(request,'Please reset your password')
        return redirect('resetPassword')
    else:
        messages.error(request,'This link has been expired')
        return redirect('login')

def resetPassword(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if password == confirm_password:
            uid = request.session.get('uid')
            try:
              user = CustomUser.objects.get(pk=uid)
            except CustomUser.DoesNotExist:
               messages.error(request, 'User not found')
               return redirect('login')

            user.set_password(password)
            user.save()
            messages.success(request,'Password reset successfull ')
            return redirect('login')
        else:
            messages.error(request,'Password do not match')
            return redirect('resetPassword')
    else:
        return render(request,'account/resetPassword.html')
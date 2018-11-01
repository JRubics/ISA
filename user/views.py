from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.template import *
from django.conf import settings
from django.contrib.auth.models import User
from .models import Profile
from django.core.mail import send_mail

def login_submit(request):
    if request.method == 'POST':
        email = request.POST['email']
        try:
            username = User.objects.get(email=email)
        except User.DoesNotExist:
            username = None
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/user/home')
        else:
            messages.error(request, "Not a user")
            return redirect(settings.LOGIN_REDIRECT_URL )
    else:
        logout(request)
        return render(request,'user/login_page.html')

def registration_submit(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        city = request.POST['city']
        phone_number = request.POST['phone_number']
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return render(request,'user/registration_page.html')
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return render(request,'user/registration_page.html')
        elif password1 != password2:
            messages.error(request, "Passwords must be same")
            return render(request,'user/registration_page.html')
        user = User.objects.create_user(username=username, email=email, password=password1, first_name=first_name, last_name=last_name, is_active = False)
        profile = Profile.objects.create(user=user, city=city, phone_number=phone_number)
        send_mail(
            'Confirm registration',
            'http://isa.theedgeofrage.com/user/confirm/' + username,
            'isa2018bfj@google.com',
            [email],
            fail_silently=False,
        )
        return redirect('/user/confirmation')
    else:
        logout(request)
        return render(request,'user/registration_page.html')

def confirmation(request):
    return render(request, 'user/confirmation_page.html')

def confirm(request, username=None):
    logout(request)
    user = User.objects.get(username=username)
    user.is_active = True
    user.save()
    return redirect(settings.LOGIN_REDIRECT_URL )

@login_required()
def logout_submit(request):
    logout(request)
    return redirect(settings.LOGIN_REDIRECT_URL)

@login_required()
def home(request):
    return render(request, 'user/home_page.html')
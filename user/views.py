from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.template import *
from django.conf import settings
from django.contrib.auth.models import User
from .models import Profile

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
        # DODAJ UNIQUE NA USERNAME I EMAIL
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        city = request.POST['city']
        phone_number = request.POST['phone_number']
        if password1 == password2:
            user = User.objects.create_user(username=username, email=email, password=password1, first_name=first_name, last_name=last_name)
            profile = Profile.objects.create(user=user, city=city, phone_number=phone_number)
            return redirect('/user/home')
        else:
            messages.error(request, "Passwords must be same")
            return render(request,'user/registration_page.html')
    else:
        logout(request)
        return render(request,'user/registration_page.html')

@login_required()
def logout_submit(request):
    logout(request)
    return redirect(settings.LOGIN_REDIRECT_URL)

@login_required()
def home(request):
    return render(request, 'user/home_page.html')
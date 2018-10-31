from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.template import *
from django.conf import settings
from django.contrib.auth.models import User

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

@login_required()
def logout_submit(request):
    logout(request)
    return redirect(settings.LOGIN_REDIRECT_URL)

@login_required()
def home(request):
    return render(request, 'user/home_page.html')
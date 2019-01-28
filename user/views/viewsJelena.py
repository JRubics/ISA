from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.template import *
from django.conf import settings
from django.contrib.auth.models import User
from user.models import Profile
from car.models import Reservation
from django.core.mail import send_mail
from django.contrib.auth.models import Permission
from car.models import Car
from django.contrib.contenttypes.models import ContentType


def login_submit(request):
    if request.method == 'POST':
        user = authenticate(request, username=Profile.get_username_from_email(
            request.POST['email']), password=request.POST['password'])
        if user is not None:
            login(request, user)
            return redirect('/user/home')
        else:
            messages.error(request, "Not a user")
            return redirect(settings.LOGIN_REDIRECT_URL)
    else:
        logout(request)
        return render(request, 'user/login_page.html')


def registration_submit(request):
    if request.method == 'POST':
        message = Profile.validate_user(
            request.POST['username'], request.POST['email'], request.POST['password1'], request.POST['password2'])
        if message:
            messages.error(request, message)
            return render(request, 'user/registration_page.html')

        profile = Profile.new(username=request.POST['username'],
                              email=request.POST['email'],
                              password=request.POST['password1'],
                              first_name=request.POST['first_name'],
                              last_name=request.POST['last_name'],
                              city=request.POST['city'],
                              phone_number=request.POST['phone_number']
                              )
        send_email(profile.user.username, profile.user.email)
        return redirect('/user/confirmation')
    else:
        logout(request)
        return render(request, 'user/registration_page.html')


def send_email(username, email):
    send_mail(
        'Confirm registration',
        'http://isa.theedgeofrage.com/user/confirm/' + username,
        'isa2018bfj@google.com',
        [email],
        fail_silently=False,
    )


def confirmation(request):
    return render(request, 'user/confirmation_page.html')


def confirm(request, username=None):
    logout(request)
    user = User.objects.get(username=username)
    user.is_active = True
    user.save()
    return redirect(settings.LOGIN_REDIRECT_URL)


@login_required()
def logout_submit(request):
    logout(request)
    return redirect(settings.LOGIN_REDIRECT_URL)


@login_required()
def home(request):
    return render(request, 'user/home_page.html')


@login_required()
def reservations(request):
    reservation_list = Reservation.objects.filter(user=request.user.id)
    context = {'reservations': reservation_list}
    return render(request, 'user/reservations.html', context)
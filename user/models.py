from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )
    city = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=30)

    class Meta:
        permissions = (("is_car_admin", "Is car admin"),
                       ("is_hotel_admin", "Is hotel admin"),
                       ("is_flight_admin", "Is flight admin"),
                       )

    def get_username_from_email(email):
        if User.objects.filter(email=email).exists():
            return User.objects.get(email=email).username
        else:
            return None

    def validate_user(username, email, password1, password2):
        if User.objects.filter(username=username).exists():
            return "Username already exists"
        elif User.objects.filter(email=email).exists():
            return "Email already exists"
        elif password1 != password2:
            return "Passwords must be same"
        else:
            return None
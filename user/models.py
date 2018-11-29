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


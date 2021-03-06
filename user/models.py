from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from avio.models import AvioCompany, PackageReservation
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=30)
    bonus = models.PositiveIntegerField(default=0)
    pic = models.FileField(upload_to='media/', default='/profile.png')
    active_package = models.OneToOneField(PackageReservation, on_delete=models.SET_NULL, null=True, blank=True)

    def new(username, email, password, first_name, last_name, city, phone_number):
        user = User.objects.create_user(username=username,
                                        email=email,
                                        password=password,
                                        first_name=first_name,
                                        last_name=last_name,
                                        is_active=False)
        profile = Profile.objects.create(user=user,
                                         city=city,
                                         phone_number=phone_number)
        return profile

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

    def __str__(self):
        return (str(self.user.first_name) + " " + str(self.user.last_name) + " " + str(self.user.email))


class AdminUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    admin_type = models.CharField(max_length=10)
    avio_admin = models.ForeignKey(
        AvioCompany, on_delete=models.DO_NOTHING, null=True, blank=True)
    first_login = models.BooleanField(default=True)

    class Meta:
        permissions = (("is_car_admin", "Is car admin"),
                       ("is_hotel_admin", "Is hotel admin"),
                       ("is_flight_admin", "Is flight admin"),
                       ("is_master_admin", "Is master admin"),
                       )


class UserRelationship(models.Model):
    user_1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_1')
    user_2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_2')
    RELATIONSHIP_STATUS = (('FF', 'Friends'), ('PS', 'Pending_first_second'), ('PF', 'Pending_second_first'))
    status = models.CharField(max_length=2, choices=RELATIONSHIP_STATUS)

    class Meta:
        unique_together = ['user_1', 'user_2']

    def clean(self):
        if self.user_1.id > self.user_2.id:
            raise ValidationError("Change order of users")

    def __str__(self):
        return (str(self.user_1) + " " + str(self.user_2) + " " + self.status)

    def sendRequest(sender, reciver):
        if sender.id < reciver.id:
            UserRelationship.objects.create(user_1 = sender, user_2 = reciver, status = "PS")
        else:
            UserRelationship.objects.create(user_1 = reciver, user_2 = sender, status = "PF")

    def accept(user1, user2):
        if user1.id < user2.id:
            UserRelationship.objects.filter(user_1 = user1, user_2 = user2).update(status='FF')
        else:
            UserRelationship.objects.filter(user_1 = user2, user_2 = user1).update(status='FF')

    def decline(user1, user2):
        if user1.id < user2.id:
            UserRelationship.objects.filter(user_1 = user1, user_2 = user2).delete()
        else:
            UserRelationship.objects.filter(user_1 = user2, user_2 = user1).delete()


class DiscountPointReference(models.Model):
    travel_coefficient = models.DecimalField(
        default=1,
        decimal_places=2,
        max_digits=8,
        validators=[MinValueValidator(1, "Minimum is 1%"),
                    MaxValueValidator(10, "Maximum is 100%")]
    )
    hotel_discount = models.PositiveIntegerField(
        default=2,
        validators=[MinValueValidator(0, "Percentage is between 0 and 100"),
                    MaxValueValidator(100, "Percentage is between 0 and 100")]
    )
    carservice_discount = models.PositiveIntegerField(
        default=5,
        validators=[MinValueValidator(0, "Percentage is between 0 and 100"),
                    MaxValueValidator(100, "Percentage is between 0 and 100")]
    )
    def clean(self):
        if self.travel_coefficient < 1 or self.travel_coefficient > 10:
            raise ValidationError("Must be between 1 and 10")
        if self.hotel_discount < 0 or self.hotel_discount > 100:
            raise ValidationError("Percentage is between 0 and 100")
        if self.carservice_discount < 0 or self.carservice_discount > 100:
            raise ValidationError("Percentage is between 0 and 100")

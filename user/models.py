from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from avio.models import AvioCompany
from django.core.exceptions import ValidationError


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=30)
    bonus = models.PositiveIntegerField(default=0)
    pic = models.FileField(null=True, default='/profile.png')

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
        return (str(self.user.username) + " " + str(self.user.id))


class AdminUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avio_admin = models.ForeignKey(
        AvioCompany, on_delete=models.DO_NOTHING, null=True)

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

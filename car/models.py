from django.db import models
from datetime import datetime, timezone
from django.conf import settings
from django.contrib.auth.models import User

class Service(models.Model):
    name = models.CharField(max_length=30)
    promo_description = models.TextField()
    country = models.CharField(max_length=60)
    city = models.CharField(max_length=60)
    address = models.CharField(max_length=60)
    number = models.CharField(max_length=60)
    service_admin = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return self.name
    def get_rate(self):
        reservations = Reservation.objects.filter(office1__service=self.id).all()
        if reservations:
            rate = 0
            counter = 0
            for reservation in reservations:
                if CarRate.objects.filter(reservation=reservation.id).exists():
                    rates = CarRate.objects.filter(reservation=reservation.id).all()
                    for r in rates:
                        rate = rate + r.service_rate
                        counter = counter + 1
            if counter != 0:
                return rate / counter
            else:
                return 0
        else:
            return 0

class Car(models.Model):
    MANUFACTURER = (
        ('0', 'Other'),
        ('1', 'Reno'),
        ('2', 'Opel'),
        ('3', 'Ford'),
        ('4', 'Fiat'),
        ('5', 'Toyota'),
        ('6', 'BMV'),
        ('7', 'Mercedes'),
        ('8', 'Peugeot'),
    )
    TYPE = (
        ('1', 'City car'),
        ('2', 'Big car'),
        ('3', 'Truck'),
        ('4', 'Motorcycle'),
    )
    name = models.CharField(max_length=30)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    manufacturer = models.CharField(max_length = 1, choices = MANUFACTURER, default=0)
    model = models.CharField(max_length=30)
    car_type = models.CharField(max_length = 1, choices = TYPE, default=1)
    price = models.DecimalField(max_digits=100,decimal_places=2)
    year = models.PositiveIntegerField()
    seats = models.PositiveIntegerField()
    is_taken = models.BooleanField(default=0)
    on_sale = models.BooleanField(default=0)
    def __str__(self):
        return self.name + " (" + self.service.name + ")"
    def is_car_taken(self, date1=datetime.now, date2=datetime.now):
        reservations = Reservation.objects.filter(car=self.id).all()
        taken = 0
        for reservation in reservations:
            reservation.date1 = reservation.date1.replace(tzinfo=None)
            reservation.date2 = reservation.date2.replace(tzinfo=None)
            if reservation.date1 <= date1 and reservation.date2 >= date1:
                taken = 1
            if reservation.date1 <= date2 and reservation.date2 >= date2:
                taken = 1
            if reservation.date1 <= date1 and reservation.date2 >= date2:
                taken = 1
            if reservation.date1 >= date1 and reservation.date2 <= date2:
                taken = 1
        if taken:
            self.is_taken = 1
        else:
            self.is_taken = 0
        self.save()
        return
    def is_reserved(self, date=datetime.now(timezone.utc)):
        date = date.replace(tzinfo=None)
        reservations = Reservation.objects.filter(car=self.id).all()
        for reservation in reservations:
            reservation.date1 = reservation.date1.replace(tzinfo=None)
            reservation.date2 = reservation.date2.replace(tzinfo=None)
            if reservation.date1 >= date or reservation.date2 >= date:
                self.is_taken = 1
                self.save()
                return
        self.is_taken = 0
        self.save()
        return
    def get_rate(self):
        reservations = Reservation.objects.filter(car=self.id).all()
        if reservations:
            rate = 0
            counter = 0
            for reservation in reservations:
                if CarRate.objects.filter(reservation=reservation.id).exists():
                    rates = CarRate.objects.filter(reservation=reservation.id).all()
                    for r in rates:
                        rate = rate + r.car_rate
                        counter = counter + 1
            if counter != 0:
                return rate / counter
            else:
                return 0
        else:
            return 0


class BranchOffice(models.Model):
    name = models.CharField(max_length=30)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    country = models.CharField(max_length=60)
    city = models.CharField(max_length=60)
    address = models.CharField(max_length=60)
    number = models.CharField(max_length=60)
    def __str__(self):
        return self.name + " (" + self.service.name + ")"

class Reservation(models.Model):
    car = models.ForeignKey(Car, on_delete=models.DO_NOTHING)
    office1 = models.ForeignKey(BranchOffice, related_name='office1', on_delete=models.DO_NOTHING)
    office2 = models.ForeignKey(BranchOffice, related_name='office2', on_delete=models.DO_NOTHING)
    date1 = models.DateTimeField(default=datetime.now)
    date2 = models.DateTimeField(default=datetime.now)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=100,decimal_places=2, default=0)
    def __str__(self):
        return self.car.name + " - " + self.user.username + " (" + str(self.date1) + "," + str(self.date2) + ") - " + str(self.price)
    def is_done(self):
        date1 = self.date2.replace(tzinfo=None)
        date2 = datetime.now().replace(tzinfo=None)
        return date1 < date2
    def can_be_closed(self):
        date1 = self.date1.replace(tzinfo=None)
        date2 = datetime.now().replace(tzinfo=None)
        return abs((date2 - date1).days) >= 2
    def is_rated(self, user):
        return CarRate.objects.filter(reservation=self.id, user=user).exists()

class CarRate(models.Model):
   reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
   car_rate = models.PositiveIntegerField()
   service_rate = models.PositiveIntegerField()
   user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
   def __str__(self):
        return "car - " + str(self.car_rate) + ", service - " + str(self.service_rate) + ", rez - " + str(self.reservation) + ", user - " + str(self.user)
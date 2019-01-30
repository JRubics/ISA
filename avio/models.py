from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


# model zemlje
class Country (models.Model):
    name = models.CharField(max_length=30)
    time_zone = models.IntegerField(
        default=0, validators=[MaxValueValidator(12), MinValueValidator(-11)])

    def __str__(self):
        return (self.name)

# model grada


class City (models.Model):
    name = models.CharField(max_length=30)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return (self.name)

# model avio kompanije


class AvioCompany (models.Model):
    name = models.CharField(max_length=30)  # naziv avio kompanije
    promo_description = models.TextField()  # promotivan opis
    cabine_luggage_description = models.CharField(max_length=130, null=True)
    luggage = models.CharField(max_length=130, null=True)
    additional_services = models.CharField(max_length=130, null=True)

    # address
    city = models.ForeignKey(City, on_delete=models.DO_NOTHING)
    address = models.CharField(max_length=60)
    number = models.CharField(max_length=60)
    destinations = models.ManyToManyField(City, related_name='destinations')

    def __str__(self):  # metoda za ispis podataka
        return (self.name)


# model aerodroma
class Airport (models.Model):
    name = models.CharField(max_length=30)  # naziv aerodroma

    # adresa
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    address = models.CharField(max_length=60)
    number = models.CharField(max_length=60)

    def __str__(self):
        return (self.name + " - " + str(self.city))


# model Leta
class Flight (models.Model):
    avio_company = models.ForeignKey(AvioCompany, on_delete=models.DO_NOTHING)
    departure_airport = models.ForeignKey(
        Airport, related_name='departure_airport', on_delete=models.DO_NOTHING)
    departure_date = models.DateTimeField('departure time')
    departure_city = models.ForeignKey(
        City, related_name='departure_city', on_delete=models.DO_NOTHING)
    arrival_airport = models.ForeignKey(
        Airport, related_name='arrival_airport', on_delete=models.DO_NOTHING)
    arrival_date = models.DateTimeField('arrival time')
    arrival_city = models.ForeignKey(
        City, related_name='arrival_city', on_delete=models.DO_NOTHING)
    distance = models.IntegerField()
    base_price = models.IntegerField()

    def duration(self):
        return self.arrival_date - self.departure_date

    def __str__(self):
        str_date = str(self.departure_date)[:16]
        return (str(self.avio_company) + " - " + str(self.departure_city) + " -> " + str(self.arrival_city) + " - " + str_date)

    def clean(self):
        if self.arrival_date < self.departure_date:
            raise ValidationError("Datas are not valid")

        if self.departure_city != self.departure_airport.city or self.arrival_city != self.arrival_airport.city:
            raise ValidationError("Airport and city must match")


# model Presedanja
class FlightLeg (models.Model):
    flight = models.ForeignKey(Flight, on_delete=models.DO_NOTHING)
    airport = models.ForeignKey(Airport, on_delete=models.DO_NOTHING)
    arrival_date = models.DateTimeField('arrival time')
    departure_date = models.DateTimeField('departure time')

    def parent_flight(self):
        return self.flight.id

    def __str__(self):
        str_date = str(self.departure_date)[:16]
        return (str(self.flight) + " st. " + str(self.airport))

    def clean(self):
        if self.arrival_date > self.flight.arrival_date or self.arrival_date < self.flight.departure_date:
            raise ValidationError("Datas must be between " + str(self.flight.departure_date) + " and " + str(self.flight.arrival_date))

        if self.departure_date < self.flight.arrival_date or self.departure_date < self.flight.departure_date:
            raise ValidationError("Datas must be between " + str(self.flight.departure_date) + " and " + str(self.flight.arrival_date))

        if self.arrival_date > self.departure_date:
            raise ValidationError("Datas are not valid")


# model sedista
class Seat (models.Model):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    seat_number = models.IntegerField()
    SEAT_STATUS = (('T', 'Taken seats'), ('F', 'Free seat'),
                   ('P', 'Promotion seat'), ('O', 'Out of order'), ('R', 'Reserved seat'))
    seat_status = models.CharField(max_length=1, choices=SEAT_STATUS)
    SEAT_TYPE = (('B', 'Business seats'),
                 ('F', 'First class seats'), ('E', 'Economy seats'), )
    seat_type = models.CharField(max_length=1, choices=SEAT_TYPE)
    price_factor = models.FloatField(default=1)

    class Meta:
        unique_together = ['seat_number', 'seat_type', 'flight']

class ManageSeats (Seat):
    class Meta:
        proxy = True
        verbose_name = 'Mange seate'

# model karte
class Ticket (models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    first_name = models.CharField(max_length=30, null=True)
    last_name = models.CharField(max_length=30, null=True)
    passport = models.CharField(max_length=15, null=True)
    time = models.DateTimeField('time of ticket creation', null=True)
    price = models.FloatField(null=True)
    seat = models.ForeignKey(Seat, on_delete=models.DO_NOTHING)
    flight = models.ForeignKey(Flight, on_delete=models.DO_NOTHING)
    TYPE = (('B', 'Bought ticket'), ('R', 'Reserved ticket'), ('P', 'Promotion ticket'))
    status = models.CharField(max_length=1, choices=TYPE)

    def clean(self):
        if self.flight != self.seat.flight:
            raise ValidationError("Seat is not form that flight")

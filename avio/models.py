from django.db import models

#model avio kompanije
class AvioCompany (models.Model):
    name = models.CharField(max_length=30) #naziv avio kompanije
    promo_description = models.TextField() #promotivan opis

    #adres
    city = models.ForeignKey(City, on_delete=models.DO_NOTHING)
    address = models.CharField(max_length=60)
    number = models.CharField(max_length=60)

    def __str__(self):     #metoda za ispis podataka
        return (self.name " " self.) 



#model leta sa presedanjem
class FlightsCombination (modells.Model):
    stops = models.ForeignKey(Flight, on_delete=models.CASCADE)

#model karte
class Ticket (models.Model):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    time = models.DateTimeField('time of ticket creation')
    seat_area = models.ForeignKey(SeatsArea, on_delete=models.DO_NOTHING)
    seat_number = models.IntegerField();
    status = models.IntegerField(); #bought, reserved

#model Leta
class Flight (models.Model):
    avio_company = models.ForeignKey(AvioCompany, on_delete=models.DO_NOTHING)
    departure_date = models.DateTimeField('departure time')
    departure_city = models.ForeignKey(City, on_delete=models.DO_NOTHING)
    arrival_date = models.DateTimeField('arrival time')
    arrival_city = models.ForeignKey(City, on_delete=models.DO_NOTHING)
    distance = models.IntegerField();
    price = models.IntegerField();
    seats_area = models.ForeignKey(SeatsArea, on_delete=models.DO_NOTHING)

#model sedista
class SeatsArea (models.Model):
    area_name = models.CharField(max_length=30)
    row = models.IntegerField(default=4)
    colume = models.IntegerField(default=4)

#model koji povezuje avio kompanije sa zemljama u kojima posluje
class AvioFlyTo (models):
    avioCompany = models.ForeignKey(AvioCompany, on_delete=models.DO_NOTHING)
    country = models.ForeignKey(Country, on_delete=models.DO_NOTHING)

#model zemlje
class Country (models.Model):   
    name = models.CharField(max_length=30)
    time_zone = models.IntegerField(default=0); #dodati ogranicenje od -12 do 12

#model grada
class City (models.Model):
    name = models.CharField(max_length=30)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
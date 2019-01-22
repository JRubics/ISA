from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings


class Hotel(models.Model):
    name = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    address_num = models.CharField(max_length=20)
    description = models.CharField()

    def __str__(self):
        return self.name


class HotelRoom(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    floor_num = models.IntegerField()
    capacity = models.PositiveIntegerField()
    has_balcony = models.BooleanField()


class HotelServices(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    price = models.DecimalField(decimal_places=2,
                                validators=[MinValueValidator(0, "Price cannot be negative")])

    def __str__(self):
        return self.name


class HotelServicePackages(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    services = models.ManyToManyField(HotelServices)
    rooms_discount = models.DecimalField(decimal_places=2,
                                         min_value=0,
                                         max_value=1,
                                         validators=[MinValueValidator(0, "Percentage is between 0 and 1"),
                                                     MaxValueValidator(1, "Percentage is between 0 and 1")])


class HotelRoomPrice(models.Model):
    room = models.ForeignKey(HotelRoom, on_delete=models.CASCADE)
    price_per_day = models.DecimalField(decimal_places=2,
                                        validators=[MinValueValidator(0, "Price cannot be negative")])
    valid_from = models.DateField()
    valid_to = models.DateField()
    # TODO: Date check constraint or validation
    # Service package only if room is on strict discount
    strictly_discounted = models.BooleanField(default=False)
    service_package = models.ForeignKey(
        HotelServicePackages, on_delete=models.CASCADE)
    


class HotelReservation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    rooms = models.ManyToManyField(HotelRoom)
    services = models.ManyToManyField(HotelServices)

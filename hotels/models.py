from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings


class Hotel(models.Model):
    name = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    address_number = models.CharField(max_length=20)
    description = models.TextField(max_length=500)

    def __str__(self):
        return self.name


class HotelRoom(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)  # type
    number = models.IntegerField()
    floor_number = models.IntegerField()
    capacity = models.PositiveIntegerField()
    has_balcony = models.BooleanField()
    class Meta:
        unique_together = ('hotel', 'number')


class HotelService(models.Model):
    PER_PERSON_PER_DAY = 'PPPD'
    PER_ROOM_PER_DAY = 'PRPD'
    PER_PERSON = 'PP'
    PER_ROOM = 'PR'
    CHARGE_TYPES = (
        (PER_PERSON_PER_DAY, "per person/day"),
        (PER_PERSON, "per person"),
        (PER_ROOM_PER_DAY, "per room/day"),
        (PER_ROOM, "per room")
    )
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    price = models.DecimalField(
        decimal_places=2,
        max_digits=8,
        validators=[MinValueValidator(0, "Price cannot be negative")]
    )
    type_of_charge = models.CharField(
        max_length=4,
        choices=CHARGE_TYPES,
        default=PER_PERSON_PER_DAY
    )

    def __str__(self):
        return self.name


class HotelServicePackage(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    services = models.ManyToManyField(HotelService)
    name = models.CharField(max_length=30)
    rooms_discount = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        validators=[MinValueValidator(0, "Percentage is between 0 and 1"),
                    MaxValueValidator(1, "Percentage is between 0 and 1")]
    )


class HotelRoomPrice(models.Model):
    room = models.ForeignKey(HotelRoom, on_delete=models.CASCADE)
    price_per_day = models.DecimalField(
        decimal_places=2,
        max_digits=8,
        validators=[MinValueValidator(0, "Price cannot be negative")]
    )
    valid_from = models.DateField()
    valid_to = models.DateField()
    # TODO: Date check constraint or validation
    # Service package only if room is on strict discount
    strictly_discounted = models.BooleanField(default=False)
    service_package = models.ForeignKey(
        HotelServicePackage, on_delete=models.CASCADE)


class HotelReservation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    rooms = models.ManyToManyField(HotelRoom)
    services = models.ManyToManyField(HotelService)

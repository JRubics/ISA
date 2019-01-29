from decimal import Decimal
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class Hotel(models.Model):
    name = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    address_number = models.CharField(max_length=20, blank=True)
    description = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return self.name


class HotelRoom(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)  # type
    number = models.IntegerField()
    floor_number = models.IntegerField()
    capacity = models.PositiveIntegerField()
    has_balcony = models.BooleanField()
    default_price_per_day = models.DecimalField(
        decimal_places=2,
        max_digits=8,
        validators=[MinValueValidator(
            Decimal('0.01'), "Price cannot be negative")]
    )

    class Meta:
        unique_together = ('hotel', 'number')
        ordering = ['number']

    def clean(self):
        if self.default_price_per_day is None:
            raise ValidationError("Price must be between 0 and 10^6")
        elif self.default_price_per_day < 0:
            raise ValidationError("Price cannot be negative")
        if self.capacity < 1:
            raise ValidationError("Capacity minimum is 1 person")

    def __str__(self):
        return self.hotel.__str__() + '|' + str(self.number)


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

    def clean(self):
        if self.price is None:
            raise ValidationError("Price must be between 0 and 10^6")
        elif self.price < 0:
            raise ValidationError("Price cannot be negative")

    def __str__(self):
        return self.hotel.__str__() + '|' + self.name


class HotelServicePackage(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    services = models.ManyToManyField(HotelService)
    name = models.CharField(max_length=30)
    rooms_discount = models.PositiveIntegerField(
        validators=[MinValueValidator(0, "Percentage is between 0 and 100"),
                    MaxValueValidator(100, "Percentage is between 0 and 100")]
    )

    def clean(self):
        if self.rooms_discount is None:
            raise ValidationError("Percentage is between 0 and 100")
        elif self.rooms_discount < 0 or self.rooms_discount > 100:
            raise ValidationError("Percentage is between 0 and 100")

    def __str__(self):
        return self.name + ' (' + str(self.rooms_discount) + '%)'


class HotelRoomPrice(models.Model):
    room = models.ForeignKey(HotelRoom, on_delete=models.CASCADE)
    price_per_day = models.DecimalField(
        decimal_places=2,
        max_digits=8,
        validators=[MinValueValidator(0, "Price cannot be negative")]
    )
    valid_from = models.DateField()
    valid_to = models.DateField()
    # Service package only if room is on strict discount
    strictly_discounted = models.BooleanField(default=False)
    service_package = models.ForeignKey(
        HotelServicePackage,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    class Meta:
        ordering = ['valid_from']

    def clean(self):
        if self.valid_from > self.valid_to:
            raise ValidationError("Valid from cannot be later than valid to")
        if self.price_per_day is None:
            raise ValidationError("Percentage is between 0 and 1")
        elif self.price_per_day < 0:
            raise ValidationError("Price cannot be negative")
        if self.strictly_discounted and self.service_package is None:
            raise ValidationError(
                "Reference to service package is required if room is discounted")


class HotelReservation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    rooms = models.ManyToManyField(HotelRoom)
    services = models.ManyToManyField(HotelService)

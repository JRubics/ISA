from django.db import models

class Service(models.Model):
    name = models.CharField(max_length=30)
    promo_description = models.TextField()
    country = models.CharField(max_length=60)
    city = models.CharField(max_length=60)
    address = models.CharField(max_length=60)
    number = models.CharField(max_length=60)
    def __str__(self):
        return self.name

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
    def __str__(self):
        return self.name + " (" + self.service.name + ")"

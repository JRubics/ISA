from django.contrib import admin
from .models import Service
from .models import Car

admin.site.register(Service)
admin.site.register(Car)
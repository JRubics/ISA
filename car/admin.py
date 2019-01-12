from django.contrib import admin
from .models import Service
from .models import Car
from .models import BranchOffice
from .models import Reservation
from .models import CarRate

admin.site.register(Service)
admin.site.register(Car)
admin.site.register(BranchOffice)
admin.site.register(Reservation)
admin.site.register(CarRate)
from django.contrib import admin
from .models import Service
from .models import Car
from .models import BranchOffice

admin.site.register(Service)
admin.site.register(Car)
admin.site.register(BranchOffice)
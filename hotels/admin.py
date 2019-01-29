from django.contrib import admin
from .models import Hotel
from .models import HotelReservation
from .models import HotelRoom
from .models import HotelRoomPrice
from .models import HotelService
from .models import HotelServicePackage

admin.site.register(Hotel)
admin.site.register(HotelReservation)
admin.site.register(HotelRoom)
admin.site.register(HotelRoomPrice)
admin.site.register(HotelService)
admin.site.register(HotelServicePackage)

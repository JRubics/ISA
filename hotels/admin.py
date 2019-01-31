from django.contrib import admin
from .models import Hotel
from .models import HotelReservation
from .models import HotelRoom
from .models import HotelRoomPrice
from .models import HotelService
from .models import HotelServicePackage
from .models import HotelShoppingCart
from .models import QuickReservationOption

admin.site.register(Hotel)
admin.site.register(HotelReservation)
admin.site.register(HotelRoom)
admin.site.register(HotelRoomPrice)
admin.site.register(HotelService)
admin.site.register(HotelServicePackage)
admin.site.register(HotelShoppingCart)
admin.site.register(QuickReservationOption)


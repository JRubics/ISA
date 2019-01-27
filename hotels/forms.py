from django.forms import ModelForm
from .models import Hotel, HotelRoom, HotelService, HotelServicePackage


class HotelInfoForm(ModelForm):
    class Meta:
        model = Hotel
        fields = [
            'name',
            'country',
            'city',
            'address',
            'address_number',
            'description'
        ]


class RoomInfoForm(ModelForm):
    class Meta:
        model = HotelRoom
        fields = [
            'name',
            'number',
            'floor_number',
            'capacity',
            'has_balcony',
            'default_price_per_day'
        ]


class HotelServiceForm(ModelForm):
    class Meta:
        model = HotelService
        fields = [
            'name',
            'price',
            'type_of_charge'
        ]


class ServicePackageForm(ModelForm):
    class Meta:
        model = HotelServicePackage
        fields = [
            'services',
            'name',
            'rooms_discount'
        ]

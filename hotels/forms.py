from django.forms import ModelForm, DateInput
from .models import Hotel, HotelRoom, HotelService, HotelServicePackage, HotelRoomPrice, HotelShoppingCart


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


class RoomPriceForm(ModelForm):
    class Meta:
        model = HotelRoomPrice
        fields = [
            'valid_from',
            'valid_to',
            'price_per_day',
            'strictly_discounted',
            'service_package'
        ]
        widgets = {
            'valid_from': DateInput(attrs={'type':'date'}),
            'valid_to': DateInput(attrs={'type':'date'})
        }


class HSCHelpFormRooms(ModelForm):
    class Meta:
        model = HotelShoppingCart
        fields = [
            'rooms'
        ]


class HSCHelpFormServices(ModelForm):
    class Meta:
        model = HotelShoppingCart
        fields = [
            'services'
        ]

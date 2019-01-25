from django.forms import ModelForm
from .models import Hotel


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

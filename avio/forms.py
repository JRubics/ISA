from django.forms import ModelForm, DateInput
from .models import Flight
import datetime

class FlightSearchForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(FlightSearchForm, self).__init__(*args, **kwargs)
        self.fields['departure_airport'].required = False
        self.fields['departure_city'].required = False
        self.fields['departure_date'].required = False
        self.fields['arrival_airport'].required = False
        self.fields['arrival_city'].required = False
        self.fields['arrival_date'].required = False
    class Meta:
        model = Flight
        fields = [
            'departure_city',
            'departure_airport',
            'departure_date',
            'arrival_city',
            'arrival_airport',
            'arrival_date',
        ]
        widgets = {
            'departure_date': DateInput(attrs={'type':'date'}),
            'arrival_date': DateInput(attrs={'type':'date'})
        }

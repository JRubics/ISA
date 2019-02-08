from django.forms import ModelForm
from .models import Car

class VehicleSearchForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(VehicleSearchForm, self).__init__(*args, **kwargs)
        self.fields['name'].required = False
        self.fields['manufacturer'].required = False
        self.fields['model'].required = False
        self.fields['year'].required = False
        self.fields['seats'].required = False
    class Meta:
        model = Car
        fields = [
            'name',
            'manufacturer',
            'model',
            'year',
            'seats'
        ]

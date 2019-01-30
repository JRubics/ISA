from django.views.generic.list import ListView
from django.views.generic.edit import View
from django.shortcuts import redirect, render
from avio.models import Flight, Ticket
from django import forms
import datetime
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class DateInput(forms.DateInput):
    input_type = 'date'

class AirportForm(forms.ModelForm):
    TRIP_TYPE = (("One-way", "One-way"), ("Return", "Return"),)
    trip_type = forms.ChoiceField(choices=TRIP_TYPE)
    SEAT_TYPE = (("Economy", "Economy"), ("Business", "Business"), ("First class", "First class"))
    seat = forms.ChoiceField(choices=SEAT_TYPE)
    passenger_numbers = forms.IntegerField(min_value=1)

    class Meta:
        model = Flight
        fields = ['departure_airport', 'arrival_airport', 'departure_date', 'arrival_date', 'departure_city', 'arrival_city']
        labels = {"departure_airport": "From", "departure_city": "From", "arrival_airport": "To", "arrival_city": "To", "departure_date": "Depart", "arrival_date": "Return",}
        widgets = {'departure_date': DateInput(), 'arrival_date': DateInput(),}

class AvioSearch(View):
    def get(self, request, *args, **kwargs):
        form = AirportForm()
        return render(request, 'avio/avio_search.html', {'form':form})




class PassportForm(forms.Form):
    passport = forms.CharField(label='passport', max_length=15, )

@method_decorator(login_required, name='dispatch')
class FastReservation(ListView):
    model = Ticket
    template_name = 'avio/avio_fast_reservation.html'

    def get_queryset(self):
        tickets = Ticket.objects.filter(flight__avio_company=self.kwargs.get('id'), status = "P")

        #  deo za racunanje cene moze npra da se povecava sa priblizavanjem datuma poletanja
        for ticket in tickets:
            ticket.price = ticket.flight.base_price * ticket.seat.price_factor * 0.5
            ticket.save()

        return tickets

    def get_context_data(self, **kwargs):
        context = super(FastReservation, self).get_context_data(**kwargs)
        context['form'] = PassportForm()
        return context 

    def post(self, request, *args, **kwargs):
        Ticket.objects.filter(pk=request.POST.get('buy')).update(user = request.user, first_name = request.user.first_name, last_name = request.user.last_name, passport = request.POST.get('passport'), time = datetime.datetime.now(), status = 'B')   
        return self.get(request, id)
        





from django.views.generic.list import ListView
from django.views.generic.edit import View
from django.shortcuts import redirect, render
from avio.models import Flight, Ticket, Seat, FlightLeg
from django import forms
import datetime
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import datetime
from django.db.models import F, ExpressionWrapper, fields


class RefineSearchForm(forms.ModelForm):
    FLY_TYPE = (("1", "None"), ("2", "With stops"), ("3", "Direct"), )
    fly_type = forms.ChoiceField(choices=FLY_TYPE , required = False)
    SORT_TYPE = (("1", "None"), ("2", "Price low-hight"), ("3", "Price high-low"), ("4", "Duration"))
    sort = forms.ChoiceField(choices=SORT_TYPE, required = False)

    class Meta:
        model = Flight
        fields = ['avio_company',]

    def __init__(self, *args, **kwargs):
        super(RefineSearchForm, self).__init__(*args, **kwargs)
        self.fields['avio_company'].required = False


class DateInput(forms.DateInput):
    input_type = 'date'


class AirportForm(forms.ModelForm):
    TRIP_TYPE = (("One-way", "One-way"), ("Return", "Return"),)
    trip_type = forms.ChoiceField(choices=TRIP_TYPE)
    SEAT_TYPE = (("Economy", "Economy"), ("Business", "Business"), ("First class", "First class"))
    seat = forms.ChoiceField(choices=SEAT_TYPE)
    passenger_numbers = forms.IntegerField(min_value=1)
    arrival_date = date_available = forms.DateField(widget=DateInput(), initial='2000-01-01')

    class Meta:
        model = Flight
        fields = ['departure_airport', 'arrival_airport', 'departure_date', 'arrival_date', 'departure_city', 'arrival_city']
        labels = {"departure_airport": "From", "departure_city": "From", "arrival_airport": "To", "arrival_city": "To", "departure_date": "Depart", "arrival_date": "Return",}
        widgets = {'departure_date': DateInput(), 'arrival_date': DateInput(),}


class AvioSearch(View):
    def get(self, request, *args, **kwargs):
        form = AirportForm()
        return render(request, 'avio/avio_search.html', {'form':form})


class AvioSearchResults(View):
    def get(self, request, *args, **kwargs):    
        depart_date = request.GET["departure_date"]
        depart_city = request.GET["departure_city"]
        arr_city = request.GET["arrival_city"]
        num_seats = request.GET["passenger_numbers"]
        t_seats = request.GET["seat"]
        ret = []
        ret_ids = []
        search_form = RefineSearchForm()

        # ako je smao u jednom pravcu:
        if request.GET["trip_type"] == "One-way":
            qs = Flight.objects.filter(departure_date__startswith = depart_date, departure_city = depart_city, arrival_city = arr_city)
            for flights in qs:
                if int(num_seats) <= len(Seat.objects.filter(flight = flights.id, seat_type = t_seats[0], seat_status='F')):
                    num_stops = len(FlightLeg.objects.filter(flight = flights.id))
                    str_storps = ("Direct", str(num_stops)+' Stops')[num_stops]
                    ret.append((flights,str_storps))
                    ret_ids.append(flights.id)

        request.session['ret'] = ret_ids
        request.session['num_seats'] = num_seats
        return render(request, 'avio/avio_search_results.html', {'ret':ret, 'num_seats':num_seats, 'search_form':search_form})


    def post(self, request, *args, **kwargs):
        ret = []
        search_form = RefineSearchForm()
        num_seats = request.session['num_seats']
        ret_ids = request.session['ret']
        # sortiranje
        if request.POST.get('sort') == '3':
            flights = Flight.objects.filter(id__in = ret_ids).order_by('-base_price')
        elif request.POST.get('sort') == '4':
            duration = ExpressionWrapper(F('arrival_date') - F('departure_date'), output_field=fields.DurationField())
            flights = Flight.objects.filter(id__in = ret_ids).annotate(duration=duration).order_by('duration')
        else:
            flights = Flight.objects.filter(id__in = ret_ids).order_by('base_price')

        # filter po kompaniji
        if request.POST.get('avio_company') != '':
            flights = flights.filter(avio_company = request.POST.get('avio_company'))

        # filter za broj stopova
        for f in flights:
            num_stops = len(FlightLeg.objects.filter(flight = f.id))
            if request.POST.get('fly_type') == '3':
                if num_stops > 0:
                    str_storps = ("Direct", str(num_stops)+' Stops')[num_stops]
                    ret.append((f,str_storps))
            else:
                str_storps = ("Direct", str(num_stops)+' Stops')[num_stops]
                ret.append((f,str_storps))

        return render(request, 'avio/avio_search_results.html', {'ret':ret, 'num_seats':num_seats, 'search_form':search_form})
    

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
        

class AvioReservation(View):
    def get(self, request, *args, **kwargs):
        id = self.kwargs.get('flight_id')
        return render(request, 'avio/avio_reservation.html', {'id':id})





from django.views.generic.list import ListView
from django.views.generic.edit import View
from django.views.generic.detail import DetailView
from django.views.generic import TemplateView
from django.shortcuts import redirect, render
from avio.models import Flight, Ticket, Seat, FlightLeg, FlightRate, PackageReservation
from user.models import Profile, UserRelationship, DiscountPointReference
from django import forms
import datetime
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import datetime
from django.db.models import F, ExpressionWrapper, fields
import json
from django.contrib import messages 
from django.core.mail import send_mail


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

    class Meta:
        model = Flight
        fields = ['departure_airport', 'arrival_airport', 'departure_date', 'arrival_date', 'departure_city', 'arrival_city']
        widgets = {'departure_date': DateInput(), 'arrival_date': DateInput(),}
        labels = {"departure_airport": "From", "departure_city": "From", "arrival_airport": "To", "arrival_city": "To", "departure_date": "Depart", "arrival_date": "Return",}
        


class AvioSearch(View):
    def get(self, request, *args, **kwargs):
        qs = Ticket.objects.filter(status = "R")
        for tic in qs:
            if tic.invitation_too_long():
                tic.cancelTicket()
                tic.delete()
            elif not tic.package_reservation.canBeCanceled:
                tic.cancelTicket()
                tic.delete()
        form = AirportForm()
        return render(request, 'avio/avio_search.html', {'form':form})


class AvioSearchResults(View):
    def get(self, request, *args, **kwargs): 
        request.session['date_to'] = request.GET["arrival_date"]
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
        request.session['seat_type'] = t_seats
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
        ticket = Ticket.objects.filter(pk=request.POST.get('buy')).update(user = request.user, first_name = request.user.first_name, last_name = request.user.last_name, passport = request.POST.get('passport'), time = datetime.datetime.now(), status = 'B')   
        seat = ticket.seat
        seat.seat_status = "T"
        seat.save()
        return self.get(request, id)

class AvioFlightDetails(DetailView):
    model = Flight
        

class AvioReservation(TemplateView):
    template_name = 'avio/avio_reservation.html'

    def get_context_data(self, *args, **kwargs):
        context = super(AvioReservation, self).get_context_data(**kwargs)
        request = self.request
        id = self.kwargs.get('flight_id')
        fligth = Flight.objects.get(pk=id)
        seat_type = request.session['seat_type']
        querry = Seat.objects.filter(flight = id)
        seats = querry.filter(seat_type = seat_type[0]).order_by('seat_number').values_list('seat_status', 'seat_number')
        context['flight'] = fligth
        context['num_seats'] = request.session['num_seats']
        context['seat_type'] = seat_type
        context['seats'] = json.dumps(list(seats))
        context['s'] = querry.filter(seat_type = seat_type[0], seat_status = "F").order_by('seat_number')

        forms = []
        for x in range(int(request.session['num_seats'])):
            f = DateReservationForm(request.user, context['s'], prefix=x)
            if x == 0:
                f.fields['person'].disabled = True
                f.fields['passport'].required = True
                f.fields['first_name'].initial = request.user.first_name
                f.fields['last_name'].initial = request.user.last_name

            forms.append(f)

        context['form'] = forms
        return context


    def post(self, request, *args, **kwargs):
        forms = []
        ctx = self.get_context_data()
        valid = True
        for x in range(int(request.session['num_seats'])):
            form = DateReservationForm(request.user, ctx['s'],request.POST,  prefix=x)
            if not form.is_valid():
                messages.error(request, "You must choose a firend or give info for a Person " + str(x))
                valid = False

            forms.append(form)
        
        # deo da proveri da nisu isti brojevi sedista i isti ljudi selektovani
        seen_seat = set()
        sean_friend = set()
        for f in forms:
            s = f['seats'].value()
            fri = f['person'].value()
            if s in seen_seat and s != "":
                messages.error(request, "Seats must be different")
                valid = False
                break
            elif fri in sean_friend and fri != "":
                messages.error(request, "Persons must be different")
                valid = False
                break
            else:
                seen_seat.add(s)
                sean_friend.add(fri)

        if not valid:
            ctx['form'] = forms
            return render(request, self.template_name, ctx)

        flight = ctx['flight']
        if_request_user = True

        new_package_reservation = PackageReservation.objects.create(city = flight.arrival_city.name, country = flight.arrival_city.country.name, master_user = request.user, date_from = flight.arrival_date, date_to = request.session['date_to'])
        for f in forms:
            seat = Seat.objects.get(pk = f['seats'].value())
            if f['person'].value() != "" and f['person'].value() != None:
                seat.seat_status = "R"
                person = Profile.objects.get(pk = f['person'].value())
                Ticket.objects.create(package_reservation = new_package_reservation, user = person.user, first_name = person.user.first_name, last_name = person.user.last_name, time =  datetime.datetime.now(), price = flight.base_price * seat.price_factor, flight = flight, seat = seat, status = "R")
                #slanje mejla
                send_mail('Travel Invitation',str(request.user.profile) + " has invited you to travel to " + str(flight) + ". Log in to your account to view the reservation",'isa2018bfj@google.com',[person.user.email],fail_silently=False,)

                if flight.distance > 1000 and person.bonus < 10:
                    person.bonus = person.bonus + 1
                    person.save()
            else:
                seat.seat_status = "T"
                ticket = Ticket.objects.create(package_reservation = new_package_reservation, passport = f['passport'].value(),first_name = f['first_name'].value(), last_name = f['last_name'].value(), time =  datetime.datetime.now(), price = flight.base_price * seat.price_factor, flight = flight, seat = seat, status = "B")
                if if_request_user:
                    if_request_user = False
                    ticket.package_reservation = new_package_reservation
                    ticket.user = request.user
                    ticket.save()

                    person = request.user.profile
                    if flight.distance > 1000 and person.bonus < 10:
                        person.bonus = person.bonus + 1
                        person.save()
            seat.save()

        request.user.profile.active_package = new_package_reservation
        request.user.profile.save()

        return redirect('avio:package_forward')


class DateReservationForm(forms.Form):
    person = forms.ModelChoiceField(queryset=Profile.objects.all(), required=False)
    seats = forms.ModelChoiceField(queryset=Seat.objects.all(), required=False)
    passport = forms.CharField(label='passport', max_length=15, required=False)
    first_name = forms.CharField(label='first_name', max_length=15, required=False)
    last_name = forms.CharField(label='last_name', max_length=15, required=False)

    def __init__(self, user, seats, *args, **kwargs):
        super(DateReservationForm, self).__init__(*args, **kwargs)
        q1 = UserRelationship.objects.filter(user_1 = user, status = 'FF').values_list('user_2', flat=True)
        q2 = UserRelationship.objects.filter(user_2 = user, status = 'FF').values_list('user_1', flat=True)
        profiles = Profile.objects.all().filter(user__id__in=q1) | Profile.objects.all().filter(user__id__in=q2)
        self.fields['person'] = forms.ModelChoiceField(queryset=profiles, required=False)

        self.fields['seats'] = forms.ModelChoiceField(queryset=seats, required=True)


    def is_valid(self):
        valid = super(DateReservationForm, self).is_valid()
        if not valid:
            return valid
 
        if self['person'].value() == '' or self['person'].value() == None:
            if self['passport'].value() == '' or self['first_name'].value() == '' or self['last_name'].value() == '':
                return False

        return True

@login_required()
def flight_rate(request, id=None):
  reservation = Ticket.objects.get(id=id)
  if request.method == 'POST':
    flight_rate = request.POST['flight_rate']
    company_rate = request.POST['company_rate']
    flight_rate = FlightRate(ticket = reservation,
                      flight_rate = flight_rate,
                      company_rate = company_rate,
                      user=request.user)
    flight_rate.save()
    return redirect('/user/home')
  else:
    context = {'reservation':reservation}
    return render(request, 'avio/rate_flight.html',context)

@login_required()
def package_forward(request):
    if request.method == "GET":
        context = {'discount': DiscountPointReference.objects.first().hotel_discount, 'discount_car': DiscountPointReference.objects.first().carservice_discount}
        return render(request, 'avio/forward_package.html', context)


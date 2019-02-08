from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from avio.models import Seat, Flight, Ticket
from django import forms
from django.db.models import Max
from django.contrib import messages
from django.http import Http404
import json

class SeatTypeForm(forms.ModelForm):
    number = forms.IntegerField(min_value=1)
    class Meta:
        model = Seat
        fields = ['seat_type']

class SeatUpdateForm(forms.ModelForm):
    class Meta:
        model = Seat
        fields = ['seat_number', 'seat_type', 'seat_status']


@login_required()
@permission_required('user.is_flight_admin')
def seat_change(request, id):
    querry = Seat.objects.filter(flight = id)
    fligth = Flight.objects.get(pk=id)
    number_b = querry.filter(seat_type = 'B').order_by('seat_number').values_list('seat_status', 'seat_number')
    number_f = querry.filter(seat_type = 'F').order_by('seat_number').values_list('seat_status', 'seat_number')
    number_e = querry.filter(seat_type = 'E').order_by('seat_number').values_list('seat_status', 'seat_number')
    context = {}
    context['id'] = id
    context['number_b'] = len(number_b)
    context['number_f'] = len(number_f)
    context['number_e'] = len(number_e)
    context['seats_e'] = json.dumps(list(number_e))
    context['seats_f'] = json.dumps(list(number_f))
    context['seats_b'] = json.dumps(list(number_b))
    context['form_seat'] = SeatTypeForm()
    context['seat_update_form'] = SeatUpdateForm()
    if request.method == 'POST':
        add_seats = SeatTypeForm(request.POST)
        update_seat = SeatUpdateForm(request.POST)
        
        if request.POST['action'] == 'Add':
            if add_seats.is_valid():
                seat_type = add_seats['seat_type'].value()
                number = int(add_seats['number'].value())
                max_seat_number = Seat.objects.filter(seat_type=seat_type, flight = id).aggregate(max = Max('seat_number'))['max']
                if max_seat_number == None:
                    max_seat_number = 1
                else:
                    max_seat_number = max_seat_number + 1
                price_factor = 1
                if seat_type == "B":
                    price_factor = 1.5
                if seat_type == "F":
                    price_factor = 2
                for x in range(number):
                    Seat.objects.create(flight=fligth, seat_number=(max_seat_number+x), seat_status="F", seat_type=seat_type, price_factor = price_factor)
        else:
            seat_type = update_seat['seat_type'].value()
            seat_status = update_seat['seat_status'].value()
            number = int(update_seat['seat_number'].value())

            try:
                this_flight = Flight.objects.get(pk=id)
                obj = Seat.objects.get(flight = id, seat_type = seat_type, seat_number = number)
                
                if obj.seat_status != "R" or request.user.is_superuser:
                    # ako se menja iz promocije u nesto drugo obrisi kartu sa promocijom
                    if obj.seat_status == "P":
                        Ticket.objects.filter(flight=this_flight, seat=obj).delete()
                    
                    #  ako se sediste menja u promociju napravi kartu sa promocijom
                    if seat_status == "P":
                        Ticket.objects.create(flight=this_flight, seat=obj, status="P")
                    
                    obj.seat_status = seat_status
                    obj.save()
                else:
                    messages.error(request, "Seat is reserved. It can not be changed")
            except Seat.DoesNotExist:
                raise Http404("No Seat matches the given query.")

        return redirect('avio:seats_change', id)
    else:
        return render(request, 'avio/admin_seat_change.html', context)
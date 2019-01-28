from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from avio.models import Seat
import json


@login_required()
@permission_required('user.is_avio_admin')
def seat_change(request, id):
    querry = Seat.objects.filter(flight = id)
    number_b = querry.filter(seat_type = 'B').order_by('seat_number').values_list('seat_status', 'seat_number')
    number_f = querry.filter(seat_type = 'F').order_by('seat_number').values_list('seat_status', 'seat_number')
    number_e = querry.filter(seat_type = 'E').order_by('seat_number').values_list('seat_status', 'seat_number')
    context = {}
    context['number_b'] = len(number_b)
    context['number_f'] = len(number_f)
    context['number_e'] = len(number_e)
    context['seats_e'] = json.dumps(list(number_e))
    context['seats_f'] = json.dumps(list(number_f))
    context['seats_b'] = json.dumps(list(number_b))
    return render(request, 'avio/admin_seat_change.html', context)
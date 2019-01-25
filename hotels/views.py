from django.shortcuts import get_object_or_404, render, redirect
from .models import *
from .forms import *


def admin_view_hotel(request, hotel_id):
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    context = {'hotel': hotel}
    return render(request, 'hotels/admin_view.html', context)


def edit_hotel_info(request, hotel_id):
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    if request.method == 'GET':
        form = HotelInfoForm(instance=hotel)
        context = {'hotel': hotel, 'form': form}
        return render(request, 'hotels/edit_info.html', context)
    elif request.method == 'POST':
        form = HotelInfoForm(request.POST, instance=hotel)
        hotel = form.save()
        return redirect('hotels:admin_view_hotel', hotel_id=hotel.id)
    return render(request, 'hotels/edit_info.html', context)

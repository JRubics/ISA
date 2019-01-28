from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from .forms import HotelInfoForm, HotelServiceForm, RoomInfoForm, RoomPriceForm, ServicePackageForm
from .models import Hotel, HotelRoom, HotelService, HotelServicePackage, HotelRoomPrice, ValidationError
from datetime import datetime, timedelta

# import pdb; pdb.set_trace()

# Hotel

def admin_view_hotel(request, hotel_id):
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    context = {'hotel': hotel}
    return render(request, 'hotels/admin_view.html', context)


def edit_hotel_info(request, hotel_id):
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    if request.method == 'GET':
        form = HotelInfoForm(instance=hotel)
    elif request.method == 'POST':
        form = HotelInfoForm(request.POST, instance=hotel)
        if form.is_valid():
            hotel = form.save()
            return redirect('hotels:admin_view_hotel', hotel_id=hotel.id)
    context = {'hotel': hotel, 'form': form}
    return render(request, 'hotels/edit_hotel_info.html', context)

# Hotel Room

def add_hotel_room(request, hotel_id):
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    if request.method == 'GET':
        form = RoomInfoForm()
    elif request.method == 'POST':
        form = RoomInfoForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.hotel = hotel
            try:
                room.full_clean()
                room.save()
                return redirect('hotels:admin_view_hotel', hotel_id=hotel.id)
            except ValidationError:
                messages.error(request, 'Room number already in use.')
    context = {'hotel': hotel, 'form': form}
    return render(request, 'hotels/add_room.html', context)


def edit_hotel_room(request, hotel_id, room_id=None):
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    room = get_object_or_404(HotelRoom, pk=room_id)
    if request.method == 'GET':
        form = RoomInfoForm(instance=room)
    elif request.method == 'POST':
        form = RoomInfoForm(request.POST, instance=room)
        if form.is_valid():
            room = form.save()
            return redirect('hotels:admin_view_hotel', hotel_id=hotel.id)
    context = {'hotel': hotel, 'room': room, 'form': form}
    return render(request, 'hotels/edit_room.html', context)


def delete_hotel_room(request, hotel_id, room_id=None):
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    room = get_object_or_404(HotelRoom, pk=room_id)
    room.delete()
    return redirect('hotels:admin_view_hotel', hotel_id=hotel.id)

# Hotel Service

def add_hotel_service(request, hotel_id):
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    if request.method == 'GET':
        form = HotelServiceForm()
    elif request.method == 'POST':
        form = HotelServiceForm(request.POST)
        if form.is_valid():
            service = form.save(commit=False)
            service.hotel = hotel
            service.save()
            return redirect('hotels:admin_view_hotel', hotel_id=hotel.id)
    context = {'hotel': hotel, 'form': form}
    return render(request, 'hotels/add_service.html', context)


def edit_hotel_service(request, hotel_id, service_id):
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    service = get_object_or_404(HotelService, pk=service_id)
    if request.method == 'GET':
        form = HotelServiceForm(instance=service)
    elif request.method == 'POST':
        form = HotelServiceForm(request.POST, instance=service)
        if form.is_valid():
            service.save()
            return redirect('hotels:admin_view_hotel', hotel_id=hotel.id)
    context = {'hotel': hotel, 'service': service, 'form': form}
    return render(request, 'hotels/edit_service.html', context)


def delete_hotel_service(request, hotel_id, service_id):
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    service = get_object_or_404(HotelService, pk=service_id)
    service.delete()
    return redirect('hotels:admin_view_hotel', hotel_id=hotel.id)

# Service Package

def add_service_package(request, hotel_id):
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    if request.method == 'GET':
        form = ServicePackageForm()
        form.fields['services'].queryset = HotelService.objects.filter(
            hotel_id=hotel_id)
    elif request.method == 'POST':
        form = ServicePackageForm(request.POST)
        if form.is_valid():
            package = form.save(commit=False)
            package.hotel = hotel
            package.save()
            return redirect('hotels:admin_view_hotel', hotel_id=hotel.id)
    context = {'hotel': hotel, 'form': form}
    return render(request, 'hotels/add_package.html', context)


def edit_service_package(request, hotel_id, package_id):
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    package = get_object_or_404(HotelServicePackage, pk=package_id)
    if request.method == 'GET':
        form = ServicePackageForm(instance=package)
        form.fields['services'].queryset = HotelService.objects.filter(
            hotel_id=hotel_id)
    elif request.method == 'POST':
        form = ServicePackageForm(request.POST, instance=package)
        if form.is_valid():
            package = form.save()
            return redirect('hotels:admin_view_hotel', hotel_id=hotel.id)
    context = {'hotel': hotel, 'package': package, 'form': form}
    return render(request, 'hotels/edit_package.html', context)


def delete_service_package(request, hotel_id, package_id):
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    package = get_object_or_404(HotelServicePackage, pk=package_id)
    package.delete()
    return redirect('hotels:admin_view_hotel', hotel_id=hotel.id)

# Room Price

def view_room_prices(request, hotel_id, room_id):
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    room = get_object_or_404(HotelRoom, pk=room_id)
    context = {'hotel': hotel, 'room': room}
    return render(request, 'hotels/view_room_prices.html', context)


def filtered_room_prices(request, hotel_id, room_id):
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    room = get_object_or_404(HotelRoom, pk=room_id)
    context = {'hotel': hotel, 'room': room}
    if request.method == 'POST':
        date_from = datetime.strptime(request.POST.get(
            'form_valid_from'), "%Y-%m-%d").date()
        date_to = datetime.strptime(request.POST.get(
            'form_valid_to'), "%Y-%m-%d").date()
        if date_from is not None and date_to is not None:
            if date_from < date_to:
                prices = HotelRoomPrice.objects.all().exclude(
                    valid_to__lt=date_from).exclude(valid_from__gt=date_to)
                context = {'hotel': hotel, 'room': room, 'prices': prices,
                           'date_from': date_from, 'date_to': date_to}
    return render(request, 'hotels/view_room_prices.html', context)


def resolve_price_overlaps(price):
    # Overlapping:
            # case 1: total insertion
    querry = HotelRoomPrice.objects.all().filter(
        valid_from__lte=price.valid_from, valid_to__gte=price.valid_to)
    if querry:
        pr1 = querry.first()
        pr2 = querry.first()
        pr2.id = None
        pr1.valid_to = price.valid_from - timedelta(days=1)
        pr2.valid_from = price.valid_to + timedelta(days=1)
        try:
            pr1.full_clean()
            pr1.save()
        except ValidationError:
            pr1.delete()
        try:
            pr2.full_clean()
            pr2.save()
        except ValidationError:
            pass
    # case 2: left partial
    querry = HotelRoomPrice.objects.all().filter(
        valid_from__gte=price.valid_from, valid_from__lte=price.valid_to)
    if querry:
        pr1 = querry.first()
        pr1.valid_from = price.valid_to + timedelta(days=1)
        try:
            pr1.full_clean()
            pr1.save()
        except ValidationError:
            pr1.delete()
    # case 3: right partial
    querry = HotelRoomPrice.objects.all().filter(
        valid_to__gte=price.valid_from, valid_to__lte=price.valid_to)
    if querry:
        pr1 = querry.first()
        pr1.valid_to = price.valid_from - timedelta(days=1)
        try:
            pr1.full_clean()
            pr1.save()
        except ValidationError:
            pr1.delete()


def add_room_price(request, hotel_id, room_id):
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    room = get_object_or_404(HotelRoom, pk=room_id)
    if request.method == 'GET':
        form = RoomPriceForm()
        form.fields['service_package'].queryset = HotelServicePackage.objects.filter(
            hotel_id=hotel_id)
    elif request.method == 'POST':
        form = RoomPriceForm(request.POST)
        if form.is_valid():
            price = form.save(commit=False)
            price.room = room
            resolve_price_overlaps(price)
            price.save()
            return redirect('hotels:view_room_prices', hotel_id=hotel.id, room_id=room.id)
    context = {'hotel': hotel, 'room': room, 'form': form}
    return render(request, 'hotels/add_price.html', context)


def edit_room_price(request, hotel_id, room_id, price_id):
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    room = get_object_or_404(HotelRoom, pk=room_id)
    price = get_object_or_404(HotelRoomPrice, pk=price_id)
    if request.method == 'GET':
        form = RoomPriceForm(instance=price)
        form.fields['service_package'].queryset = HotelService.objects.filter(
            hotel_id=hotel_id)
    elif request.method == 'POST':
        form = RoomPriceForm(request.POST, instance=price)
        if form.is_valid():
            price = form.save(commit=False)
            resolve_price_overlaps(price)
            price.save()
            return redirect('hotels:view_room_prices', hotel_id=hotel.id, room_id=room.id)
    context = {'hotel': hotel, 'room': room, 'price': price, 'form': form}
    return render(request, 'hotels/edit_price.html', context)


def delete_room_price(request, hotel_id, room_id, price_id):
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    room = get_object_or_404(HotelRoom, pk=room_id)
    price = get_object_or_404(HotelRoomPrice, pk=price_id)
    price.delete()
    return redirect('hotels:view_room_prices', hotel_id=hotel.id, room_id=room.id)

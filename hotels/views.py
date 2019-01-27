from django.shortcuts import get_object_or_404, render, redirect
from django.db import models
from .forms import *
from .models import *

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
            room.save()
            return redirect('hotels:admin_view_hotel', hotel_id=hotel.id)
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

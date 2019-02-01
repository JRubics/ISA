from datetime import datetime, timedelta, date
from decimal import Decimal
from calendar import monthrange
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from .forms import HotelInfoForm, HotelServiceForm, RoomInfoForm, RoomPriceForm, ServicePackageForm, HSCHelpFormRooms, HSCHelpFormServices
from .models import Hotel, HotelRoom, HotelService, HotelServicePackage, HotelRoomPrice, ValidationError, HotelShoppingCart, HotelReservation, QuickReservationOption
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required

# import pdb; pdb.set_trace()


def get_room_total(room, check_in, check_out):
    prices = HotelRoomPrice.objects.filter(room_id=room.id)
    prices = prices.exclude(valid_to__lt=check_in).exclude(
        valid_from__gt=check_out)
    total_price = 0
    total_nights = 0
    for price in prices:
        if price.strictly_discounted:
            return -1
        if price.valid_from < check_in:
            price.valid_from = check_in
        if price.valid_to > check_out:
            price.valid_to = check_out
        nights = (price.valid_to - price.valid_from).days
        total_nights += nights
        total_price += price.price_per_day * nights
    total_price += room.default_price_per_day * \
        ((check_out - check_in).days - total_nights)
    room.default_price_per_day = total_price
    return total_price


def get_total_room_prices(rooms, check_in, check_out):
    total = 0
    for room in rooms:
        total += get_room_total(room, check_in, check_out)
    return total


def filter_out_discounted_and_calculate_price(rooms, check_in, check_out):
    tmp = []
    for room in rooms:
        if get_room_total(room, check_in, check_out) > -1:
            tmp.append(room)
    return tmp


def filter_rooms_by_price(rooms, min_price, max_price):
    tmp = []
    for room in rooms:
        if min_price < room.default_price_per_day < max_price:
            tmp.append(room)
    return tmp


def filter_rooms_by_guest_and_room_number(rooms, guest_number, room_number):
    tmp = []
    for room in rooms:
        if room.capacity <= (guest_number - room_number + 1):
            if room_number == 1:
                if room.capacity >= guest_number:
                    tmp.append(room)
            else:
                tmp.append(room)
    return tmp


def get_rids_from_list(rooms):
    tmp = []
    for room in rooms:
        tmp.append(room.id)
    return tmp


def check_room_availability(room, check_in, check_out):
    resers = room.hotelreservation_set.all()
    for res in resers:
        if not (res.check_out <= check_in or res.check_in >= check_out):
            return False
    return True


def filter_avialable_rooms(rooms, check_in, check_out):
    tmp = []
    for room in rooms:
        if check_room_availability(room, check_in, check_out):
            tmp.append(room)
    return tmp


def check_hotel_availability(hotel, check_in, check_out):
    rooms = hotel.hotelroom_set.all()
    rooms = list(rooms)
    rooms = filter_avialable_rooms(rooms, check_in, check_out)
    rooms = filter_out_discounted_and_calculate_price(
        rooms, check_in, check_out)
    if len(rooms) > 0:
        return True
    return False


def filter_available_hotels(hotels, check_in, check_out):
    hotels = list(hotels)
    tmp = []
    for hotel in hotels:
        if check_hotel_availability(
            hotel,
            datetime.strptime(check_in, "%Y-%m-%d").date(),
            datetime.strptime(check_out, "%Y-%m-%d").date()
        ):
            tmp.append(hotel)
    return tmp


def get_total_services(services, day_num, guest_num, room_num):
    total = 0
    for service in services:
        if service.type_of_charge == HotelService.PER_PERSON:
            total += service.price * guest_num
        elif service.type_of_charge == HotelService.PER_PERSON_PER_DAY:
            total += service.price * guest_num * day_num
        elif service.type_of_charge == HotelService.PER_ROOM:
            total += service.price * room_num
        elif service.type_of_charge == HotelService.PER_ROOM_PER_DAY:
            total += service.price * room_num * day_num
    return total

# Hotel


@login_required()
def admin_view_hotel(request, hotel_id):
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    context = {'hotel': hotel}
    return render(request, 'hotels/admin_view.html', context)


@login_required()
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


def view_hotels(request):
    hotels = Hotel.objects.all()
    context = {'hotels': hotels}
    return render(request, 'hotels/view_hotels.html', context)


def search_hotels(request):
    hotels = Hotel.objects.all()
    if request.method == 'POST':
        name = request.POST.get('name')
        country = request.POST.get('country')
        city = request.POST.get('city')
        checkin = request.POST.get('checkin')
        checkout = request.POST.get('checkout')
        if name:
            hotels = hotels.filter(name__icontains=name)
        if country:
            hotels = hotels.filter(country__iexact=country)
        if city:
            hotels = hotels.filter(city__icontains=city)
        if checkin and checkout:
            hotels = filter_available_hotels(hotels, checkin, checkout)
    context = {'hotels': hotels}
    return render(request, 'hotels/view_hotels.html', context)


def view_hotel_unregistered(request, hotel_id):
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    context = {'hotel': hotel}
    return render(request, 'hotels/view_hotel_unregistered.html', context)


@login_required()
def view_hotel_registered(request, hotel_id):
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    context = {'hotel': hotel}
    return render(request, 'hotels/view_hotel_registered.html', context)


# Hotel Room

@login_required()
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


@login_required()
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


@login_required()
def delete_hotel_room(request, hotel_id, room_id=None):
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    room = get_object_or_404(HotelRoom, pk=room_id)
    room.delete()
    return redirect('hotels:admin_view_hotel', hotel_id=hotel.id)

# Hotel Service


@login_required()
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


@login_required()
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


@login_required()
def delete_hotel_service(request, hotel_id, service_id):
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    service = get_object_or_404(HotelService, pk=service_id)
    service.delete()
    return redirect('hotels:admin_view_hotel', hotel_id=hotel.id)

# Service Package


@login_required()
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


@login_required()
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


@login_required()
def delete_service_package(request, hotel_id, package_id):
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    package = get_object_or_404(HotelServicePackage, pk=package_id)
    package.delete()
    return redirect('hotels:admin_view_hotel', hotel_id=hotel.id)

# Room Price


@login_required()
def view_room_prices(request, hotel_id, room_id):
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    room = get_object_or_404(HotelRoom, pk=room_id)
    context = {'hotel': hotel, 'room': room}
    return render(request, 'hotels/view_room_prices.html', context)


@login_required()
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
                prices = HotelRoomPrice.objects.filter(room_id=room.id)
                prices = prices.exclude(valid_to__lt=date_from).exclude(
                    valid_from__gt=date_to)
                context = {'hotel': hotel, 'room': room, 'prices': prices,
                           'date_from': date_from, 'date_to': date_to}
    return render(request, 'hotels/view_room_prices.html', context)


def resolve_price_overlaps(price):
    # Overlapping:
    # case 1: total insertion
    querry = HotelRoomPrice.objects.all().filter(
        room_id=price.room.id,
        valid_from__lte=price.valid_from,
        valid_to__gte=price.valid_to
    )
    if querry:
        pr1 = querry.get()
        pr2 = querry.get()
        pr2.id = None
        pr1.valid_to = price.valid_from
        pr2.valid_from = price.valid_to
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
        room_id=price.room.id,
        valid_from__gte=price.valid_from,
        valid_from__lt=price.valid_to
    )
    if querry:
        pr1 = querry.first()
        pr1.valid_from = price.valid_to
        try:
            pr1.full_clean()
            pr1.save()
        except ValidationError:
            pr1.delete()
    # case 3: right partial
    querry = HotelRoomPrice.objects.all().filter(
        room_id=price.room.id,
        valid_to__gt=price.valid_from,
        valid_to__lte=price.valid_to
    )
    if querry:
        pr1 = querry.first()
        pr1.valid_to = price.valid_from
        try:
            pr1.full_clean()
            pr1.save()
        except ValidationError:
            pr1.delete()


@login_required()
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


@login_required()
def edit_room_price(request, hotel_id, room_id, price_id):
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    room = get_object_or_404(HotelRoom, pk=room_id)
    price = get_object_or_404(HotelRoomPrice, pk=price_id)
    if request.method == 'GET':
        form = RoomPriceForm(instance=price)
        form.fields['service_package'].queryset = HotelServicePackage.objects.filter(
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


@login_required()
def delete_room_price(request, hotel_id, room_id, price_id):
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    room = get_object_or_404(HotelRoom, pk=room_id)
    price = get_object_or_404(HotelRoomPrice, pk=price_id)
    price.delete()
    return redirect('hotels:view_room_prices', hotel_id=hotel.id, room_id=room.id)

# Hotel Reservation


@login_required()
def reservation_step_1(request, hotel_id):
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    if request.method == 'GET':
        context = {'hotel': hotel}
        return render(request, 'hotels/reservation_step_1.html', context)
    if request.method == 'POST':
        check_in = request.POST.get('checkin')
        check_out = request.POST.get('checkout')
        guest_num = request.POST.get('guest_num')
        room_num = request.POST.get('room_num')
        min_price = request.POST.get('min_price')
        max_price = request.POST.get('max_price')

        hsc = HotelShoppingCart()
        if not (check_in and check_out and guest_num and room_num):
            messages.error(request, 'Required fields not filled')
            context = {'hotel': hotel}
            return render(request, 'hotels/reservation_step_1.html', context)

        hsc.check_in = check_in
        hsc.check_out = check_out
        if hsc.check_in >= hsc.check_out:
            messages.error(request, 'Must check out after check in')
            context = {'hotel': hotel}
            return render(request, 'hotels/reservation_step_1.html', context)

        if guest_num >= room_num:
            hsc.guest_number = guest_num
            hsc.room_number = room_num
        else:
            messages.error(
                request, 'Cannot reserve more rooms than number of guests')
            context = {'hotel': hotel}
            return render(request, 'hotels/reservation_step_1.html', context)

        if min_price and max_price:
            if min_price <= max_price:
                hsc.min_room_price = min_price
                hsc.max_room_price = max_price
            else:
                messages.error(
                    request, 'Maximum price smaller than minimum price')
                context = {'hotel': hotel}
                return render(request, 'hotels/reservation_step_1.html', context)
        hsc.hotel = hotel

        user = request.user
        if hasattr(user, 'hotelshoppingcart'):
            user.hotelshoppingcart.delete()
        hsc.user = user

        hsc.save()

        return redirect('hotels:reservation_step_2', hotel_id=hotel.id)


@login_required()
def reservation_step_2(request, hotel_id):
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    user = request.user
    hsc = user.hotelshoppingcart
    if request.method == 'GET':
        rooms = HotelRoom.objects.filter(hotel_id=hotel.id)
        rooms = list(rooms)
        rooms = filter_avialable_rooms(rooms, hsc.check_in, hsc.check_out)
        rooms = filter_out_discounted_and_calculate_price(
            rooms, hsc.check_in, hsc.check_out)
        rooms = filter_rooms_by_guest_and_room_number(
            rooms, hsc.guest_number, hsc.room_number)
        if hsc.min_room_price and hsc.max_room_price:
            rooms = filter_rooms_by_price(
                rooms, hsc.min_room_price, hsc.max_room_price)

        hscform = HSCHelpFormRooms()
        hscform.fields['rooms'].queryset = HotelRoom.objects.filter(
            id__in=get_rids_from_list(rooms))

        context = {'hotel': hotel, 'hsc': hsc,
                   'hscform': hscform, 'rooms': rooms}
        return render(request, 'hotels/reservation_step_2.html', context)
    elif request.method == 'POST':
        hscform = HSCHelpFormRooms(request.POST)
        if hscform.is_valid():
            hsc.rooms.clear()
            for room in hscform.cleaned_data['rooms'].all():
                hsc.rooms.add(room)
            hsc.save()
            return redirect('hotels:reservation_step_3', hotel_id=hotel.id)


@login_required()
def reservation_step_3(request, hotel_id):
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    user = request.user
    hsc = user.hotelshoppingcart
    if request.method == 'GET':
        hscform = HSCHelpFormServices()
        hscform.fields['services'].queryset = HotelService.objects.filter(
            hotel_id=hotel_id)
        services = HotelService.objects.filter(hotel_id=hotel_id)
        context = {'hotel': hotel, 'hsc': hsc,
                   'hscform': hscform, 'services': services}
        return render(request, 'hotels/reservation_step_3.html', context)
    if request.method == 'POST':
        hscform = HSCHelpFormServices(request.POST)
        if hscform.is_valid():
            hsc.services.clear()
            for service in hscform.cleaned_data['services'].all():
                hsc.services.add(service)
            hsc.save()
            return redirect('hotels:reservation_step_4', hotel_id=hotel.id)
        context = {'hotel': hotel, 'hsc': hsc, 'hscform': hscform}
        return render(request, 'hotels/reservation_step_3.html', context)


@login_required()
def reservation_step_4(request, hotel_id):
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    user = request.user
    hsc = user.hotelshoppingcart
    if request.method == 'GET':
        rooms = hsc.rooms.all()
        total_rooms = get_total_room_prices(rooms, hsc.check_in, hsc.check_out)
        total_nights = (hsc.check_out - hsc.check_in).days
        total_services = get_total_services(
            hsc.services.all(), (hsc.check_out - hsc.check_in).days, hsc.guest_number, hsc.rooms.count())
        grand_total = total_rooms + total_services

        hsc.rooms_charge = total_rooms
        hsc.services_charge = total_services
        hsc.save()

        context = {'hotel': hotel, 'hsc': hsc, 'rooms': rooms, 'total_rooms': total_rooms,
                   'total_nights': total_nights, 'total_services': total_services, 'grand_total': grand_total}
        return render(request, 'hotels/reservation_step_4.html', context)
    if request.method == 'POST':
        for room in hsc.rooms.all():
            if not check_room_availability(room, hsc.check_in, hsc.check_out):
                messages.error(
                    request, 'Error during reservation: Some of the requested rooms have already been booked.')
                context = {'hotel': hotel}
                return render(request, 'hotels/reservation_step_4.html', context)
        reservation = HotelReservation()
        reservation.user = user
        reservation.hotel = hotel
        reservation.check_in = hsc.check_in
        reservation.check_out = hsc.check_out
        reservation.rooms_charge = hsc.rooms_charge
        reservation.services_charge = hsc.services_charge
        reservation.guest_number = hsc.guest_number
        try:
            reservation.full_clean()
            reservation.save()
        except ValidationError:
            messages.error(request, 'Error during reservation')
            context = {'hotel': hotel}
            return render(request, 'hotels/reservation_step_4.html', context)
        for room in hsc.rooms.all():
            reservation.rooms.add(room)
        for service in hsc.services.all():
            reservation.services.add(service)
        reservation.save()
        hsc.delete()
        # TODO: reroute
        return redirect('hotels:view_hotels')


def filter_discounted_rooms_and_prepare(rooms, check_in, check_out):
    tmp = []
    for room in rooms:
        prices = HotelRoomPrice.objects.filter(room_id=room.id)
        prices = prices.filter(valid_from__lte=check_in,
                               valid_to__gte=check_out)
        prices = prices.filter(strictly_discounted=True)
        if prices.exists():
            price = prices.get()
            daynum = (check_out - check_in).days
            room.defprice = price.price_per_day * daynum
            service_package = price.service_package
            room.disprice = price.price_per_day * daynum * \
                (Decimal(100) - service_package.rooms_discount) / Decimal(100)
            room.check_in = check_in
            room.check_out = check_out
            room.services = service_package.services.all()
            room.total = room.disprice + \
                get_total_services(room.services, daynum, room.capacity, 1)
            tmp.append(room)
    return tmp


@login_required()
def quick_reservation(request, hotel_id):
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    user = request.user
    hsc = user.hotelshoppingcart
    if request.method == 'GET':
        rooms = hotel.hotelroom_set.all()
        rooms = list(rooms)
        rooms = filter_avialable_rooms(rooms, hsc.check_in, hsc.check_out)
        rooms = filter_discounted_rooms_and_prepare(
            rooms, hsc.check_in, hsc.check_out)
        # TODO: izbaci sobe sa vecim kapacitetom od broja karata
        for room in rooms:
            qro = QuickReservationOption()
            qro.shopping_cart = hsc
            qro.rooms_charge = room.disprice
            qro.services_charge = room.total - room.disprice
            qro.room = get_object_or_404(HotelRoom, pk=room.id)
            qro.save()
            for service in room.services:
                qro.services.add(service)
            room.qro = qro.id
        context = {'rooms': rooms, 'hotel': hotel}
        return render(request, 'hotels/quick_reservation.html', context)
    elif request.method == 'POST':
        qro_id = request.POST.get('qroption')
        qro = get_object_or_404(QuickReservationOption, pk=qro_id)
        if hsc:
            reservation = HotelReservation()
            reservation.user = request.user
            reservation.hotel = hotel
            if not check_room_availability(qro.room, hsc.check_in, hsc.check_out):
                messages.error(
                    request, 'Error during reservation: Room has already been booked.')
                context = {'rooms': rooms, 'hotel': hotel}
                return redirect('hotels:quick_reservation', hotel_id=hotel.id)
            reservation.check_in = hsc.check_in
            reservation.check_out = hsc.check_out
            reservation.rooms_charge = qro.rooms_charge
            reservation.services_charge = qro.services_charge
            reservation.guest_number = hsc.guest_number
            import pdb
            pdb.set_trace()
            try:
                reservation.full_clean()
                reservation.save()
            except ValidationError:
                messages.error(request, 'Error during reservation')
                context = {'hotel': hotel}
                # TODO: reroute
                return render(request, 'hotels/quick_reservation.html', context)
            reservation.rooms.add(qro.room)
            for service in qro.services.all():
                reservation.services.add(service)
            hsc.delete()
            # TODO: reroute
            return redirect('hotels:view_hotels')
        else:
            messages.error(
                request, 'Error during reservation. Please try again')
            # TODO: reroute
            return render(request, 'hotels/quick_reservation.html', context)


# Statistic


def calculate_number_of_visitors_per_day(resers, begin_date, end_date):
    tmp = []
    i = begin_date
    while i <= end_date:
        day_num = 0
        curr_res = resers.filter(check_in__lte=i, check_out__gte=i)
        if curr_res.exists():
            for res in curr_res.all():
                day_num += res.guest_number
        tmp.append(day_num)
        i = i + timedelta(days=1)
    return tmp


def calculate_number_of_visitors_per_week(resers, year):
    tmp = []
    (dow, x) = monthrange(year, 1)
    begin_date = date(year, 1, 1)
    end_date = begin_date + timedelta(days=(6-dow))
    cur_res = resers.filter(
        check_in__lte=end_date,
        check_out__gte=begin_date
    )
    glup = 0
    if cur_res.exists():
        for res in cur_res.all():
            glup += res.guest_number
    tmp.append(glup)
    begin_date = end_date + timedelta(days=1)
    end_date = end_date + timedelta(days=7)
    for i in range(2, 52):
        cur_res = resers.filter(
            check_in__lte=end_date,
            check_out__gte=begin_date
        )
        glup = 0
        if cur_res.exists():
            for res in cur_res.all():
                glup += res.guest_number
        begin_date = begin_date + timedelta(days=7)
        end_date = end_date + timedelta(days=7)
        tmp.append(glup)
    return tmp


def calculate_number_of_visitors_per_month(resers, year):
    tmp = []
    for i in range(1, 13):
        (x, month_end) = monthrange(year, i)
        cur_res = resers.filter(
            check_in__lte=date(year, i, month_end),
            check_out__gte=date(year, i, 1)
        )
        glup = 0
        if cur_res.exists():
            for res in cur_res.all():
                glup += res.guest_number
        tmp.append(glup)
    return tmp


@login_required()
def visitor_number(request, hotel_id):
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    year = date.today().year
    begin_date = date(year, 1, 1)
    end_date = date(year, 12, 31)
    resers = HotelReservation.objects.filter(
        hotel_id=hotel.id
    ).order_by('check_in')
    rset_days = calculate_number_of_visitors_per_day(
        resers, begin_date, end_date)
    rset_weeks = calculate_number_of_visitors_per_week(resers, year)
    rset_months = calculate_number_of_visitors_per_month(resers, year)
    context = {
        'hotel': hotel,
        'rset_days': rset_days,
        'rset_weeks': rset_weeks,
        'rset_months': rset_months
    }
    return render(request, 'hotels/hotel_stats_guests.html', context)


def calculate_earnings(hotel, begin_date, end_date):
    resers = HotelReservation.objects.filter(
        hotel_id=hotel.id,
        check_out__gte=begin_date,
        check_out__lte=end_date
    )
    tmp = 0
    if resers.exists():
        for res in resers.all():
            tmp += res.rooms_charge + res.services_charge
    return tmp


@login_required()
def earnings_statistic(request, hotel_id):
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    if request.method == 'GET':
        context = {'hotel': hotel}
        return render(request, 'hotels/hotel_stats_earnings.html', context)
    elif request.method == 'POST':
        begin_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        if begin_date is None or end_date is None:
            messages.error(request, 'Both dates required')
            context = {'hotel': hotel}
            return render(request, 'hotels/hotel_stats_earnings.html', context)
        if begin_date > end_date:
            messages.error(request, 'Both dates required')
            context = {'hotel': hotel}
            return render(request, 'hotels/hotel_stats_earnings.html', context)
        total_earnings = calculate_earnings(hotel, begin_date, end_date)
        context = {'hotel': hotel, 'total_earnings': total_earnings}
        return render(request, 'hotels/hotel_stats_earnings.html', context)

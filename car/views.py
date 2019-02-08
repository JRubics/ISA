from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from decimal import Decimal
import sys
from django.contrib import messages
from datetime import datetime, timedelta, date
from .models import Service
from .models import Car
from .models import BranchOffice
from .models import Reservation
from .models import CarRate
from user.models import User, DiscountPointReference
from avio.models import PackageReservation, Ticket
from django.conf import settings
from django.db import IntegrityError, transaction
from .forms import VehicleSearchForm


@login_required()
@permission_required('user.is_car_admin')
def edit_service(request):
  try:
    service = Service.objects.get(id=request.user.service.id)
    if request.method == 'POST':
      service.name = request.POST['name']
      service.country = request.POST['country']
      service.city = request.POST['city']
      service.address = request.POST['address']
      service.number = request.POST['number']
      service.promo_description = request.POST['promo_description']
      service.save()
    cars = Car.objects.select_related().filter(service = service.id)
    for car in cars:
      car.is_reserved()
    offices = BranchOffice.objects.select_related().filter(service = service.id)
    context = {'manufacturer':Car.MANUFACTURER, 'type':Car.TYPE,'service':service, 'cars':cars, 'offices':offices}
    return render(request, 'car/edit_service.html',context)
  except:
    messages.error(request, "User has ho service!")
    return render(request, 'user/login_page.html')


@login_required()
@permission_required('user.is_car_admin')
def add_car(request, service_id=None):
  if request.method == 'POST':
    car = Car(name = request.POST['name'],
              service = Service.objects.get(id=service_id),
              manufacturer = request.POST['manufacturer_select'],
              model = request.POST['model'],
              car_type = request.POST['type_select'],
              price = request.POST['price'],
              year = request.POST['year'],
              seats = request.POST['seats'],
              )
    car.save()
    return redirect('/car/service')
  else:
    context = {'manufacturer':Car.MANUFACTURER, 'type':Car.TYPE, 'service_id':service_id}
    return render(request, 'car/add_car.html', context)

@login_required()
@permission_required('user.is_car_admin')
def edit_car(request, id=None):
  car = Car.objects.get(id=id)
  if request.user.service == car.service:
    if request.method == 'POST':
      car.name = request.POST['name']
      car.manufacturer = request.POST['manufacturer_select']
      car.model = request.POST['model']
      car.car_type = request.POST['type_select']
      car.price = request.POST['price']
      car.year = request.POST['year']
      car.seats = request.POST['seats']
      if request.POST.getlist('on_sale') != []:
        car.on_sale = True
      else:
        car.on_sale = False
      car.save()
      context = {'car':car}
      return redirect('/car/service')
    else:
      context = {'manufacturer':Car.MANUFACTURER, 'type':Car.TYPE,'car':car}
      return render(request, 'car/edit_car.html',context)
  else:
    messages.error(request, "Invalid car id!")
    return redirect('/car/service')

@login_required()
@permission_required('user.is_car_admin')
def delete_car(request, id=None):
  car = Car.objects.get(id=id)
  if request.user.service == car.service:
    service = car.service
    car.delete()
    return redirect('/car/service')
  else:
    messages.error(request, "Invalid car id!")
    return redirect('/car/service')

@login_required()
@permission_required('user.is_car_admin')
def add_office(request, service_id=None):
  if request.method == 'POST':
    office = BranchOffice(name = request.POST['name'],
                          service = Service.objects.get(id=service_id),
                          country = request.POST['country'],
                          city = request.POST['city'],
                          address = request.POST['address'],
                          number = request.POST['number']
                          )
    office.save()
    return redirect('/car/service')
  else:
    context = {'service_id':service_id}
    return render(request, 'car/add_office.html', context)

@login_required()
@permission_required('user.is_car_admin')
def edit_office(request, id=None):
  office = BranchOffice.objects.get(id=id)
  if request.user.service == office.service:
    if request.method == 'POST':
      office.name = request.POST['name']
      office.country = request.POST['country']
      office.city = request.POST['city']
      office.address = request.POST['address']
      office.number = request.POST['number']
      office.save()
      context = {'office':office}
      return redirect('/car/service')
    else:
      context = {'office':office}
      return render(request, 'car/edit_office.html',context)
  else:
    messages.error(request, "Invalid office id!")
    return redirect('/car/service')

@login_required()
@permission_required('user.is_car_admin')
def delete_office(request, id=None):
  office = BranchOffice.objects.get(id=id)
  if request.user.service == office.service:
    service = office.service
    office.delete()
    return redirect('/car/service')
  else:
    messages.error(request, "Invalid office id!")
    return redirect('/car/service')


@login_required()
def choose_service(request):
  if request.method == 'POST':
    name = request.POST['name']
    country = request.POST['country1']
    city = request.POST['city']
    street = request.POST['address']
    number = request.POST['number']
    services = [service for service in Service.objects.all()
                        if name in service.name
                        and country in service.country
                        and city in service.city
                        and street in service.address
                        and number in service.number]
    offices = BranchOffice.objects.all()
    services = [service for service in services
                        if service.id in [b.service.id for b in offices]]
    context = {'services':services, 'name':name, 'country':country,
            'city':city, 'street':street, 'number':number, 'offices':offices}
    return render(request, 'car/service_list.html', context)
  else:
    if request.user.profile.active_package is None:
      messages.error(request, "You don't have active package!")
      return redirect('/user/home')
    else:
      services = Service.objects.all()
      offices = BranchOffice.objects.all()
      services = [service for service in services
                          if service.id in [b.service.id for b in offices]]
      context = {'services':services, 'offices':offices}
      return render(request, 'car/choose_service.html', context)


@login_required()
def sort_by_name(request):
  services = Service.objects.all().order_by('name')
  offices = BranchOffice.objects.all()
  services = [service for service in services
                      if service.id in [b.service.id for b in offices]]
  context = {'services':services, 'offices':offices}
  return render(request, 'car/choose_service.html', context)


@login_required()
def sort_by_city(request):
  services = Service.objects.all().order_by('city')
  offices = BranchOffice.objects.all()
  services = [service for service in services
                      if service.id in [b.service.id for b in offices]]
  context = {'services':services, 'offices':offices}
  return render(request, 'car/choose_service.html', context)


@login_required()
def reservation(request, id=None):
  if id != "None":
    service = Service.objects.get(id=id)
    cars = Car.objects.select_related().filter(service = id)
    offices = BranchOffice.objects.select_related().filter(service = id)
    context = {'type':Car.TYPE,'service':service, 'offices':offices}
    return render(request, 'car/reservation.html', context)
  else:
    return redirect('/car/choose')

@login_required()
def choose_car(request, id):
  if request.method == 'POST':
    max_price = request.POST['max'] if request.POST['max'] != "" else sys.maxsize
    min_price = request.POST['min'] if request.POST['min'] != "" else -sys.maxsize - 1
    cars = Car.objects.select_related().filter(service = id,
                                      car_type = request.POST['type_select'],
                                      price__lte = max_price,
                                      price__gte = min_price,
                                      seats__gte = request.POST['seats'])
    office1 = request.POST['office_select1']
    office2 = request.POST['office_select2']
    date1 = request.POST['date1']
    date2 = request.POST['date2']
    d1 = datetime.strptime(date1, '%Y-%m-%d')
    d2 = datetime.strptime(date2, '%Y-%m-%d')
    d3 = datetime.now()
    days1 = (d2-d1).days
    days2 = (d1-d3).days
    if days1 <= 0 or days2 < 0:
      return render(request, 'car/date_warning.html')
    car_prices_for_user = {}
    for car in cars:
      car.is_car_taken(d1, d2)
      car_prices_for_user[car.id] = car.price * days1 * Decimal((100-make_discount(request, False)) * 0.01)
    cars = [c for c in cars if c.is_taken == 0 and c.on_sale == 0]
    context = {'manufacturer':Car.MANUFACTURER, 'type':Car.TYPE,
              'cars':cars,'office1':office1, 'office2':office2,
              'date1':date1, 'date2':date2,
              'car_prices_for_user':car_prices_for_user}
    return render(request, 'car/choose_car.html', context)
  else:
    return redirect('/car/choose')


def make_discount(request, fast):
  discount = DiscountPointReference.objects.all().first()
  discount_value = request.user.profile.bonus * round(discount.travel_coefficient)
  if fast:
    discount_value = discount_value + 20
  if request.user.profile.active_package:
    if request.user.profile.active_package.hotel_reservation:
      discount_value = discount_value + discount.carservice_discount
    else:
      discount_value = discount_value + discount.hotel_discount
  if discount_value >= 90:
    discount_value = 90
  return discount_value

@login_required()
def fast_choose_car(request):
  if request.method == 'POST':
    cars = Car.objects.all()
    country = request.POST['country']
    city = request.POST['city']
    date1 = request.POST['date1']
    date2 = request.POST['date2']
    d1 = datetime.strptime(date1, '%Y-%m-%d')
    d2 = datetime.strptime(date2, '%Y-%m-%d')
    d3 = datetime.now()
    days1 = (d2-d1).days
    days2 = (d1-d3).days
    if days1 <= 0 or days2 < 0:
      return render(request, 'car/date_warning.html')
    car_prices_for_user = {}
    for car in cars:
      car.is_car_taken(d1, d2)
      car_prices_for_user[car.id] = car.price * days1 * Decimal((100-make_discount(request, True)) * 0.01)
    cars = [c for c in cars if c.is_taken == 0 and c.on_sale == 1 and c.service.country == country and c.service.city == city]
    context = {'manufacturer':Car.MANUFACTURER, 'type':Car.TYPE,
              'cars':cars, 'days':days1,
              'date1':date1, 'date2':date2,
              'car_prices_for_user':car_prices_for_user}
    return render(request, 'car/fast_choose_car.html', context)
  else:
    return redirect('/car/choose')

# @transaction.atomic
@login_required()
def make_reservation(request, id):
  if request.method == 'POST':
    user = User.objects.get(id=request.user.id)
    if user.profile.active_package is None:
      messages.error(request, "You don't have active package!")
      return redirect('/user/home')
    office1 = request.POST['office1']
    office2 = request.POST['office2']
    date1 = request.POST['date1']
    date2 = request.POST['date2']
    price = request.POST['price']
    car = Car.objects.get(id=id)
    d1 = datetime.strptime(date1, '%Y-%m-%d')
    d2 = datetime.strptime(date2, '%Y-%m-%d')
    car.is_car_taken(d1, d2)
    if car.is_taken:
      messages.error(request, "Reservation already exists")
      return redirect('/car/choose')
    reservation = Reservation(car = car,
                          office1 = BranchOffice.objects.get(id=office1),
                          office2 = BranchOffice.objects.get(id=office2),
                          date1 = date1,
                          date2 = date2,
                          price = price,
                          user = user)
    reservation.save()
    package = PackageReservation.objects.get(id=user.profile.active_package.id)
    package.car_reservation = reservation
    package.save()
    return redirect('/car/confirm')
  else:
    return redirect('/car/choose')

# @transaction.atomic
@login_required()
def make_fast_reservation(request, id):
  if request.method == 'POST':
    user = User.objects.get(id=request.user.id)
    if user.profile.active_package is None:
      messages.error(request, "You don't have active package!")
      return redirect('/user/home')
    service = Service.objects.get(id=request.POST['service'])
    date1 = request.POST['date1']
    date2 = request.POST['date2']
    price = request.POST['price']
    office = BranchOffice.objects.filter(service=service.id).first()
    car = Car.objects.get(id=id)
    d1 = datetime.strptime(date1, '%Y-%m-%d')
    d2 = datetime.strptime(date2, '%Y-%m-%d')
    car.is_car_taken(d1, d2)
    if car.is_taken:
      messages.error(request, "Reservation already exists")
      return redirect('/car/choose')
    reservation = Reservation(car = car,
                          office1 = office,
                          office2 = office,
                          date1 = date1,
                          date2 = date2,
                          price = price,
                          user = User.objects.get(id=request.user.id))
    reservation.save()
    package = PackageReservation.objects.get(id=user.profile.active_package.id)
    package.car_reservation = reservation
    package.save()
    return redirect('/car/confirm')
  else:
    return redirect('/car/choose')


@login_required()
def confirmation(request):
  package = PackageReservation.objects.get(id=request.user.profile.active_package.id)
  tickets = Ticket.objects.all()
  context = {'package':package, 'tickets':tickets}
  return render(request, 'car/confirm_package.html',context)

@login_required()
def confirm_package(request):
  user = User.objects.get(id=request.user.id)
  if user.profile.active_package is None:
    messages.error(request, "You don't have active package!")
    return redirect('/user/home')
  profile = user.profile
  profile.active_package = None
  profile.save()
  return redirect('/user/home')

# @transaction.atomic
@login_required()
def close_package(request):
  user = User.objects.get(id=request.user.id)
  if user.profile.active_package is None:
    messages.error(request, "You don't have active package!")
    return redirect('/user/home')
  profile = user.profile
  package = profile.active_package
  profile.active_package = None
  profile.save()

  for tic in package.ticket_set.all():
    tic.cancelTicket()

  if package.car_reservation != None:
    car_res = package.car_reservation
    car_res.delete()

  if package.hotel_reservation != None:
    hotel_res = package.hotel_reservation
    hotel_res.delete()
  package.delete()
  return redirect('/user/home')


@login_required()
def car_rate(request, id=None):
  reservation = Reservation.objects.get(id=id)
  if request.method == 'POST':
    car_rate = request.POST['car_rate']
    service_rate = request.POST['service_rate']
    car_rate = CarRate(reservation = reservation,
                      car_rate = car_rate,
                      service_rate = service_rate,
                      user=request.user)
    car_rate.save()
    return redirect('/user/home')
  else:
    context = {'reservation':reservation}
    return render(request, 'car/rate_car.html',context)

# @transaction.atomic
@login_required()
def cancel_reservation(request, id=None):
  reservation = Reservation.objects.get(id=id)
  package = PackageReservation.objects.filter(master_user=request.user, car_reservation = reservation).first()
  if reservation.can_be_closed:
    package.car_reservation = None
    package.save()
    reservation.delete()
  return redirect('/user/home')


def calculate_number_of_cars_per_period(resers, period):
  year = date.today().year
  begin_date = date(year, 1, 1)
  end_date = date(year, 12, 31)
  tmp = []
  i = begin_date
  while i <= end_date:
    car_num = 0
    curr_res =[x for x in resers if i <= x.date1.date() and i + timedelta(days=period) > x.date1.date()]
    if curr_res:
      for res in curr_res:
        car_num += 1
    tmp.append(car_num)
    i = i + timedelta(days=period)
  return tmp


def calculate_number_of_cars_per_month(resers):
  tmp = []
  year = date.today().year
  for i in range(1,13):
    car_num = 0
    curr_res =[x for x in resers if i == x.date1.date().month and x.date1.date().year == year]
    if curr_res:
      for res in curr_res:
        car_num += 1
    tmp.append(car_num)
  return tmp


@login_required()
def graph(request):
  service = Service.objects.get(id=request.user.service.id)
  reservations = Reservation.objects.all().order_by('date1')
  reservations = [r for r in reservations if r.office1.service == service]
  rset_days = calculate_number_of_cars_per_period(reservations, 1)
  rset_weeks = calculate_number_of_cars_per_period(reservations, 7)
  rset_months = calculate_number_of_cars_per_month(reservations)
  context = {
    'rset_days': rset_days,
    'rset_weeks': rset_weeks,
    'rset_months': rset_months
  }
  return render(request, 'car/graph.html', context)


@login_required()
def incomes(request):
  service = Service.objects.get(id=request.user.service.id)
  income = -1
  if request.method == 'POST':
    income = 0
    reservations = Reservation.objects.all().order_by('date1')
    reservations = [r for r in reservations if r.office1.service == service]
    date1 = request.POST['date1']
    date2 = request.POST['date2']
    d1 = datetime.strptime(date1, '%Y-%m-%d').replace(tzinfo=None)
    d2 = datetime.strptime(date2, '%Y-%m-%d').replace(tzinfo=None)
    days = (d2-d1).days
    if days < 0:
      messages.error(request, "FIRST DATE MUST BE BEFORE SECOND DATE AND IN THE FUTURE!")
      context = {
        'service':service,
        'income':income
      }
      return render(request, 'car/incomes.html', context)
    for r in reservations:
      if r.date1.replace(tzinfo=None) >= d1 and r.date2.replace(tzinfo=None) <= d2:
        income = income + r.price
  context = {
    'service':service,
    'income':income
  }
  return render(request, 'car/incomes.html', context)


def service_home_page_unregistered(request, service_id):
  service = get_object_or_404(Service, pk=service_id)
  search_form = VehicleSearchForm()
  helper = dict(Car.MANUFACTURER)
  if request.method == 'GET':
    vehicles = service.car_set.all()
    context = {'service': service, 'vehicles': vehicles.all(), 'search_form': search_form, 'helper': helper}
    return render(request, 'car/view_unregistered.html', context)
  elif request.method == 'POST':
    vehicles = Car.objects.filter(service_id=service.id)
    form = VehicleSearchForm(request.POST)
    if form.is_valid():
      name = form.cleaned_data['name']
      manufacturer = form.cleaned_data['manufacturer']
      model = form.cleaned_data['model']
      year = form.cleaned_data['year']
      seats = form.cleaned_data['seats']
      if name:
        vehicles = vehicles.filter(name__icontains=name)
      if manufacturer:
         vehicles = vehicles.filter(manufacturer__exact=manufacturer)
      if model:
        vehicles = vehicles.filter(model__icontains=model)
      if year:
        vehicles = vehicles.filter(year=year)
      if seats:
        vehicles = vehicles.filter(seats=seats)
    context = {'service': service, 'vehicles': vehicles.all(), 'search_form': search_form, 'helper': helper}
    return render(request, 'car/view_unregistered.html', context)


def all_services_unregistered(request):
  services = Service.objects.all()
  context = {'services': services}
  return render(request, 'car/all_services_unregistered.html', context)

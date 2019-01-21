from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from decimal import Decimal
import sys
from datetime import datetime, timedelta
from .models import Service
from .models import Car
from .models import BranchOffice
from .models import Reservation
from .models import CarRate
from user.models import User



@login_required()
@permission_required('user.is_car_admin')
def car_home(request):
  services = Service.objects.all()
  context = {'services':services}
  return render(request, 'car/car_admin_home.html',context)

@login_required()
@permission_required('user.is_car_admin')
def edit_service(request, id=None):
  if request.method == 'POST':
    service = Service.objects.filter(id=id).first()
    service.name = request.POST['name']
    service.country = request.POST['country']
    service.city = request.POST['city']
    service.address = request.POST['address']
    service.number = request.POST['number']
    service.promo_description = request.POST['promo_description']
    service.save()
  service = Service.objects.filter(id=id).first()
  cars = Car.objects.select_related().filter(service = id)
  car_rates = {}
  for car in cars:
    car.is_reserved()
    car_rates[car.id] = car.get_rate()
  rate = service.get_rate()
  offices = BranchOffice.objects.select_related().filter(service = id)
  context = {'manufacturer':Car.MANUFACTURER, 'type':Car.TYPE,'service':service, 'cars':cars, 'offices':offices, 'rate':rate, 'car_rates':car_rates}
  return render(request, 'car/edit_service.html',context)

@login_required()
@permission_required('user.is_car_admin')
def add_service(request):
  if request.method == 'POST':
    service = Service(name = request.POST['name'],
                          country = request.POST['country'],
                          city = request.POST['city'],
                          address = request.POST['address'],
                          number = request.POST['number'],
                          promo_description = request.POST['promo_description'])
    service.save()
    return redirect('/car/home')
  else:
    context = {'manufacturer':Car.MANUFACTURER, 'type':Car.TYPE}
    return render(request, 'car/add_service.html', context)

@login_required()
@permission_required('user.is_car_admin')
def add_car(request, service_id=None):
  if request.method == 'POST':
    car = Car(name = request.POST['name'],
              service = Service.objects.filter(id=service_id).first(),
              manufacturer = request.POST['manufacturer_select'],
              model = request.POST['model'],
              car_type = request.POST['type_select'],
              price = request.POST['price'],
              year = request.POST['year'],
              seats = request.POST['seats'],
              )
    car.save()
    return redirect('/car/service/'+str(service_id))
  else:
    context = {'manufacturer':Car.MANUFACTURER, 'type':Car.TYPE, 'service_id':service_id}
    return render(request, 'car/add_car.html', context)

@login_required()
@permission_required('user.is_car_admin')
def edit_car(request, id=None):
  if request.method == 'POST':
    car = Car.objects.filter(id=id).first()
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
    return redirect('/car/service/'+str(car.service.id))
  else:
    car = Car.objects.filter(id=id).first()
    context = {'manufacturer':Car.MANUFACTURER, 'type':Car.TYPE,'car':car}
    return render(request, 'car/edit_car.html',context)

@login_required()
@permission_required('user.is_car_admin')
def delete_car(request, id=None):
  car = Car.objects.filter(id=id).first()
  service = car.service
  car.delete()
  return redirect('/car/service/'+str(service.id))

@login_required()
@permission_required('user.is_car_admin')
def add_office(request, service_id=None):
  if request.method == 'POST':
    office = BranchOffice(name = request.POST['name'],
                          service = Service.objects.filter(id=service_id).first(),
                          country = request.POST['country'],
                          city = request.POST['city'],
                          address = request.POST['address'],
                          number = request.POST['number']
                          )
    office.save()
    return redirect('/car/service/'+str(service_id))
  else:
    context = {'service_id':service_id}
    return render(request, 'car/add_office.html', context)

@login_required()
@permission_required('user.is_car_admin')
def edit_office(request, id=None):
  if request.method == 'POST':
    office = BranchOffice.objects.filter(id=id).first()
    office.name = request.POST['name']
    office.country = request.POST['country']
    office.city = request.POST['city']
    office.address = request.POST['address']
    office.number = request.POST['number']
    office.save()
    context = {'office':office}
    return redirect('/car/service/'+str(office.service.id))
  else:
    office = BranchOffice.objects.filter(id=id).first()
    context = {'office':office}
    return render(request, 'car/edit_office.html',context)

@login_required()
@permission_required('user.is_car_admin')
def delete_office(request, id=None):
  office = BranchOffice.objects.filter(id=id).first()
  service = office.service
  office.delete()
  return redirect('/car/service/'+str(service.id))


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
    service_rates = {}
    for service in services:
      service_rates[service.id] = service.get_rate()
    context = {'services':services, 'name':name, 'country':country,
            'city':city, 'street':street, 'number':number, 'offices':offices,
            'service_rates':service_rates}
    return render(request, 'car/service_list.html', context)
  else:
    services = Service.objects.all()
    service_rates = {}
    for service in services:
      service_rates[service.id] = service.get_rate()
    rate = service.get_rate()
    offices = BranchOffice.objects.all()
    context = {'services':services, 'offices':offices, 'service_rates':service_rates}
    return render(request, 'car/choose_service.html', context)

@login_required()
def reservation(request):
  if request.method == 'POST':
    s_id = request.POST['service_select']
    if s_id == "None":
      services = Service.objects.all()
      offices = BranchOffice.objects.all()
      context = {'services':services, 'offices':offices,}
      return render(request, 'car/choose_service.html', context)
    service = Service.objects.filter(id=s_id).first()
    cars = Car.objects.select_related().filter(service = s_id)
    offices = BranchOffice.objects.select_related().filter(service = s_id)
    context = {'type':Car.TYPE,'service':service, 'offices':offices}
    return render(request, 'car/reservation.html', context)

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
    days = abs((d2-d1).days)
    car_rates = {}
    car_prices_for_user = {}
    for car in cars:
      car.is_car_taken(d1, d2)
      car_rates[car.id] = car.get_rate()
      car_prices_for_user[car.id] = car.price * days * Decimal((100-request.user.profile.bonus) * 0.01)
    cars = [c for c in cars if c.is_taken == 0 and c.on_sale == 0]
    context = {'manufacturer':Car.MANUFACTURER, 'type':Car.TYPE,
              'cars':cars,'office1':office1, 'office2':office2,
              'date1':date1, 'date2':date2, 'car_rates': car_rates,
              'car_prices_for_user':car_prices_for_user}
    return render(request, 'car/choose_car.html', context)

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
    days = abs((d2-d1).days)
    car_rates = {}
    car_prices_for_user = {}
    for car in cars:
      car.is_car_taken(d1, d2)
      car_rates[car.id] = car.get_rate()
      car_prices_for_user[car.id] = car.price * days * Decimal((100-request.user.profile.bonus - 5) * 0.01)
    cars = [c for c in cars if c.is_taken == 0 and c.on_sale == 1 and c.service.country == country and c.service.city == city]
    print(cars)
    context = {'manufacturer':Car.MANUFACTURER, 'type':Car.TYPE,
              'cars':cars, 'days':days,
              'date1':date1, 'date2':date2,
              'car_prices_for_user':car_prices_for_user}
    return render(request, 'car/fast_choose_car.html', context)

@login_required()
def make_reservation(request, id):
  if request.method == 'POST':
    office1 = request.POST['office1']
    office2 = request.POST['office2']
    date1 = request.POST['date1']
    date2 = request.POST['date2']
    price = request.POST['price']
    reservation = Reservation(car = Car.objects.filter(id=id).first(),
                          office1 = BranchOffice.objects.filter(id=office1).first(),
                          office2 = BranchOffice.objects.filter(id=office2).first(),
                          date1 = date1,
                          date2 = date2,
                          price = price,
                          user = User.objects.filter(id=request.user.id).first())
    reservation.save()
    return redirect('/user/reservations')

@login_required()
def make_fast_reservation(request, id):
  if request.method == 'POST':
    service = Service.objects.filter(id=request.POST['service']).first()
    date1 = request.POST['date1']
    date2 = request.POST['date2']
    price = request.POST['price']
    office = BranchOffice.objects.filter(service=service.id).first()
    reservation = Reservation(car = Car.objects.filter(id=id).first(),
                          office1 = office,
                          office2 = office,
                          date1 = date1,
                          date2 = date2,
                          price = price,
                          user = User.objects.filter(id=request.user.id).first())
    reservation.save()
    return redirect('/user/reservations')


@login_required()
def car_rate(request, id=None):
  if request.method == 'POST':
    reservation = Reservation.objects.filter(id=id).first()
    car_rate = request.POST['car_rate']
    service_rate = request.POST['service_rate']
    car_rate = CarRate(reservation = reservation,
                      car_rate = car_rate,
                      service_rate = service_rate)
    car_rate.save()
    return redirect('/user/reservations')
  else:
    reservation = Reservation.objects.filter(id=id).first()
    context = {'reservation':reservation}
    return render(request, 'car/rate_car.html',context)

@login_required()
def cancel_reservation(request, id=None):
  reservation = Reservation.objects.filter(id=id).first()
  if reservation.can_be_closed:
    reservation.delete()
  return redirect('/user/reservations')

@login_required()
def graph(request, id=None):
  service = Service.objects.filter(id=id).first()
  reservations = Reservation.objects.all()
  reservations = [r for r in reservations if r.office1.service == service]
  r_year = [r for r in reservations if r.date1.replace(tzinfo=None) >= datetime.now() - timedelta(days=365) and r.date1.replace(tzinfo=None) <= datetime.now()]
  r_month = [r for r in reservations if r.date1.replace(tzinfo=None) >= datetime.now() - timedelta(days=30) and r.date1.replace(tzinfo=None) <= datetime.now()]
  r_week = [r for r in reservations if r.date1.replace(tzinfo=None) >= datetime.now() - timedelta(days=7) and r.date1.replace(tzinfo=None) <= datetime.now()]
  r_day = [r for r in reservations if r.date1.replace(tzinfo=None) >= datetime.now() - timedelta(days=1) and r.date1.replace(tzinfo=None) <= datetime.now()]
  res_num = [len(r_day), len(r_week), len(r_month), len(r_year)]
  print([len(r_day), len(r_week), len(r_month), len(r_year)])
  day_income = 0
  day_income = sum([r.price for r in r_day]) / 100
  week_income = 0
  week_income = sum([r.price for r in r_week]) / 100
  month_income = 0
  month_income = sum([r.price for r in r_month]) / 100
  year_income = 0
  year_income = sum([r.price for r in r_year]) / 100
  print([day_income,week_income,month_income,year_income])
  print(type(2.2))
  income = [float(day_income),float(week_income),float(month_income),float(year_income)]
  return render(request, 'car/graph.html', {'res_num': res_num, 'income':income})
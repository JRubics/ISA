from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from .models import Service
from .models import Car
from .models import BranchOffice


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
  offices = BranchOffice.objects.select_related().filter(service = id)
  context = {'manufacturer':Car.MANUFACTURER, 'type':Car.TYPE,'service':service, 'cars':cars, 'offices':offices}
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
def test_graph(request, id=None):
  godina = [2,1,3,4]
  mesec = [1,3,4,2,5,3,4]
  dan = [1,3,4,2,9,6,1,2]
  return render(request, 'car/test.html', {'godina': godina, 'mesec':mesec, 'dan':dan})
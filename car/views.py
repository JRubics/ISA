from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from .models import Service
from .models import Car

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
    context = {'service':service}
    return render(request, 'car/edit_service.html',context)
  else:
    service = Service.objects.filter(id=id).first()
    cars = Car.objects.select_related().filter(service = id)
    context = {'service':service, 'cars':cars}
    return render(request, 'car/edit_service.html',context)

@login_required()
@permission_required('user.is_car_admin')
def add_service(request, id=None):
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
    return render(request, 'car/add_service.html')
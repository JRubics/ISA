from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from .models import Service

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
    context = {'service':service}
    return render(request, 'car/edit_service.html',context)

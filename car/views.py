from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required

@login_required()
@permission_required('user.is_car_admin')
def car_home(request):
  return HttpResponse("You're looking at car")
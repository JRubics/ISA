from django.urls import path
from . import views

app_name = 'car'
urlpatterns = [
    path('home', views.car_home, name='car_home'),
]
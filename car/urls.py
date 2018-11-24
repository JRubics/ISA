from django.urls import path
from . import views

app_name = 'car'
urlpatterns = [
    path('home', views.car_home, name='car_home'),
    path('edit_service/<id>', views.edit_service, name='edit_service'),
    path('add_service', views.add_service, name='add_service'),
]
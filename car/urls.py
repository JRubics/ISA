from django.urls import path
from . import views

app_name = 'car'
urlpatterns = [
    path('home', views.car_home, name='car_home'),
    path('service', views.add_service, name='add_service'),
    path('service/<id>', views.edit_service, name='edit_service'),
    path('add_car/<service_id>', views.add_car, name='add_car'),
    path('edit_car/<id>', views.edit_car, name='edit_car'),
    path('add_office/<service_id>', views.add_office, name='add_office'),
    path('edit_office/<id>', views.edit_office, name='edit_office'),
]
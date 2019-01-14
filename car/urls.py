from django.urls import path
from . import views

app_name = 'car'
urlpatterns = [
    path('home', views.car_home, name='car_home'),
    path('service', views.add_service, name='add_service'),
    path('service/<id>', views.edit_service, name='edit_service'),
    path('add/<service_id>', views.add_car, name='add_car'),
    path('edit/<id>', views.edit_car, name='edit_car'),
    path('delete/<id>', views.delete_car, name='delete_car'),
    path('office/<service_id>', views.add_office, name='add_office'),
    path('office/edit/<id>', views.edit_office, name='edit_office'),
    path('office/delete/<id>', views.delete_office, name='delete_office'),
    path('choose', views.choose_service, name='choose_service'),
    path('reservation', views.reservation, name='reservation'),
    path('choose/<id>', views.choose_car, name='choose_car'),
    path('reservation/<id>', views.make_reservation, name='make_reservation'),
    path('rate/<id>', views.car_rate, name='car_rate'),
]
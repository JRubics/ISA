from django.urls import path
from . import views

app_name = 'car'
urlpatterns = [
    path('service', views.edit_service, name='edit_service'),
    path('add/<service_id>', views.add_car, name='add_car'),
    path('edit/<id>', views.edit_car, name='edit_car'),
    path('delete/<id>', views.delete_car, name='delete_car'),
    path('office/<service_id>', views.add_office, name='add_office'),
    path('office/edit/<id>', views.edit_office, name='edit_office'),
    path('office/delete/<id>', views.delete_office, name='delete_office'),
    path('choose', views.choose_service, name='choose_service'),
    path('reservation', views.reservation, name='reservation'),
    path('choose/<id>', views.choose_car, name='choose_car'),
    path('fast', views.fast_choose_car, name='fast_choose_car'),
    path('reservation/<id>', views.make_reservation, name='make_reservation'),
    path('reservation/fast/<id>', views.make_fast_reservation, name='make_fast_reservation'),
    path('rate/<id>', views.car_rate, name='car_rate'),
    path('rate/cancel/<id>', views.cancel_reservation, name='cancel_reservation'),
    path('graph', views.graph, name='graph'),
    path('incomes', views.incomes, name='incomes'),
]
from django.urls import path
from . import views

app_name = 'hotels'
urlpatterns = [
    path('<int:hotel_id>/admin_view/', views.admin_view_hotel, name="admin_view_hotel"),
    path('<int:hotel_id>/edit_info/', views.edit_hotel_info, name="edit_hotel_info"),
    path('<int:hotel_id>/guest_stats/', views.visitor_number, name="visitor_number"),
    path('<int:hotel_id>/earning_stats/', views.earnings_statistic, name="earnings_statistic"),
    path('<int:hotel_id>/rooms/new/', views.add_hotel_room, name="add_hotel_room"),
    path('<int:hotel_id>/rooms/<int:room_id>/edit/', views.edit_hotel_room, name="edit_hotel_room"),
    path('<int:hotel_id>/rooms/<int:room_id>/delete/', views.delete_hotel_room, name="delete_hotel_room"),
    path('<int:hotel_id>/services/new/', views.add_hotel_service, name="add_hotel_service"),
    path('<int:hotel_id>/services/<int:service_id>/edit/', views.edit_hotel_service, name="edit_hotel_service"),
    path('<int:hotel_id>/services/<int:service_id>/delete/', views.delete_hotel_service, name="delete_hotel_service"),
    path('<int:hotel_id>/packages/new/', views.add_service_package, name="add_service_package"),
    path('<int:hotel_id>/packages/<int:package_id>/edit/', views.edit_service_package, name="edit_service_package"),
    path('<int:hotel_id>/packages/<int:package_id>/delete/', views.delete_service_package, name="delete_service_package"),
    path('<int:hotel_id>/rooms/<int:room_id>/prices/', views.view_room_prices, name="view_room_prices"),
    path('<int:hotel_id>/rooms/<int:room_id>/prices/filtered/', views.filtered_room_prices, name="filtered_room_prices"),
    path('<int:hotel_id>/rooms/<int:room_id>/prices/new/', views.add_room_price, name="add_room_price"),
    path('<int:hotel_id>/rooms/<int:room_id>/prices/<int:price_id>/edit/', views.edit_room_price, name="edit_room_price"),
    path('<int:hotel_id>/rooms/<int:room_id>/prices/<int:price_id>/delete/', views.delete_room_price, name="delete_room_price"),
    path('all/', views.view_hotels, name="view_hotels"),
    path('search/', views.search_hotels, name="search_hotels"),
    path('<int:hotel_id>/view', views.view_hotel_unregistered, name="view_hotel_unregistered"),
    path('<int:hotel_id>/booking_view', views.view_hotel_registered, name="view_hotel_registered"),
    path('<int:hotel_id>/reservation/step_1', views.reservation_step_1, name="reservation_step_1"),
    path('<int:hotel_id>/reservation/step_2', views.reservation_step_2, name="reservation_step_2"),
    path('<int:hotel_id>/reservation/step_3', views.reservation_step_3, name="reservation_step_3"),
    path('<int:hotel_id>/reservation/final', views.reservation_step_4, name="reservation_step_4"),
    path('<int:hotel_id>/reservation/quick', views.quick_reservation, name="quick_reservation"),
    path('rate/<id>', views.hotel_rate, name='hotel_rate'),
]

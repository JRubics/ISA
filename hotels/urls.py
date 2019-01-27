from django.urls import path
from . import views

app_name = 'hotels'
urlpatterns = [
    path('<int:hotel_id>/admin_view/', views.admin_view_hotel, name="admin_view_hotel"),
    path('<int:hotel_id>/edit_info/', views.edit_hotel_info, name="edit_hotel_info"),
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
]

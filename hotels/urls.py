from django.urls import path
from . import views

app_name = 'hotels'
urlpatterns = [
    path('<int:hotel_id>/admin_view/', views.admin_view_hotel, name="admin_view_hotel"),
    path('<int:hotel_id>/edit_info/', views.edit_hotel_info, name="edit_hotel_info")
]
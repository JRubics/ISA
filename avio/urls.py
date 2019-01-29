from django.urls import path
from . import views

app_name = 'avio'
urlpatterns = [
    path('avio/seats/flight/change/<id>', views.seat_change, name='seats_change'),

    path('avio/search', views.AvioSearch.as_view(), name='search_avio'),
]
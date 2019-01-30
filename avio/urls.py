from django.urls import path
from . import views

app_name = 'avio'
urlpatterns = [
    path('avio/seats/flight/change/<id>', views.seat_change, name='seats_change'),

    path('avio/search', views.AvioSearch.as_view(), name='search_avio'),




    # za ko god radi profilne stranice kompanija
    path('avio/fast/reservation/<id>', views.FastReservation.as_view(), name='fast_reservation'),
]
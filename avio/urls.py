from django.urls import path
from . import views

app_name = 'avio'
urlpatterns = [
    path('avio/seats/flight/change/<id>', views.seat_change, name='seats_change'),

    path('avio/search', views.AvioSearch.as_view(), name='search_avio'),
    path('avio/search/results/', views.AvioSearchResults.as_view(), name='search_results_avio'),
    path('avio/search/flight/details/<pk>', views.AvioFlightDetails.as_view(), name='avio_flight_details'),
    path('avio/search/reservation/<flight_id>', views.AvioReservation.as_view(), name='avio_reservation'),
    # za ko god radi profilne stranice kompanija
    path('avio/fast/reservation/<id>', views.FastReservation.as_view(), name='fast_reservation'),
    path('rate/<id>', views.flight_rate, name='flight_rate'),
]
from django.test import TestCase
from avio.models import *
from django.urls import reverse


class AvioReservation(TestCase):
    fixtures = ['avio/fixtures/avio.json']

    # testovi za AvioSearch rezultate
    def test_avio_seach_results_found_1(self):
        self.client.login(username="Orion", password="wdvhu098")
        context = {}
        context['arrival_date'] = "2019-02-19"
        context["departure_date"] = "2019-02-10"
        context["departure_city"] = "1"
        context["arrival_city"] = "7"
        context["passenger_numbers"] = "2"
        context["seat"] = "Economy"
        context["trip_type"] = "One-way"
        response = self.client.get(reverse('avio:search_results_avio'),data=context)
        self.assertQuerysetEqual(response.context['ret'], ["(<Flight: FTN AIR - Novi Sad -> Porto - 2019-02-10 18:04>, 'Direct')"])

    def test_avio_seach_results_found_2(self):
        self.client.login(username="Orion", password="wdvhu098")
        context = {}
        context['arrival_date'] = "2019-02-19"
        context["departure_date"] = "2019-02-10"
        context["departure_city"] = "1"
        context["arrival_city"] = "7"
        context["passenger_numbers"] = "1"
        context["seat"] = "Economy"
        context["trip_type"] = "One-way"
        response = self.client.get(reverse('avio:search_results_avio'),data=context)
        self.assertQuerysetEqual(response.context['ret'], ["(<Flight: FTN AIR - Novi Sad -> Porto - 2019-02-10 18:04>, 'Direct')", "(<Flight: TAP AIR PROTUGAL - Novi Sad -> Porto - 2019-02-10 20:55>, 'Direct')"])

    def test_avio_seach_results_found_0(self):
        self.client.login(username="Orion", password="wdvhu098")
        context = {}
        context['arrival_date'] = "2019-02-19"
        context["departure_date"] = "2019-02-07"
        context["departure_city"] = "1"
        context["arrival_city"] = "7"
        context["passenger_numbers"] = "1"
        context["seat"] = "Economy"
        context["trip_type"] = "One-way"
        response = self.client.get(reverse('avio:search_results_avio'),data=context)
        self.assertQuerysetEqual(response.context['ret'], [])

    def test_avio_seach_results_not_enogh_seats_0(self):
        self.client.login(username="Orion", password="wdvhu098")
        context = {}
        context['arrival_date'] = "2019-02-19"
        context["departure_date"] = "2019-02-10"
        context["departure_city"] = "1"
        context["arrival_city"] = "7"
        context["passenger_numbers"] = "21"
        context["seat"] = "Economy"
        context["trip_type"] = "One-way"
        response = self.client.get(reverse('avio:search_results_avio'),data=context)
        self.assertQuerysetEqual(response.context['ret'], [])

    # testovi za AvioSearch filtere
    def test_avio_seach_results_sorted_price_high_low(self):
        self.client.login(username="Orion", password="wdvhu098")
        session = self.client.session
        session['ret'] = [15, 23]
        session['num_seats'] = 1
        context = {}
        context['sort'] = "3" # sortiranje po ceni
        context["avio_company"] = ""
        context["fly_type"] = ""
        response = self.client.post(reverse('avio:search_results_avio'),data=context)
        self.assertQuerysetEqual(response.context['ret'], ["(<Flight: TAP AIR PROTUGAL - Novi Sad -> Porto - 2019-02-10 20:55>, 'Direct')", "(<Flight: FTN AIR - Novi Sad -> Porto - 2019-02-10 18:04>, 'Direct')"])





















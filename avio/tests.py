from django.test import TestCase
from avio.models import *
from django.urls import reverse
import datetime


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
        context["departure_date"] = "2019-02-11"
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
        context = {}
        context['sort'] = "3" # sortiranje po ceni
        context["avio_company"] = ""
        context["fly_type"] = ""
        context['arrival_date'] = "2019-02-19"
        context["departure_date"] = "2019-02-10"
        context["departure_city"] = "1"
        context["arrival_city"] = "7"
        context["passenger_numbers"] = "1"
        context["seat"] = "Economy"
        context["trip_type"] = "One-way"
        response = self.client.get(reverse('avio:search_results_avio'),data=context)
        response = self.client.post(reverse('avio:search_results_avio'),data=context)
        self.assertQuerysetEqual(response.context['ret'], ["(<Flight: TAP AIR PROTUGAL - Novi Sad -> Porto - 2019-02-10 20:55>, 'Direct')", "(<Flight: FTN AIR - Novi Sad -> Porto - 2019-02-10 18:04>, 'Direct')"])

    def test_avio_seach_results_sorted_price_low_high(self):
        self.client.login(username="Orion", password="wdvhu098")
        context = {}
        context['sort'] = "2" # sortiranje po ceni
        context["avio_company"] = ""
        context["fly_type"] = ""
        context['arrival_date'] = "2019-02-19"
        context["departure_date"] = "2019-02-10"
        context["departure_city"] = "1"
        context["arrival_city"] = "7"
        context["passenger_numbers"] = "1"
        context["seat"] = "Economy"
        context["trip_type"] = "One-way"
        response = self.client.get(reverse('avio:search_results_avio'),data=context)
        response = self.client.post(reverse('avio:search_results_avio'),data=context)
        self.assertQuerysetEqual(response.context['ret'], ["(<Flight: FTN AIR - Novi Sad -> Porto - 2019-02-10 18:04>, 'Direct')", "(<Flight: TAP AIR PROTUGAL - Novi Sad -> Porto - 2019-02-10 20:55>, 'Direct')"])

    def test_avio_seach_results_sorted_flight_duration(self):
        self.client.login(username="Orion", password="wdvhu098")
        context = {}
        context['sort'] = "4" # sortiranje po trajanju
        context["avio_company"] = ""
        context["fly_type"] = ""
        context['arrival_date'] = "2019-02-19"
        context["departure_date"] = "2019-02-10"
        context["departure_city"] = "1"
        context["arrival_city"] = "7"
        context["passenger_numbers"] = "1"
        context["seat"] = "Economy"
        context["trip_type"] = "One-way"
        response = self.client.get(reverse('avio:search_results_avio'),data=context)
        response = self.client.post(reverse('avio:search_results_avio'),data=context)
        self.assertQuerysetEqual(response.context['ret'], ["(<Flight: TAP AIR PROTUGAL - Novi Sad -> Porto - 2019-02-10 20:55>, 'Direct')", "(<Flight: FTN AIR - Novi Sad -> Porto - 2019-02-10 18:04>, 'Direct')"])

    def test_avio_seach_results_filter_by_avio_company(self):
        self.client.login(username="Orion", password="wdvhu098")
        context = {}
        context['sort'] = "4" # sortiranje po trajanju
        context["avio_company"] = "1" # ftn air
        context["fly_type"] = ""
        context['arrival_date'] = "2019-02-19"
        context["departure_date"] = "2019-02-10"
        context["departure_city"] = "1"
        context["arrival_city"] = "7"
        context["passenger_numbers"] = "1"
        context["seat"] = "Economy"
        context["trip_type"] = "One-way"
        response = self.client.get(reverse('avio:search_results_avio'),data=context)
        response = self.client.post(reverse('avio:search_results_avio'),data=context)
        self.assertQuerysetEqual(response.context['ret'], ["(<Flight: FTN AIR - Novi Sad -> Porto - 2019-02-10 18:04>, 'Direct')"])

    # test rezervacije sedista
    def test_avio_seach_reserve_ticket(self):
        user = self.client.login(username="Orion", password="wdvhu098")

        # karta sa pk = 39 pre ovoga ne postoji
        self.assertQuerysetEqual(Ticket.objects.filter(pk = 39), [])
        old_len = len(Ticket.objects.all())

        # paket sa pk = 11 ne postoji
        self.assertQuerysetEqual(PackageReservation.objects.filter(pk = 11), [])
        num_of_pac = len(PackageReservation.objects.all())

        context = {}
        context['arrival_date'] = "2019-02-19"
        context["departure_date"] = "2019-02-10"
        context["departure_city"] = "1"
        context["arrival_city"] = "7"
        context["passenger_numbers"] = "1"
        context["seat"] = "Economy"
        context["trip_type"] = "One-way"
        response = self.client.get(reverse('avio:search_results_avio'),data=context)

        response = self.client.get(reverse('avio:avio_reservation', kwargs={'flight_id': 15}))
        
        context["passport"] = 123456
        context["seats"] = 1
        context["first_name"] = "Orion"
        context["last_name"] = "Strelac"
        context["seats"] = 695
        response = self.client.post(reverse('avio:avio_reservation',kwargs={'flight_id': 15}), data=context)

        # postoji 1 vise objekat karata
        self.assertEqual(old_len + 1,len(Ticket.objects.all()))

        # pasos vezan za kartu je 123456
        self.assertEqual(Ticket.objects.get(pk = 39).passport, '123456')

        # sediste pk 695 vezano za kartu- sediste 13 Economy klase
        self.assertEqual(Ticket.objects.get(pk = 39).seat.id, 695)

        # sediste pk 695 vezano za kartu - je promenjeno u zauzeto
        self.assertEqual(Ticket.objects.get(pk = 39).seat.seat_status, "T")

        # let pk 15 je vezan za kreiranu kartu
        self.assertEqual(Ticket.objects.get(pk = 39).flight.id, 15)

        # ime vezano za kartu je Orion
        self.assertEqual(Ticket.objects.get(pk = 39).first_name, "Orion")

        # prezime vezano za kartu je Strelac
        self.assertEqual(Ticket.objects.get(pk = 39).last_name, "Strelac")

        # status karte je kupljen
        self.assertEqual(Ticket.objects.get(pk = 39).status, "B")

        # user vezan za kartu je Orion koji je logovan
        self.assertEqual(Ticket.objects.get(pk = 39).user, response.wsgi_request.user)


        # postoji 1 vise objekat karata
        self.assertEqual(num_of_pac + 1, len(PackageReservation.objects.all()))

        # master user paketa pk 11 je Orion logovani user
        self.assertEqual(PackageReservation.objects.get(pk = 11).master_user, response.wsgi_request.user)

        # date from u paket je iz prve forme u searcu
        dat = datetime.date(2019, 2, 10)
        self.assertEqual(PackageReservation.objects.get(pk = 11).date_from.date(), dat)

        # date to u paket je iz prve forme u searcu
        dat = datetime.date(2019, 2, 19)
        self.assertEqual(PackageReservation.objects.get(pk = 11).date_to.date(), dat)

        # grad je sa pk 7 sto je prosledjen u search formi kao destinacija
        city_name = City.objects.get(pk = 7).name
        self.assertEqual(PackageReservation.objects.get(pk = 11).city, city_name)


        # aktivan paket u useru je postao novostvoreni paket pk 11
        self.assertEqual(response.wsgi_request.user.profile.active_package, PackageReservation.objects.get(pk = 11))



        






    


















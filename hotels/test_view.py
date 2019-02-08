from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.contrib.auth.models import User, Permission
from django.contrib.auth import authenticate
from seleniumlogin import force_login
from .models import *
from avio.models import PackageReservation
from user.models import User, Profile, DiscountPointReference
from datetime import datetime, timedelta
from selenium.webdriver.support.ui import Select


class HotelSeleniumTestCase(LiveServerTestCase):
    def setUp(self):
        self.selenium = webdriver.Chrome()

        self.admin = User.objects.create(
            username='admin', email='admin@test.com', password='passtest', is_active=True)
        self.admin.user_permissions.add(
            Permission.objects.get(name='Is hotel admin'))
        self.admin.save()

        self.user = User.objects.create(
            username='test1', email='test1@test.com', password='passtest', is_active=True)
        self.profile = Profile.objects.create(
            user=self.user, city='Novi Sad', phone_number='021333444', bonus=2)
        self.user.save()

        self.hotel = Hotel(name='Test', country="Testonia", city="Testville", address="Test drive",
                           address_number=1, description="Test description.", admin=self.admin)
        self.hotel.save()

        self.room = HotelRoom(hotel=self.hotel, name="TestRoom", number=1,
                              floor_number=1, capacity=2, has_balcony=True, default_price_per_day=100)
        self.room.save()

        self.service = HotelService(hotel=self.hotel, name="TestService",
                                    price=10, type_of_charge=HotelService.PER_PERSON_PER_DAY)
        self.service.save()

        self.package = PackageReservation(master_user=self.user, date_from=datetime.now(
        ), date_to=datetime.date.today() + datetime.timedelta(days=7), country='Serbia', city='Novi Sad')
        self.package.save()
        self.user.profile.active_package = self.package
        self.user.profile.save()

        self.discount = DiscountPointReference()
        self.discount.save()

        def tearDown(self):
            self.selenium.quit()

        def test_reservation_scenario(self):
            selenium = self.selenium
            force_login(self.user, selenium, self.live_server_url)

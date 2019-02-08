from django.test import TestCase
from .models import Hotel, HotelRoom, HotelService, HotelRate
from user.models import User, Profile, AdminUser
from datetime import datetime
from datetime import timedelta
from django.db import DatabaseError
from django.core.exceptions import ValidationError


class HotelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='test', email='test@test.com', is_active=True)
        self.profile = Profile.objects.create(user=self.user, city='Novi Sad', phone_number='021333444', bonus=2)
        self.user.set_password('Test1234')
        self.user.save()

        self.admin = User.objects.create(username='admin', email='admin@test.com', is_active=True)
        self.admin_user = AdminUser.objects.create(user=self.admin, admin_type='hotel', first_login=False)

        self.hotel = Hotel(name='Test', country="Testonia", city="Testville", address="Test drive", address_number=1, description="Test description.", admin=self.admin)
        self.hotel.save()

        self.hotel_room = HotelRoom(hotel=self.hotel, name="TestRoom", number=1, floor_number=1, capacity=2, has_balcony=True, default_price_per_day=100)
        self.hotel_room.save()

        self.hotel_service = HotelService(hotel=self.hotel, name="TestService", price=10, type_of_charge=HotelService.PER_PERSON_PER_DAY)
        self.hotel_service.save()

    def test_hotel_in_database(self):
        self.assertEqual(Hotel.objects.count(), 1)
        admin = User.objects.create(username='admin1', email='admin1@test1.com', is_active=True)
        admin.save()
        hotel = Hotel(name='Test1', country="Testonia1", city="Testville1", address="Test drive1", address_number=2, description="Test description.1", admin=admin)
        hotel.save()
        self.assertEqual(Hotel.objects.count(), 2)

    def test_room_in_database(self):
        self.assertEqual(HotelRoom.objects.count(), 1)
        room = HotelRoom(hotel=self.hotel, name="TestRoom1", number=2, floor_number=1, capacity=2, has_balcony=True, default_price_per_day=100)
        room.save()
        self.assertEqual(HotelRoom.objects.count(), 2)

    def test_service_in_database(self):
        self.assertEqual(HotelService.objects.count(), 1)
        service = HotelService(hotel=self.hotel, name="TestService1", price=11, type_of_charge=HotelService.PER_PERSON_PER_DAY)
        service.save()
        self.assertEqual(HotelService.objects.count(), 2)

    def test_hotel_tostr(self):
        self.assertEqual(str(self.hotel), 'Test')
    
    def test_room_tostr(self):
        self.assertEqual(str(self.hotel_room), 'Hotel Test | Room no 1')
    
    def test_service_tostr(self):
        self.assertEqual(str(self.hotel_service), 'Test|TestService')

    def test_room_number_unique(self):
        room = HotelRoom(hotel=self.hotel, name="TestRoom1", number=1, floor_number=1, capacity=2, has_balcony=True, default_price_per_day=100)
        with self.assertRaises(DatabaseError):
            room.save()

    def test_hotel_admin_unique(self):
        hotel = Hotel(name='Test1', country="Testonia1", city="Testville1", address="Test drive1", address_number=2, description="Test description 1", admin=self.admin)
        with self.assertRaises(DatabaseError):
            hotel.save()

    def test_room_clean1(self):
        room = HotelRoom(hotel=self.hotel, name="TestRoom1", number=2, floor_number=1, capacity=2, has_balcony=True, default_price_per_day=-1.0)
        with self.assertRaises(ValidationError):
            room.clean()

    def test_room_clean2(self):
        room = HotelRoom(hotel=self.hotel, name="TestRoom1", number=2, floor_number=1, capacity=0, has_balcony=True, default_price_per_day=1.0)
        with self.assertRaises(ValidationError):
            room.clean()

    def test_service_clean(self):
        service = HotelService(hotel=self.hotel, name="TestService", price=-1, type_of_charge=HotelService.PER_PERSON_PER_DAY)
        with self.assertRaises(ValidationError):
            service.clean()

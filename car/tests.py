from django.test import TestCase
from .models import Service
from .models import Car
from .models import BranchOffice
from .models import Reservation
from user.models import User
from datetime import datetime
from datetime import timedelta

import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)

class CarTestCase(TestCase):
    def setUp(self):
      self.user = User.objects.create(username='test', email='test@test.com', is_active=True)
      self.user.set_password('Test1234')
      self.user.save()

      self.service = Service(name='testService', promo_description='someDesc', country='SRB', city='Novi Sad', address='Street', number='123')
      self.service.save()

      self.car = Car(name='testCar', service=self.service, manufacturer='1', model='someModel', car_type='1', price=123.45, year=2001, seats=3)
      self.car.save()

      self.office = BranchOffice(name='testOffice', service=self.service, country='SRB', city='Novi Sad', address='Street 2', number='6')
      self.office.save()

      self.reservation = Reservation(car = self.car, office1 = self.office, office2 = self.office, date1 = (datetime.now()).replace(tzinfo=None), date2 = (datetime.now() + timedelta(days=2)).replace(tzinfo=None), user = self.user)
      self.reservation.save()

    def test_service_in_database(self):
      self.assertEqual(Service.objects.all().count(), 1)
      service = Service(name='testService1', promo_description='someDesc', country='SRB', city='Novi Sad', address='Street', number='123')
      service.save()
      self.assertEqual(Service.objects.all().count(), 2)

    def test_car_in_database(self):
      self.assertEqual(Car.objects.all().count(), 1)
      car = Car(name='testCar1', service=self.service, manufacturer='1', model='someModel', car_type='1', price=123.45, year=2001, seats=3)
      car.save()
      self.assertEqual(Car.objects.all().count(), 2)

    def test_office_in_database(self):
      self.assertEqual(BranchOffice.objects.all().count(), 1)
      office = BranchOffice(name='testService1', service=self.service, country='SRB', city='Novi Sad', address='Street 2', number='6')
      office.save()
      self.assertEqual(BranchOffice.objects.all().count(), 2)

    def test_service_str(self):
      self.assertEqual(self.service.__str__(), 'testService')

    def test_car_str(self):
      self.assertEqual(self.car.__str__(), 'testCar (testService)')
    
    def test_office_str(self):
      self.assertEqual(self.office.__str__(), 'testOffice (testService)')

    def test_car_taken_default(self):
      self.car.is_taken = 0
      self.assertEqual(self.car.is_taken, 0)

    def test_car_taken(self):
      self.car.is_taken = 1
      self.assertEqual(self.car.is_taken, 1)

    def test_car_is_car_taken1(self):
      self.car.is_car_taken(datetime.now() - timedelta(days=10), datetime.now() - timedelta(days=4))
      self.assertEqual(self.car.is_taken, 0)

    def test_car_is_car_taken2(self):
      self.car.is_car_taken(datetime.now() - timedelta(days=10), datetime.now() + timedelta(days=1))
      self.assertEqual(self.car.is_taken, 1)

    def test_car_is_car_taken3(self):
      self.car.is_car_taken(datetime.now() - timedelta(days=10), datetime.now() + timedelta(days=4))
      self.assertEqual(self.car.is_taken, 1)

    def test_car_is_car_taken4(self):
      self.car.is_car_taken(datetime.now(), datetime.now() + timedelta(days=1))
      self.assertEqual(self.car.is_taken, 1)

    def test_car_is_car_taken5(self):
      self.car.is_car_taken(datetime.now() + timedelta(days=1), datetime.now() + timedelta(days=4))
      self.assertEqual(self.car.is_taken, 1)

    def test_car_is_car_taken6(self):
      self.car.is_car_taken(datetime.now() + timedelta(days=3), datetime.now() + timedelta(days=4))
      self.assertEqual(self.car.is_taken, 0)

    def test_car_is_reserved1(self):
      self.car.is_reserved(datetime.now() - timedelta(days=3))
      self.assertEqual(self.car.is_taken, 1)

    def test_car_is_reserved2(self):
      self.car.is_reserved(datetime.now() + timedelta(days=3))
      self.assertEqual(self.car.is_taken, 0)
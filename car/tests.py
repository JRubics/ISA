from django.test import TestCase
from .models import Service
from .models import Car
from .models import BranchOffice

class CarTestCase(TestCase):
    def setUp(self):
      self.service = Service(name='testService', promo_description='someDesc', country='SRB', city='Novi Sad', address='Street', number='123')
      self.service.save()

      self.car = Car(name='testCar', service=self.service, manufacturer='1', model='someModel', car_type='1', price=123.45, year=2001, seats=3)
      self.car.save()

      self.office = BranchOffice(name='testOffice', service=self.service, country='SRB', city='Novi Sad', address='Street 2', number='6')
      self.office.save()

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
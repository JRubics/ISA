from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.contrib.auth.models import User, Permission
from django.contrib.auth import authenticate
from seleniumlogin import force_login
from .models import Service
from .models import Car
from .models import BranchOffice
from selenium.webdriver.support.ui import Select

class CarSeleniumTestCase(LiveServerTestCase):
    def setUp(self):
      self.selenium = webdriver.Chrome()

      self.user = User.objects.create(username='test', email='test@test.com',password='passtest', is_active=True)
      self.user.user_permissions.add(Permission.objects.get(name='Is car admin'))
      self.user.save()

      self.service = Service(name='testService', promo_description='someDesc', country='SRB', city='Novi Sad', address='Street', number='123')
      self.service.save()

      self.car = Car(name='testCar', service=self.service, manufacturer='1', model='someModel', car_type='1', price=123.45, year=2001, seats=3)
      self.car.save()

      self.office = BranchOffice(name='testOffice', service=self.service, country='SRB', city='Novi Sad', address='Street 2', number='6')
      self.office.save()

    def tearDown(self):
      self.selenium.quit()

    def test_car_home(self):
      selenium = self.selenium
      selenium.get(self.live_server_url + "/car/home")
      assert 'LOGIN' in selenium.page_source

    def test_car_home_with_user(self):
      selenium = self.selenium
      force_login(self.user, selenium, self.live_server_url)
      selenium.get(self.live_server_url + "/car/home")

      assert 'car/home' in selenium.current_url

    def test_car_new_service(self):
      selenium = self.selenium
      force_login(self.user, selenium, self.live_server_url)
      selenium.get(self.live_server_url + "/car/service")

      selenium.find_element_by_name('name').send_keys('servicename')
      selenium.find_element_by_name('country').send_keys('Serbia')
      selenium.find_element_by_name('city').send_keys('Belgrade')
      selenium.find_element_by_name('address').send_keys('Asd fgh')
      selenium.find_element_by_name('number').send_keys('3')
      selenium.find_element_by_name('promo_description').send_keys('promo text')

      selenium.find_element_by_name('add_service').click()

      assert 'car/home' in selenium.current_url
      assert 'servicename' in selenium.page_source
      assert 'Serbia' in selenium.page_source
      assert 'Belgrade' in selenium.page_source
      assert 'Asd fgh' in selenium.page_source
      assert '3' in selenium.page_source
      assert 'promo text' in selenium.page_source

    def test_car_edit_service(self):
      selenium = self.selenium
      force_login(self.user, selenium, self.live_server_url)
      selenium.get(self.live_server_url + "/car/service/" + str(self.service.id))

      selenium.find_element_by_name('name').clear()
      selenium.find_element_by_name('name').send_keys('testService1')
      selenium.find_element_by_name('country').clear()
      selenium.find_element_by_name('country').send_keys('HU')
      selenium.find_element_by_name('city').clear()
      selenium.find_element_by_name('city').send_keys('Budapest')
      selenium.find_element_by_name('address').clear()
      selenium.find_element_by_name('address').send_keys('Street 2')
      selenium.find_element_by_name('number').clear()
      selenium.find_element_by_name('number').send_keys('33')
      selenium.find_element_by_name('promo_description').clear()
      selenium.find_element_by_name('promo_description').send_keys('someDesc 1')

      selenium.find_element_by_name('save').click()

      assert 'car/service' in selenium.current_url
      assert 'testService1' in selenium.page_source
      assert 'HU' in selenium.page_source
      assert 'Budapest' in selenium.page_source
      assert 'Street 2' in selenium.page_source
      assert '33' in selenium.page_source
      assert 'someDesc 1' in selenium.page_source

    def test_car_new_car(self):
      selenium = self.selenium
      force_login(self.user, selenium, self.live_server_url)
      selenium.get(self.live_server_url + "/car/add/" + str(self.service.id))

      selenium.find_element_by_name('name').send_keys('car1')
      selenium.find_element_by_name('model').send_keys('Model')

      select = Select(selenium.find_element_by_name('manufacturer_select'))
      select.select_by_value('1')
      select = Select(selenium.find_element_by_name('type_select'))
      select.select_by_value('2')

      selenium.find_element_by_name('price').send_keys('1000')
      selenium.find_element_by_name('year').send_keys('2012')
      selenium.find_element_by_name('seats').send_keys('4')

      selenium.find_element_by_name('add_car').click()

      assert 'car/service' in selenium.current_url
      assert 'car1' in selenium.page_source
      assert 'Model' in selenium.page_source
      assert 'Reno' in selenium.page_source
      assert 'Big car' in selenium.page_source
      assert '1000' in selenium.page_source
      assert '2012' in selenium.page_source
      assert '4' in selenium.page_source

    def test_car_edit_car(self):
      selenium = self.selenium
      force_login(self.user, selenium, self.live_server_url)
      selenium.get(self.live_server_url + "/car/edit/" + str(self.car.id))

      selenium.find_element_by_name('name').clear()
      selenium.find_element_by_name('name').send_keys('car1 name')
      selenium.find_element_by_name('model').clear()
      selenium.find_element_by_name('model').send_keys('Model 2')

      select = Select(selenium.find_element_by_name('manufacturer_select'))
      select.select_by_value('4')
      select = Select(selenium.find_element_by_name('type_select'))
      select.select_by_value('3')

      selenium.find_element_by_name('price').clear()
      selenium.find_element_by_name('price').send_keys('2000')
      selenium.find_element_by_name('year').clear()
      selenium.find_element_by_name('year').send_keys('2008')
      selenium.find_element_by_name('seats').clear()
      selenium.find_element_by_name('seats').send_keys('5')
     
      selenium.find_element_by_name('edit_car').click()

      assert 'car/service' in selenium.current_url
      assert 'car1 name' in selenium.page_source
      assert 'Model 2' in selenium.page_source
      assert 'Fiat' in selenium.page_source
      assert 'Truck' in selenium.page_source
      assert '2000' in selenium.page_source
      assert '2008' in selenium.page_source
      assert '5' in selenium.page_source

    def test_car_new_office(self):
      selenium = self.selenium
      force_login(self.user, selenium, self.live_server_url)
      selenium.get(self.live_server_url + "/car/office/" + str(self.service.id))

      selenium.find_element_by_name('name').send_keys('office name')
      selenium.find_element_by_name('country').send_keys('Serbia')
      selenium.find_element_by_name('city').send_keys('NS')
      selenium.find_element_by_name('address').send_keys('addr')
      selenium.find_element_by_name('number').send_keys('34')

      selenium.find_element_by_name('add_office').click()

      assert 'car/service' in selenium.current_url
      assert 'office name' in selenium.page_source
      assert 'Serbia' in selenium.page_source
      assert 'NS' in selenium.page_source
      assert 'addr' in selenium.page_source
      assert '34' in selenium.page_source

    def test_car_edit_office(self):
      selenium = self.selenium
      force_login(self.user, selenium, self.live_server_url)
      selenium.get(self.live_server_url + "/car/office/edit/" + str(self.office.id))

      selenium.find_element_by_name('name').clear()
      selenium.find_element_by_name('name').send_keys('office name 1')
      selenium.find_element_by_name('country').clear()
      selenium.find_element_by_name('country').send_keys('GB')
      selenium.find_element_by_name('city').clear()
      selenium.find_element_by_name('city').send_keys('London')
      selenium.find_element_by_name('address').clear()
      selenium.find_element_by_name('address').send_keys('addr 1')
      selenium.find_element_by_name('number').clear()
      selenium.find_element_by_name('number').send_keys('4')

      selenium.find_element_by_name('edit_office').click()

      assert 'car/service' in selenium.current_url
      assert 'office name 1' in selenium.page_source
      assert 'GB' in selenium.page_source
      assert 'London' in selenium.page_source
      assert 'addr 1' in selenium.page_source
      assert '4' in selenium.page_source
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import Profile

class UserSeleniumTestCase(LiveServerTestCase):
    def setUp(self):
      self.selenium = webdriver.Chrome()

      self.user = User.objects.create(username='test', email='test@test.com', is_active=True)
      self.profile = Profile.objects.create(user=self.user, city='Novi Sad', phone_number='021333444', bonus=2)
      self.user.set_password('Test1234')
      self.user.save()

    def tearDown(self):
      self.selenium.quit()


    def test_login_fail(self):
      selenium = self.selenium
      selenium.get(self.live_server_url + "/user/login")

      selenium.find_element_by_name('email').send_keys('some@email.com')
      selenium.find_element_by_name('password').send_keys('some pass')
      selenium.find_element_by_name('login').click()

      assert 'ERROR: Not a user' in selenium.page_source

    def test_login(self):
      selenium = self.selenium
      selenium.get(self.live_server_url + "/user/login")

      selenium.find_element_by_name('email').send_keys(self.user.email)
      selenium.find_element_by_name('password').send_keys('Test1234')
      selenium.find_element_by_name('login').click()

      assert 'user/home' in selenium.current_url

    def test_login_invalid_email(self):
      selenium = self.selenium
      selenium.get(self.live_server_url + "/user/login")

      selenium.find_element_by_name('email').send_keys('invalid_email')
      selenium.find_element_by_name('password').send_keys('Test1234')
      selenium.find_element_by_name('login').click()

      assert 'user/login' in selenium.current_url

    # da ne bi svaki put slalo email na random adresu
    # def test_register(self):
    #   selenium = self.selenium
    #   selenium.get(self.live_server_url + "/user/register")

    #   selenium.find_element_by_name('username').send_keys('username')
    #   selenium.find_element_by_name('email').send_keys('isa2018bfj@gmail.com')
    #   selenium.find_element_by_name('password1').send_keys('Test1234')
    #   selenium.find_element_by_name('password2').send_keys('Test1234')
    #   selenium.find_element_by_name('first_name').send_keys('first name')
    #   selenium.find_element_by_name('last_name').send_keys('last name')
    #   selenium.find_element_by_name('city').send_keys('Novi Sad')
    #   selenium.find_element_by_name('phone_number').send_keys('+38165123456')
    #   selenium.find_element_by_name('sign_in').click()

    #   assert 'An email has been sent to you. Please confirm.' in selenium.page_source
    #   assert 'user/confirmation/' in selenium.current_url

    def test_register_username(self):
      selenium = self.selenium
      selenium.get(self.live_server_url + "/user/register")

      selenium.find_element_by_name('username').send_keys(self.user.username)
      selenium.find_element_by_name('email').send_keys('email@test.test')
      selenium.find_element_by_name('password1').send_keys('Test1234')
      selenium.find_element_by_name('password2').send_keys('Test1234')
      selenium.find_element_by_name('first_name').send_keys('first name')
      selenium.find_element_by_name('last_name').send_keys('last name')
      selenium.find_element_by_name('city').send_keys('Novi Sad')
      selenium.find_element_by_name('phone_number').send_keys('+38165123456')
      selenium.find_element_by_name('sign_in').click()

      assert 'ERROR: Username already exists' in selenium.page_source

    def test_register_email(self):
      selenium = self.selenium
      selenium.get(self.live_server_url + "/user/register")

      selenium.find_element_by_name('username').send_keys('username')
      selenium.find_element_by_name('email').send_keys(self.user.email)
      selenium.find_element_by_name('password1').send_keys('Test1234')
      selenium.find_element_by_name('password2').send_keys('Test1234')
      selenium.find_element_by_name('first_name').send_keys('first name')
      selenium.find_element_by_name('last_name').send_keys('last name')
      selenium.find_element_by_name('city').send_keys('Novi Sad')
      selenium.find_element_by_name('phone_number').send_keys('+38165123456')
      selenium.find_element_by_name('sign_in').click()

      assert 'ERROR: Email already exists' in selenium.page_source

    def test_logout(self):
      selenium = self.selenium
      selenium.get(self.live_server_url + "/user/logout")

      assert 'user/login' in selenium.current_url

    def test_user_home(self):
      selenium = self.selenium
      selenium.get(self.live_server_url + "/user/home")

      assert 'user/login' in selenium.current_url
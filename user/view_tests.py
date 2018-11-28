from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import Profile

class UserSeleniumTestCase(LiveServerTestCase):
    def setUp(self):
      self.selenium = webdriver.Firefox()

      self.user = User.objects.create(username='test', email='test@test.com', is_active=True)
      self.profile = Profile.objects.create(user=self.user, city='Novi Sad', phone_number='021333444')
      self.user.set_password('Test1234')
      self.user.save()

    def tearDown(self):
      self.selenium.quit()

    def test_login(self):
      selenium = self.selenium
      selenium.get('http://127.0.0.1:8000/user/login/')
      email = selenium.find_element_by_id('login_email')
      password = selenium.find_element_by_id('login_pass')
      submit = selenium.find_element_by_name('login')

      email.send_keys('some@email.com')
      password.send_keys('some pass')
      submit.click()
      assert 'ERROR: Not a user' in selenium.page_source
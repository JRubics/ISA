from django.test import TestCase
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

class UserTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='test', email='test@test.com', is_active=True)
        self.user.set_password('Test1234')
        self.user.save()

    def test_login(self):
        self.user = authenticate(username='test', password='Test1234')
        if self.user is not None:
            self.user = User.objects.get(username='test')
            self.login = self.client.login(username='test', password='Test1234')
            self.assertEqual(self.login, True)
            print("Login successful")
        else:
            print("Login failed")

    def test_authenticate_negative(self):
        self.user = authenticate(username='testfalse', password='TestFalse')
        self.assertEqual(self.user, None)

from django.test import TestCase
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import Profile

class UserTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='test', email='test@test.com', is_active=True)
        self.profile = Profile.objects.create(user=self.user, city='Novi Sad', phone_number='021333444')
        self.user.set_password('Test1234')
        self.user.save()

    def test_login(self):
        self.user = authenticate(username='test', password='Test1234')
        if self.user is not None:
            self.user = User.objects.get(username='test')
            self.login = self.client.login(username='test', password='Test1234')
            self.assertEqual(self.login, True)
        else:
            assert False

    def test_authenticate_negative(self):
        self.user = authenticate(username='testfalse', password='TestFalse')
        self.assertEqual(self.user, None)

    def test_get_username_from_email(self):
        email = self.user.email
        username = Profile.get_username_from_email(email)
        self.assertEqual(username, self.user.username)

    def test_validate_user_same_username(self):
        username = self.user.username
        message = Profile.validate_user(username, 'test1@email.com', 'pass', 'pass')
        self.assertEqual(message, 'Username already exists')

    def test_validate_password(self):
        message = Profile.validate_user('name', 'test1@email.com', 'pass1', 'pass2')
        self.assertEqual(message, 'Passwords must be same')

    def test_validate_user_pass(self):
        message = Profile.validate_user('name', 'test1@email.com', 'pass', 'pass')
        self.assertEqual(message, None)
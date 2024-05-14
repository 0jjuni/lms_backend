import os
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status

User = get_user_model()

class UserTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')  # Assuming you have named your RegisterView as 'register' in your urls
        self.token_url = reverse('token_obtain_pair')  # Assuming you have named your MyTokenObtainPairView as 'token_obtain_pair' in your urls
        self.change_password_url = reverse('change_password')  # Assuming you have named your ChangePasswordView as 'change_password' in your urls
        self.user_data = {
            'enrollment_number': '123456789',
            'first_name': 'John',
            'last_name': 'Doe',
            'password': 'TestPassword123!',
            'password2': 'TestPassword123!',
            'user_type': 'S'
        }

    def test_register_user(self):
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(enrollment_number='123456789').exists())

    def test_login_user(self):
        # Register the user first
        self.client.post(self.register_url, self.user_data, format='json')
        login_data = {
            'enrollment_number': '123456789',
            'password': 'TestPassword123!'
        }
        response = self.client.post(self.token_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_change_password(self):
        # Register the user first
        self.client.post(self.register_url, self.user_data, format='json')
        user = User.objects.get(enrollment_number='123456789')
        self.client.force_login(user)
        change_password_data = {
            'old_password': 'TestPassword123!',
            'password': 'NewTestPassword123!',
            'password2': 'NewTestPassword123!'
        }
        response = self.client.put(self.change_password_url, change_password_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        user.refresh_from_db()
        self.assertTrue(user.check_password('NewTestPassword123!'))

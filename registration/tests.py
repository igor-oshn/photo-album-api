import os
import io

from PIL import Image
from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token


class UserTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username='Test', is_active=True)
        cls.user.set_password('Azds213123')
        cls.user.save()
        cls.token = Token.objects.create(user=cls.user)

    def test_user_token_auth_valid(self):
        """
        Ensure we can authenticate Test user and get token.
        """
        url = reverse('api-token-auth')
        data = {'username': 'Test', 'password': 'Azds213123'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['token'], str(self.token))

    def test_create_user_valid(self):
        """
        Ensure we can create a new user.
        """
        url = reverse('user-register')
        data = {'email': 'test@test.com', 'username': 'Test2', 'password': 'Azds213123', 'is_active': True}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(User.objects.last().username, 'Test2')

    def test_create_user_without_name(self):
        """
        Ensure we can't create a new user without username.
        """
        url = reverse('user-register')
        data = {'email': 'test@test.com', 'username': '', 'password': 'Azds213123'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)

    def test_create_user_without_email(self):
        """
        Ensure we can't create a new user without email.
        """
        url = reverse('user-register')
        data = {'email': '', 'username': 'User12356', 'password': 'Azds213123'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)

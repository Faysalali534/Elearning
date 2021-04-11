import io
import requests
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from django.urls import reverse
from rest_framework.parsers import JSONParser
from rest_framework.test import APITestCase, APIClient


class TestUserRetrieve(APITestCase):
    user_profile_list_url = reverse('restapi:user_list_api')
    client = APIClient()

    def setUp(self):
        data = {
            "email": "django@gmail.com",
            "username": "django",
            "password": "Vend1213",
            "first_name": "django",
            "last_name": "unchained",
        }
        headers = {
            'Content-Type': 'application/json',
        }

        user_data = requests.post('http://127.0.0.1:8002/auth/users/', json=data, headers=headers)

        # fetch jwt token
        response = requests.post('http://127.0.0.1:8002/auth/jwt/create/', json={
            'username': 'django',
            'password': 'Vend1213',
        }, headers=headers)
        stream = io.BytesIO(response.content)
        pythondata = JSONParser().parse(stream)

        self.token = pythondata['access']
        self.api_authentication()

        return super().setUp()

    def tearDown(self):
        return super().tearDown()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_user_profile_list_authenticated(self):
        response = requests.get('http://127.0.0.1:8002/restapi/' + self.user_profile_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_profile_list_unauthenticated(self):
        if User.objects.get(user=None):
            pass
        else:
            response = requests.get('http://127.0.0.1:8002/restapi/' + self.user_profile_list_url)
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_retrieve_api(self):
        response = requests.get('http://127.0.0.1:8002/restapi/' + reverse('restapi:user_retrieve_api', kwargs={'pk': 4}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

def test_created_user_profile_set(self):
    user_profile_data = {'phone_number': '03204432250', 'location': 'Liberty gate',
                         'user_type': 'student'}
    response = self.client.post('')

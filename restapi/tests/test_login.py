from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase


class LoginApiTestCase(APITestCase):
    login_url = reverse('restapi:login_api_view')
    register_url = reverse('restapi:list_create_api_view')

    def test_login_user_successfully(self):
        user = User.objects.create_user(
            first_name="django2",
            username="django2",
            email="django2@gmail.com",
            last_name="unchained",
            password="Vend1213",
        )
        data = {
            "username": "django2",
            "password": "Vend1213",
        }

        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_login_user_without_data(self):
        response = self.client.post(self.login_url)
        self.assertEqual(response.status_code, 400)

    def test_login_user_with_wrong_credentials(self):
        data = {
            "username": "django90",
            "password": "Vend1213",
        }

        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, 400)

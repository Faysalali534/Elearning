from django.urls import reverse
from rest_framework.test import APITestCase


class RegisterAPITestCase(APITestCase):
    register_url = reverse('restapi:list_create_api_view')

    def test_user_registration_successfully(self):
        data = {
            "user": {
                "first_name": "django2",
                "username": "django2",
                "email": "django2@gmail.com",
                "last_name": "unchained",
                "password": "Vend1213",
            },
            "phone_number": "03204432250",
            "location": "Liberty Gate",
            "user_type": "student",
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_user_registration_without_data(self):
        response = self.client.post(self.register_url)
        self.assertEqual(response.status_code, 400)

    def test_user_registration_with_already_existing_data(self):
        data = {
            "user": {
                "first_name": "django2",
                "username": "django2",
                "email": "django2@gmail.com",
                "last_name": "unchained",
                "password": "Vend1213",
            },
            "phone_number": "03204432250",
            "location": "Liberty Gate",
            "user_type": "student",
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, 201)

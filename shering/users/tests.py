from time import sleep
from django.conf import settings
from django.test import override_settings
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status


class UsersTest(APITestCase):
    URL = reverse("registration")

    def test_create_user_ok(self):
        credentials = {"phone": "+123456789"}
        response = self.client.post(self.URL, credentials)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_user_again(self):
        credentials = {"phone": "+123456789"}
        output = {"phone": ["user with this phone already exists."]}
        self.client.post(self.URL, credentials)
        response = self.client.post(self.URL, credentials)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(response.json(), output)

    def test_create_user_with_invalid_creds(self):
        credentials = {"phone": "lorem ipsum"}
        output = {
            "phone": [
                "Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
            ]
        }
        response = self.client.post(self.URL, credentials)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(response.json(), output)

    @override_settings(CODE_RESEND_TIMEOUT=0.1)
    def test_update_code_ok(self):
        credentials = {"phone": "+123456789"}
        self.client.post(self.URL, credentials)
        # Waiting for the timeout to pass
        sleep(0.1)
        response = self.client.put(self.URL, credentials)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_code_before_timeout_passed(self):
        credentials = {"phone": "+123456789"}
        output = [
            f"Can't send SMS earlier than {settings.CODE_RESEND_TIMEOUT} seconds after previous"
        ]
        self.client.post(self.URL, credentials)
        response = self.client.put(self.URL, credentials)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), output)

    def test_update_code_for_nonexisting_phone(self):
        credentials = {"phone": "+123456789"}
        output = ["User with this phone doesn't exist"]
        response = self.client.put(self.URL, credentials)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), output)

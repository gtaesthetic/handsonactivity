from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

class RBACAPITests(APITestCase):
    def setUp(self):
        self.hr_user = User.objects.create_user(email="hr@example.com", password="password", role="HR")
        self.employee_user = User.objects.create_user(email="employee@example.com", password="password", role="Regular Employee")

    def test_hr_can_view_roles(self):
        self.client.login(email="hr@example.com", password="password")
        response = self.client.get("/user/roles/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_employee_cannot_view_roles(self):
        self.client.login(email="employee@example.com", password="password")
        response = self.client.get("/user/roles/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

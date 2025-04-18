from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import LeaveRequest, LeaveType

User = get_user_model()

class LeavesAPITests(APITestCase):
    def setUp(self):
        self.hr_user = User.objects.create_user(email="hr@example.com", password="password", role="hr")
        self.employee_user = User.objects.create_user(email="employee@example.com", password="password", role="employee")
        self.leave_type = LeaveType.objects.create(name="Vacation")

    def test_submit_leave_request(self):
        self.client.login(email="employee@example.com", password="password")
        response = self.client.post("/leaves/submit/", {
            "leave_type": self.leave_type.id,
            "start_date": "2025-04-10",
            "end_date": "2025-04-15",
            "reason": "Family vacation"
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_approve_leave_request(self):
        leave_request = LeaveRequest.objects.create(
            employee_ID=self.employee_user,
            leave_type=self.leave_type,
            start_date="2025-04-10",
            end_date="2025-04-15",
            reason="Family vacation"
        )
        self.client.login(email="hr@example.com", password="password")
        response = self.client.post(f"/leaves/{leave_request.id}/approve_reject/", {
            "status": "approved"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_view_own_leaves(self):
        LeaveRequest.objects.create(
            employee_ID=self.employee_user,
            leave_type=self.leave_type,
            start_date="2025-04-10",
            end_date="2025-04-15",
            reason="Family vacation"
        )
        self.client.login(email="employee@example.com", password="password")
        response = self.client.get("/leaves/view/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

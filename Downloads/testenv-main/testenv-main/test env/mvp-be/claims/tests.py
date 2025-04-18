from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Claim

User = get_user_model()

class ClaimAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="user@example.com", password="password", role="employee")

    def test_submit_claim_with_new_fields(self):
        self.client.login(email="user@example.com", password="password")
        data = {
            "claim_type": "medical",
            "amount": 1000,
            "currency": "PHP",
            "bill_no": "12345",
            "bill_date": "2025-04-01",
            "supplier": "ABC Supplier",
            "claimant": "John Doe",
            "claim_date": "2025-04-01",
            "claim_due_date": "2025-04-10",
            "tax": 100,
            "tax_amount": 100,
            "discount": 50,
            "rate": 500,
            "quantity": 2,
            "item_description": "Medical claim for consultation",
            "remarks": "Urgent processing required",
        }
        response = self.client.post("/claims/new/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["total"], 1150)  # (rate * quantity) + tax_amount - discount

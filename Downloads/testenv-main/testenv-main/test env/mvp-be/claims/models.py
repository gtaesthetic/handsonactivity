from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Claim(models.Model):
    CLAIM_TYPES = [
        ("medical", "Medical"),
        ("dental", "Dental"),
        ("ope", "Out of Pocket Expenses"),
        ("transportation", "Transportation"),
        ("travel", "Travel Allowance"),
        ("meal", "Meal Allowance"),
        ("entertainment", "Entertainment Allowance"),
        ("reimbursement", "Reimbursement"),
        ("mobile", "Mobile Allowance"),
        ("others", "Others (NEC)"),
    ]

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
        ("paid", "Paid"),
    ]

    employee_ID = models.ForeignKey(User, on_delete=models.CASCADE)
    claim_type = models.CharField(max_length=50, choices=CLAIM_TYPES, default="others")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=5, choices=[("PHP", "Peso"), ("SGD", "SGD")], default="PHP")
    submission_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    is_approved = models.BooleanField(default=False)
    remarks = models.TextField(blank=True, null=True)
    proof_of_expense = models.FileField(upload_to="proofs/", blank=True, null=True)

    bill_no = models.CharField(max_length=50, blank=True, null=True)
    bill_date = models.DateField(blank=True, null=True)
    supplier = models.CharField(max_length=100, blank=True, null=True)

    claimant = models.CharField(max_length=100, blank=True, null=True)
    claim_date = models.DateField(blank=True, null=True)
    claim_due_date = models.DateField(blank=True, null=True)

    tax_rate = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=0,
        verbose_name="Tax Rate (%)",
        help_text="Tax rate as a percentage (e.g., 12 for 12%)"
    )
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    rate = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    quantity = models.IntegerField(default=1)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    item_description = models.TextField(blank=True, null=True)
    
    accrued_balance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="Accrued Balance"
    )
    
    used_balance = models.DecimalField(
        max_digits=10,
        decimal_places=2, 
        default=0,
        verbose_name="Used Balance"
    )
    
    client_name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Client Name"
    )

    def save(self, *args, **kwargs):
        # Calculate tax_amount from rate and tax_rate percentage
        self.tax_amount = (self.rate * self.quantity) * (self.tax_rate / 100)
        self.total = (self.rate * self.quantity) + self.tax_amount - self.discount
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.employee_ID} - {self.claim_type} - {self.status}"

from django.db import models
from django.contrib.auth import get_user_model
from datetime import date, timedelta

User = get_user_model()

class LeaveType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    max_days_allowed = models.IntegerField(default=0)
    requires_documentation = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class LeaveRequest(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
        ("paid", "Paid"),
        ("cancelled", "Cancelled"),
    ]

    employee_ID = models.ForeignKey(User, on_delete=models.CASCADE)
    leave_type = models.ForeignKey(LeaveType, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    total_days = models.IntegerField(default=0)  # New field for total days
    total_days_chosen = models.IntegerField(default=0)  # New field for total days chosen
    accrued = models.IntegerField(default=0)  # New field for accrued leaves
    used = models.IntegerField(default=0)  # New field for used leaves
    remaining = models.IntegerField(default=0)  # New field for remaining leaves

    def save(self, *args, **kwargs):
        # Calculate total days based on start_date and end_date
        if self.start_date and self.end_date:
            delta = (self.end_date - self.start_date).days + 1  # Include both start and end dates
            self.total_days_chosen = max(delta, 0)  # Ensure it's not negative

        # Calculate accrued leaves (1 leave every 14 days, max 14 per year)
        if self.employee_ID.date_joined:  # Assuming `date_joined` exists in User model
            days_worked = (date.today() - self.employee_ID.date_joined).days
            self.accrued = min(days_worked // 14, 14)  # Max 14 leaves per year

        # Calculate remaining leaves
        self.remaining = max(self.accrued - self.used, 0)

        super().save(*args, **kwargs)

    remarks = models.TextField(blank=True, null=True)  # New field for additional context
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    proof_of_documentation = models.FileField(upload_to="proofs/", blank=True, null=True)
    approval_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.employee_ID} - {self.leave_type} - {self.status} - {self.start_date} to {self.end_date}"

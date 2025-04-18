from rest_framework import serializers
from .models import Claim

class ClaimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Claim
        fields = "__all__"
        read_only_fields = ["id", "employee_ID", "submission_date", "status", "total"]

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")
        return value

    def validate(self, data):
        # Ensure required fields are provided
        if data.get("rate") and data.get("quantity"):
            if data["rate"] <= 0 or data["quantity"] <= 0:
                raise serializers.ValidationError("Rate and Quantity must be greater than zero.")
        return data


class ClaimApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Claim
        fields = ["status", "remarks"]
        read_only_fields = ["id", "employee_ID", "submission_date"]

    def validate_status(self, value):
        valid_statuses = ["approved", "rejected", "paid"]  # Added "paid" status
        if value not in valid_statuses:
            raise serializers.ValidationError(f"Invalid status. Choose from {', '.join(valid_statuses)}.")
        return value

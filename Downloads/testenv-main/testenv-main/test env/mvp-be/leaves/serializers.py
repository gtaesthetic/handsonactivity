from rest_framework import serializers
from .models import LeaveRequest, LeaveType

class LeaveTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveType
        fields = "__all__"


class LeaveRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveRequest
        fields = [
            'leave_type', 'start_date', 'end_date', 'reason', 
            'total_days_chosen', 'remarks', 'status', 'approval_date',
            'accrued', 'used', 'remaining'  # Added new fields
        ]
        read_only_fields = ["employee_ID", "status", "approval_date", "accrued", "remaining"]  # Marked accrued and remaining as read-only

    def validate(self, data):
        # Check for overlapping leave requests
        employee = self.context['request'].user
        start_date = data['start_date']
        end_date = data['end_date']

        overlapping_requests = LeaveRequest.objects.filter(
            employee_ID=employee,
            start_date__lt=end_date,
            end_date__gt=start_date,
            status__in=["pending", "approved"]
        )

        if overlapping_requests.exists():
            raise serializers.ValidationError("This leave request overlaps with an existing request.")

        return data


class LeaveApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveRequest
        fields = ["status", "approval_date"]

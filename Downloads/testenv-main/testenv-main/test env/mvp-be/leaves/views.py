from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from django.utils.timezone import now
from .models import LeaveRequest, LeaveType
from .serializers import LeaveRequestSerializer, LeaveApprovalSerializer
from users.permissions import RolePermission

class SubmitLeaveRequestView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = LeaveRequestSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(employee_ID=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def put(self, request, leave_id=None):
        # Handle both update and cancel operations
        is_cancel = 'cancel/' in request.path

        # Get leave ID from URL or request data
        if not leave_id:
            leave_id = request.data.get('id')
            
        if not leave_id:
            return Response({"detail": "Leave request ID is required."}, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            leave_request = LeaveRequest.objects.get(id=leave_id)
        except LeaveRequest.DoesNotExist:
            return Response({"detail": "Leave request not found."}, status=status.HTTP_404_NOT_FOUND)
            
        # Check if user is the owner of the leave request
        if leave_request.employee_ID != request.user:
            return Response({"detail": "You do not have permission to modify this leave request."}, status=status.HTTP_403_FORBIDDEN)
            
        # Only allow updates if the leave request is still pending
        if leave_request.status != "pending":
            if is_cancel and leave_request.status == "approved":
                # Allow cancellation of approved leaves
                pass
            else:
                return Response({"detail": "Only pending leave requests can be updated."}, status=status.HTTP_400_BAD_REQUEST)
        
        if is_cancel:
            # Handle cancellation
            leave_request.status = "cancelled"
            leave_request.save()
            return Response({"detail": "Leave request cancelled successfully."}, status=status.HTTP_200_OK)
        else:
            # Handle normal update
            serializer = LeaveRequestSerializer(leave_request, data=request.data, context={'request': request}, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ApproveRejectLeaveView(APIView):
    permission_classes = [permissions.IsAuthenticated, RolePermission]

    def post(self, request, leave_id):
        user = request.user
        role = user.role.lower()

        # Ensure only higher management roles can approve, reject, or pay leave requests
        if role not in ["hr", "ceo", "director", "owner"]:
            return Response({"detail": "You do not have permission to perform this action."}, status=403)

        leave_request = get_object_or_404(LeaveRequest, id=leave_id)

        # Process the request to approve, reject, or pay the leave request
        action = request.data.get("action")
        if action not in ["approve", "reject", "pay"]:
            return Response({"detail": "Invalid action. Allowed actions are 'approve', 'reject', or 'pay'."}, status=400)

        if action == "approve":
            leave_request.status = "approved"
            leave_request.approval_date = now()
        elif action == "reject":
            leave_request.status = "rejected"
        elif action == "pay":
            if leave_request.status != "approved":
                return Response({"detail": "Only approved leave requests can be paid."}, status=400)
            leave_request.status = "paid"

        leave_request.save()

        # Handle response messages for irregular verbs
        if action == "pay":
            message = "Leave request paid successfully!"
        elif action == "reject":
            message = "Leave request rejected successfully!"
        else:
            message = f"Leave request {action}d successfully!"

        return Response({"message": message}, status=200)

class ViewLeavesView(APIView):
    permission_classes = [permissions.IsAuthenticated, RolePermission]

    def get(self, request, leave_id=None, user_id=None):
        user = request.user
        role = user.role.lower()

        # If a specific leave ID is provided, return that leave
        if leave_id:
            leave = get_object_or_404(LeaveRequest, id=leave_id)
            
            # Check permissions: Only the leave owner or management can view it
            if leave.employee_ID != user and role not in ["hr", "ceo", "director", "owner", "manager", "team_lead", "supervisor"]:
                return Response({"detail": "You do not have permission to view this leave request."}, status=status.HTTP_403_FORBIDDEN)
            
            serializer = LeaveRequestSerializer(leave)
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        # If a user ID is provided, return leaves for that user
        if user_id:
            # Only management can view other users' leaves
            if str(user.id) != str(user_id) and role not in ["hr", "ceo", "director", "owner", "manager", "team_lead", "supervisor"]:
                return Response({"detail": "You do not have permission to view other users' leave requests."}, status=status.HTTP_403_FORBIDDEN)
                
            leaves = LeaveRequest.objects.filter(employee_ID=user_id)
            serializer = LeaveRequestSerializer(leaves, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # Otherwise return leaves based on role
        # Higher management roles can view all leave requests
        if role in ["hr", "ceo", "director", "owner", "manager", "team_lead", "supervisor"]:
            leaves = LeaveRequest.objects.all()

        # Regular employees can view only their own leave requests
        elif role == "employee":
            leaves = LeaveRequest.objects.filter(employee_ID=user)

        else:
            return Response({"detail": "You do not have permission to view leave requests."}, status=status.HTTP_403_FORBIDDEN)

        serializer = LeaveRequestSerializer(leaves, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

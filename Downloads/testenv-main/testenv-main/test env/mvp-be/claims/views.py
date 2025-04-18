from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import get_object_or_404
from django.db import models
from .models import Claim
from .serializers import ClaimSerializer
from users.permissions import RolePermission

class SubmitClaimView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ClaimSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(employee_ID=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def put(self, request):
        claim_id = request.data.get('id')
        if not claim_id:
            return Response({"detail": "Claim ID is required."}, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            claim = Claim.objects.get(id=claim_id)
        except Claim.DoesNotExist:
            return Response({"detail": "Claim not found."}, status=status.HTTP_404_NOT_FOUND)
            
        # Check if user is the owner of the claim
        if claim.employee_ID != request.user:
            return Response({"detail": "You do not have permission to update this claim."}, status=status.HTTP_403_FORBIDDEN)
            
        # Only allow updates if the claim is still pending
        if claim.status != "pending":
            return Response({"detail": "Only pending claims can be updated."}, status=status.HTTP_400_BAD_REQUEST)
            
        serializer = ClaimSerializer(claim, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ApproveRejectClaimView(APIView):
    permission_classes = [IsAuthenticated, RolePermission]

    def post(self, request, claim_id):
        user = request.user
        role = user.role.lower()

        # Ensure only higher management roles can approve, reject, or pay claims
        if role not in ["hr", "ceo", "director", "owner"]:
            return Response({"detail": "You do not have permission to perform this action."}, status=403)

        claim = get_object_or_404(Claim, id=claim_id)

        # Process the request to approve, reject, or pay the claim
        action = request.data.get("action")
        if action not in ["approve", "reject", "pay"]:
            return Response({"detail": "Invalid action. Allowed actions are 'approve', 'reject', or 'pay'."}, status=400)

        if action == "approve":
            claim.status = "approved"
            claim.is_approved = True
        elif action == "reject":
            claim.status = "rejected"
            claim.is_approved = False
        elif action == "pay":
            if claim.status != "approved":
                return Response({"detail": "Only approved claims can be paid."}, status=400)
            claim.status = "paid"

        claim.save()

        # Handle response messages for irregular verbs
        if action == "pay":
            message = "Claim paid successfully!"
        elif action == "reject":
            message = "Claim rejected successfully!"
        else:
            message = f"Claim {action}d successfully!"

        return Response({"message": message}, status=200)

class ViewClaimsView(APIView):
    permission_classes = [IsAuthenticated, RolePermission]

    def get(self, request, claim_id=None, user_id=None):
        user = request.user
        role = user.role.lower()

        # If a specific claim ID is provided, return that claim
        if claim_id:
            claim = get_object_or_404(Claim, id=claim_id)
            
            # Check permissions: Only the claim owner or management can view it
            if claim.employee_ID != user and role not in ["hr", "ceo", "director", "owner", "manager", "team_lead", "supervisor", "admin"]:
                return Response({"detail": "You do not have permission to view this claim."}, status=403)
            
            serializer = ClaimSerializer(claim)
            return Response(serializer.data, status=200)
            
        # If a user ID is provided, return claims for that user
        if user_id:
            # Only management can view other users' claims
            if str(user.id) != str(user_id) and role not in ["hr", "ceo", "director", "owner", "manager", "team_lead", "supervisor", "admin"]:
                return Response({"detail": "You do not have permission to view other users' claims."}, status=403)
                
            claims = Claim.objects.filter(employee_ID=user_id)
            serializer = ClaimSerializer(claims, many=True)
            return Response(serializer.data, status=200)

        # Otherwise return claims based on role
        # HR, CEO, Directors, Owners, Managers, Team Leads, Supervisors, and Admins can view all claims
        if role in ["hr", "ceo", "director", "owner", "manager", "team_lead", "supervisor", "admin"]:
            claims = Claim.objects.all()

        # Regular Employees can view only their own claims
        elif role == "employee":
            claims = Claim.objects.filter(employee_ID=user)

        else:
            return Response({"detail": "You do not have permission to view claims."}, status=403)

        serializer = ClaimSerializer(claims, many=True)
        return Response(serializer.data, status=200)

class ClaimStatisticsView(APIView):
    permission_classes = [IsAuthenticated, RolePermission]

    def get(self, request):
        # Verify user has permission to view statistics
        if not request.user.has_perm('claims.view_claim_statistics'):
            return Response({"detail": "Permission denied"}, status=403)

        # Calculate basic statistics
        total_claims = Claim.objects.count()
        pending = Claim.objects.filter(status='pending').count()
        approved = Claim.objects.filter(status='approved').count()
        paid = Claim.objects.filter(status='paid').count()
        rejected = Claim.objects.filter(status='rejected').count()

        # Calculate total amounts
        total_amount = Claim.objects.aggregate(models.Sum('amount'))['amount__sum'] or 0
        pending_amount = Claim.objects.filter(status='pending').aggregate(models.Sum('amount'))['amount__sum'] or 0
        approved_amount = Claim.objects.filter(status='approved').aggregate(models.Sum('amount'))['amount__sum'] or 0

        return Response({
            'total_claims': total_claims,
            'pending': pending,
            'approved': approved,
            'paid': paid,
            'rejected': rejected,
            'total_amount': float(total_amount),
            'pending_amount': float(pending_amount),
            'approved_amount': float(approved_amount)
        }, status=200)

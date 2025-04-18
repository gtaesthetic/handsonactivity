from rest_framework.permissions import BasePermission

class RolePermission(BasePermission):
    """
    Custom permission class to enforce role-based access control.
    """

    def has_permission(self, request, view):
        user = request.user
        role = user.role.lower()

        # Allow HR, CEO, Directors, and Owners to approve, reject, and pay claims
        if view.__class__.__name__ == "ApproveRejectClaimView" and request.method == "POST":
            return role in ["hr", "ceo", "director", "owner"]
        
        if view.__class__.__name__ == "ApproveRejectLeaveView" and request.method == "POST":
            return role in ["hr", "ceo", "director", "owner"]

        # Check if the request is for viewing claims
        if request.method == "GET" and "view" in request.path:
            # Allow HR, CEO, Directors, Owners, Managers, Team Leads, and Supervisors to view all claims
            if role in ["hr", "ceo", "director", "owner", "manager", "team_lead", "supervisor", "admin"]:
                return True

            # Allow Regular Employees to view only their own claims
            if role == "employee":
                return True

        return False

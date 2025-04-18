from rest_framework import status
from rest_framework import viewsets
from .permissions import RolePermission 
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import UserSerializer
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import get_user_model
from django.db import connection
from django.http import JsonResponse
from .roles import ROLES

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_roles(request):
    """
    Fetch all user roles and permissions.
    Restrict employees from accessing this endpoint.
    """
    user = request.user

    # Restrict employees from accessing this endpoint
    if user.role.lower() == "employee":
        return Response(
            {"detail": "You do not have permission to perform this action."},
            status=status.HTTP_403_FORBIDDEN,
        )

    roles = [
        {"role": "HR", "description": "Human Resources"},
        {"role": "CEO", "description": "Chief Executive Officer"},
        {"role": "Director", "description": "Director"},
        {"role": "Owner", "description": "Owner"},
        {"role": "Manager", "description": "Manager"},
        {"role": "Team Lead", "description": "Team Lead"},
        {"role": "Supervisor", "description": "Supervisor"},
        {"role": "Regular Employee", "description": "Employee"},
        {"role": "Administrator", "description": "Admin with limited permissions"},
    ]
    return Response(roles, status=status.HTTP_200_OK)

def test_db_connection(request):
    try:
        connection.ensure_connection()
        return JsonResponse({"message": "Database connection successful!"})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, RolePermission]

class RegisterView(APIView):
    permission_classes = [AllowAny]  # Require authentication

    def post(self, request):
        serializer = UserSerializer(data=request.data, context={"request": request})  # Pass request
        if serializer.is_valid():
            user = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(email=email, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                    "role": user.role,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                },
                status=status.HTTP_200_OK,
            )

        return Response(
            {"error": "Invalid email or password"}, 
            status=status.HTTP_401_UNAUTHORIZED
        )
    
class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh_token")
            if not refresh_token:
                return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)

            token = RefreshToken(refresh_token)
            token.blacklist()  # Blacklists the refresh token

            return Response({"message": "Successfully logged out"}, status=status.HTTP_205_RESET_CONTENT)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class UserRoleView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(ROLES, status=200)

class UserPermissionsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Debug print statements
        print("DEBUG: Request headers:", request.headers)
        print("DEBUG: Authentication info:", request.auth)
        print("DEBUG: User:", request.user)
        
        user = request.user
        role = user.role
        
        # Get permissions based on user's role
        if role in ROLES:
            permissions = ROLES[role]
            return Response(permissions, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": f"Role '{role}' not found"},
                status=status.HTTP_404_NOT_FOUND
            )

class AllRolesView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """
        Returns all available roles with descriptions
        Only accessible to admin roles (HR, CEO, Director, Owner, Administrator)
        """
        user = request.user
        role = user.role.lower()
        
        # Check if user has permission to view all roles
        admin_roles = ["hr", "ceo", "director", "owner", "administrator"]
        if role not in admin_roles:
            return Response(
                {"detail": "You do not have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN
            )
            
        roles = [
            {"role": "HR", "description": "Human Resources"},
            {"role": "CEO", "description": "Chief Executive Officer"},
            {"role": "Director", "description": "Director"},
            {"role": "Owner", "description": "Owner"},
            {"role": "Manager", "description": "Manager"},
            {"role": "Team Lead", "description": "Team Lead"},
            {"role": "Supervisor", "description": "Supervisor"},
            {"role": "Regular Employee", "description": "Employee"},
            {"role": "Administrator", "description": "Admin with limited permissions"},
        ]
        return Response(roles, status=status.HTTP_200_OK)

class AssignRoleView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """
        Assigns a role to a user
        Only accessible to admin roles (HR, CEO, Director, Owner)
        """
        user = request.user
        role = user.role.lower()
        
        # Check if user has permission to assign roles
        admin_roles = ["hr", "ceo", "director", "owner"]
        if role not in admin_roles:
            return Response(
                {"detail": "You do not have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN
            )
            
        user_id = request.data.get("user_id")
        new_role = request.data.get("role")
        
        if not user_id or not new_role:
            return Response(
                {"error": "user_id and role are required"},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        try:
            user_to_update = User.objects.get(id=user_id)
            
            # Check if the role is valid
            valid_roles = ["HR", "CEO", "Director", "Owner", "Manager", 
                          "Team Lead", "Supervisor", "Regular Employee", 
                          "Administrator"]
                          
            if new_role not in valid_roles:
                return Response(
                    {"error": f"Invalid role: {new_role}"},
                    status=status.HTTP_400_BAD_REQUEST
                )
                
            user_to_update.role = new_role
            user_to_update.save()
            
            return Response(
                {"message": f"Role updated to {new_role} for user {user_to_update.email}"},
                status=status.HTTP_200_OK
            )
            
        except User.DoesNotExist:
            return Response(
                {"error": f"User with id {user_id} not found"},
                status=status.HTTP_404_NOT_FOUND
            )
            
class CreateUserView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """
        Creates a new user
        Only accessible to admin roles (HR, CEO, Director, Owner, Administrator)
        """
        user = request.user
        role = user.role.lower()
        
        # Check if user has permission to create users
        admin_roles = ["hr", "ceo", "director", "owner", "administrator"]
        if role not in admin_roles:
            return Response(
                {"detail": "You do not have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN
            )
            
        serializer = UserSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            new_user = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """
        Returns the current user's profile information
        """
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UpdateProfileView(APIView):
    permission_classes = [IsAuthenticated]
    
    def put(self, request):
        """
        Updates the current user's profile
        """
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



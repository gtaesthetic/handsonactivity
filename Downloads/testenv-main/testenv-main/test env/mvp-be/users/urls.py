from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from .views import (
    RegisterView, LoginView, LogoutView, UserRoleView, UserPermissionsView, 
    AllRolesView, AssignRoleView, CreateUserView, UserProfileView, UpdateProfileView
)

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path("user/", UserProfileView.as_view(), name="user_profile"),
    path("user/update/", UpdateProfileView.as_view(), name="update_profile"),
    path("user/roles/", UserRoleView.as_view(), name="user_roles"),
    path("user/permissions/", UserPermissionsView.as_view(), name="user_permissions"),
    path("user/all-roles/", AllRolesView.as_view(), name="all_roles"),
    path("user/assign-role/", AssignRoleView.as_view(), name="assign_role"),
    path("user/create/", CreateUserView.as_view(), name="create_user"),
]

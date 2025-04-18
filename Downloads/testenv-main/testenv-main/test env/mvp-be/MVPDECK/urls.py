"""
URL configuration for MVPDECK project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from users.views import test_db_connection


from users.views import RegisterView, LoginView, LogoutView, UserViewSet


urlpatterns = [
    path("admin/", admin.site.urls),
    path('test-db/', test_db_connection),
    path('api/', include('users.urls')),
    path("api/claims/", include("claims.urls")),
    path("api/leaves/", include("leaves.urls")),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),# New Logout Endpoint
    path("users/", UserViewSet.as_view({"get": "list", "post": "create"}), name="user-list"),  
]


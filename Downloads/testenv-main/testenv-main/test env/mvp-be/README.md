# **Authentication Module Integration Guide**  

This guide explains how to integrate the authentication module into an existing Django project.

---

## **Step 1: Copy the Authentication Module**  
Copy the `authentication` folder into the root directory of your Django project (next to `manage.py`).

---

## **Step 2: Install Required Dependencies**  
Run the following command to install the required packages:

```bash
pip install djangorestframework djangorestframework-simplejwt
```

---

## **Step 3: Update `settings.py`**  

### 1. Add `authentication` and `rest_framework` to `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    ...
    'rest_framework',
    'authentication',
]
```

### 2. Configure **JWT Authentication** in `settings.py`:

```python
from datetime import timedelta

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": "your_secret_key_here",
}
```

---

## **Step 4: Include Authentication URLs**  
Modify your `urls.py` file to include the authentication module:

```python
from django.urls import path, include

urlpatterns = [
    ...
    path('auth/', include('authentication.urls')),
]
```

---

## **Step 5: Run Migrations**  
Apply the migrations:

```bash
python manage.py makemigrations authentication
python manage.py migrate
```

---

## **Step 6: Create a Superuser (Optional)**  
To create an admin user for testing, run:

```bash
python manage.py createsuperuser
```

---

## **Step 7: Test Authentication in Postman**  

### **Register a New User**
**POST** `http://127.0.0.1:8000/auth/register/`  
**Body (JSON):**  
```json
{
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123"
}
```

---

### **Login and Get Token**
**POST** `http://127.0.0.1:8000/auth/login/`  
**Body (JSON):**  
```json
{
    "email": "test@example.com",
    "password": "password123"
}
```

_Response Example:_
```json
{
    "access": "your_access_token",
    "refresh": "your_refresh_token"
}
```

---

### **Access a Protected Endpoint**
Include the token in the headers:  
```http
Authorization: Bearer your_access_token
```

---

### **Logout (Blacklist Token)**
**POST** `http://127.0.0.1:8000/auth/logout/`  
**Body (JSON):**  
```json
{
    "refresh_token": "your_refresh_token"
}
```

---

## **You're All Set! 🚀**  

The authentication module is now successfully integrated into your Django project. 🎉

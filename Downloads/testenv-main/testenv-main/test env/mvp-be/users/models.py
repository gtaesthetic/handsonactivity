from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, annual_leave_balance=0, sick_leave_balance=0, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('hr', 'HR'),
        ('ceo', 'CEO'),
        ('director', 'Director'),
        ('owner', 'Owner'),
        ('manager', 'Manager'),
        ('team_lead', 'Team Lead'),
        ('supervisor', 'Supervisor'),
        ('employee', 'Regular Employee'),
        ('admin', 'Administrator'),  # New role
    )
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    # New fields for leave balances
    annual_leave_balance = models.IntegerField(default=0)
    sick_leave_balance = models.IntegerField(default=0)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'role']

    def __str__(self):
        return self.email

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=100)
    position = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.department}"

class Manager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    managed_department = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.managed_department}"

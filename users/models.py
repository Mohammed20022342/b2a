from django.contrib.auth.models import AbstractUser
from django.db import models
from orders.models import Order
from django.shortcuts import render, redirect


from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)

class UserProfile(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'  # ✅ Use email as the primary identifier
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

class Address(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="addresses")
    address_line = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    is_default = models.BooleanField(default=False)


def profile_view(request):
    if request.user.is_authenticated:
        orders = Order.objects.filter(user=request.user)  # Fetch orders for logged-in user
        return render(request, 'users/profile.html', {'orders': orders, 'user': request.user})
    else:
        return redirect('users:login_view')
    

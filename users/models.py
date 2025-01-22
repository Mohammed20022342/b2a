from django.contrib.auth.models import AbstractUser
from django.db import models
from orders.models import Order
from django.shortcuts import render, redirect


class UserProfile(AbstractUser):
    phone_number = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    phone_verified = models.BooleanField(default=False)

    # Specify related_name to avoid clashes
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='userprofile_set',  # Changed from 'user_set' to 'userprofile_set'
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='userprofile_set',  # Changed from 'user_set' to 'userprofile_set'
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def __str__(self):
        return self.username

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
    

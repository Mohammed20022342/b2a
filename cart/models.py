from django.db import models
from products.models import Product
from users.models import UserProfile


class Cart(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True, related_name="carts")
    session_id = models.CharField(max_length=255, unique=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)  # Default value for quantity

    def get_total_price(self):
        return self.product.price * self.quantity

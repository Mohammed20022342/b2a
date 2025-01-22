from django.db import models
from users.models import UserProfile  # Ensure this import is correct
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=200, db_index=True)  # For search
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, db_index=True)  # For price range filtering
    stock_quantity = models.PositiveIntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products", db_index=True)
    offer = models.BooleanField(default=False, db_index=True)  # For quick filtering
    detail_image_1 = models.ImageField(upload_to='product_images/', blank=True, null=True)
    detail_image_2 = models.ImageField(upload_to='product_images/', blank=True, null=True)
    detail_image_3 = models.ImageField(upload_to='product_images/', blank=True, null=True)
    brand = models.CharField(max_length=100, blank=True, null=True)
    color = models.CharField(max_length=50, blank=True, null=True)
    size = models.CharField(max_length=50, choices=[('small', 'Small'), ('medium', 'Medium'), ('large', 'Large')], blank=True, null=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # Rating from 1 to 5
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.user.username} - {self.product.title} ({self.rating})"


class RelatedProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="related_products")
    related_product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="+")  # Self-referential




class ContactMessage(models.Model):
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject} ({self.created_at.strftime('%Y-%m-%d %H:%M')})"
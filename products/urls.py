# products/urls.py

from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import contact_us


urlpatterns = [
    path('', views.product_list, name='product_list'),  # List of all products
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('category/<int:category_id>/', views.product_by_category, name='product_by_category'),
    path('review/<int:product_id>/', views.add_review, name='add_review'),  # Add a review
    path('contact/', contact_us, name='contact'),
    path('arabic/', views.arabic_product_list, name='arabic_product_list'),
    path('arabic/product/<int:product_id>/', views.arabic_product_detail, name='arabic_product_detail'),
    path('arabic/category/<int:category_id>/', views.arabic_product_by_category, name='arabic_product_by_category'),



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

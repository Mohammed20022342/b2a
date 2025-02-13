# cart/urls.py
from django.urls import path
from .views import add_to_cart, cart_view, update_cart_item, remove_from_cart, create_checkout_session
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart_view'),
    path('update_cart/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('create-checkout-session/', create_checkout_session, name='create_checkout_session'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path('payment-cancel/', views.payment_cancel, name='payment_cancel'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

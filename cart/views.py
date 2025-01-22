# cart/views.py
from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product
from .models import Cart, CartItem
from django.db.models import Sum


def get_or_create_cart(request):
    session_id = request.session.session_key
    if not session_id:
        request.session.create()  # Create a session if it doesn't exist
        session_id = request.session.session_key

    cart, created = Cart.objects.get_or_create(session_id=session_id)
    return cart

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = get_or_create_cart(request)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if created:  # If it's a new CartItem, set the quantity to 1
        cart_item.quantity = 1
    else:  # If it already exists, increment the quantity
        cart_item.quantity += 1
    cart_item.save()

    return redirect('cart_view')  # Redirect to the cart view


def cart_view(request):
    cart = get_or_create_cart(request)  # Get the cart associated with the session
    cart_items = CartItem.objects.filter(cart=cart)  # Filter items by this cart
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    total_quantity = sum(item.quantity for item in cart_items)  # Sum up the quantities

    context = {
        'items': cart_items,
        'total_price': total_price,
        'total_quantity': total_quantity,  # Pass the total quantity
    }
    return render(request, 'cart/cart.html', context)


def update_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'increase':
            cart_item.quantity += 1
        elif action == 'decrease' and cart_item.quantity > 1:
            cart_item.quantity -= 1

        cart_item.save()

    return redirect('cart_view')


def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()
    return redirect('cart_view')

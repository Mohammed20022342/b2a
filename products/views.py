# products/views.py

from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category, Review
from .forms import ReviewForm  # Assuming you have a ReviewForm for handling reviews
from django.http import HttpResponse
from .forms import ContactForm
from .models import ContactMessage  # Import your model to save messages
from django.db.models import Q  # Import Q for complex queries



def product_list(request):
    query = request.GET.get('q', '')  # Get search query from the URL
    category_id = request.GET.get('category_id', None)  # Optional category filter

    # Start with all products
    products = Product.objects.all()
    products_on_offer = Product.objects.filter(offer=True)

    # Filter by category if category_id is provided
    if category_id:
        products = products.filter(category_id=category_id)
        products_on_offer = products_on_offer.filter(category_id=category_id)

    # Filter by search query if provided (title and description)
    if query:
        # Split the query into individual words
        query_words = query.split()

        # Create a Q object for each word to match in both title and description
        query_filter = Q()
        for word in query_words:
            query_filter &= (Q(title__icontains=word) | Q(description__icontains=word))

        # Apply the filter to the product list
        products = products.filter(query_filter)
        products_on_offer = products_on_offer.filter(query_filter)

    # Get all categories for the filter sidebar
    categories = Category.objects.all()

    context = {
        'products': products,
        'products_on_offer': products_on_offer,
        'categories': categories,
        'query': query,
        'current_category': Category.objects.get(id=category_id) if category_id else None,
    }

    return render(request, 'products/product_list.html', context)


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = product.reviews.all()  # Fetch related reviews
    review_form = ReviewForm()

    if request.method == "POST" and request.user.is_authenticated:
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            return redirect('product_detail', product_id=product.id)

    context = {
        'product': product,
        'reviews': reviews,
        'review_form': review_form,
    }
    return render(request, 'products/product_detail.html', context)


def product_by_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category)
    
    # Apply filters based on GET parameters
    if request.GET.get('price'):
        products = products.filter(price__lte=request.GET['price'])
    if request.GET.get('brand'):
        products = products.filter(brand=request.GET['brand'])
    if request.GET.get('size'):
        products = products.filter(size=request.GET['size'])
    if request.GET.get('color'):
        products = products.filter(color=request.GET['color'])
    
    return render(request, 'products/categories.html', {'category': category, 'products': products})


def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)  # Get the product
    if request.method == 'POST':
        form = ReviewForm(request.POST)  # Assuming you have a ReviewForm
        if form.is_valid():
            review = form.save(commit=False)  # Create review without saving
            review.product = product  # Set the product
            review.user = request.user  # Set the logged-in user as the reviewer
            review.save()  # Save the review
            return redirect('product_detail', pk=product.id)  # Redirect to the product detail page
    else:
        form = ReviewForm()  # Create a new form instance

    return render(request, 'products/add_review.html', {'form': form, 'product': product})


def contact_us(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Retrieve data from the form
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            
            # Save to the database
            ContactMessage.objects.create(subject=subject, message=message)
            
            # Redirect to a 'thank you' page or the same page with a success message
            return redirect('product_list')  # Replace with a valid URL name
        else:
            # Optionally log or handle invalid forms
            print("Invalid form submission")
    else:
        form = ContactForm()
    
    return render(request, 'products/contact-us.html', {'form': form})


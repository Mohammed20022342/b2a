from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from .forms import RegistrationForm, LoginForm
import random
from django.contrib import messages


def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email_verified = False  # ✅ Track email verification
            user.set_password(form.cleaned_data['password'])  # Hash password
            user.save()
            request.session['email'] = user.email  # ✅ Store email for OTP
            return redirect('send_otp')  # Redirect to OTP verification

    else:
        form = RegistrationForm()

    return render(request, 'users/register.html', {'form': form, 'page': 'register'})


from django.core.mail import send_mail
import random

def send_otp(request):
    email = request.session.get('email')  # Retrieve email from session
    if not email:
        return redirect('register_view')  # Redirect if no email found

    otp = random.randint(1000, 9999)  # Generate a 4-digit OTP
    request.session['otp'] = otp  # Store OTP in session

    # ✅ Send OTP via Email
    send_mail(
        subject="Your OTP Code",
        message=f"Your OTP code is: {otp}",
        from_email="b2a.org@gmail.com",  # Replace with your Gmail
        recipient_list=[email],  # Send to the user's email
        fail_silently=False,
    )

    return render(request, 'users/otp.html')  # Show OTP input page

def verify_otp(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')  # Get OTP from form
        actual_otp = request.session.get('otp')  # Get stored OTP

        if str(entered_otp) == str(actual_otp):  # Compare OTPs
            email = request.session.get('email')
            user = UserProfile.objects.get(email=email)
            user.email_verified = True  # ✅ Mark email as verified
            user.save()
            login(request, user)  # Log the user in
            return redirect('profile_view')  # Redirect to profile page

    return render(request, 'users/otp.html', {'error': 'Invalid OTP'})



from django.contrib.auth import get_user_model

User = get_user_model()  # Get the custom User model

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            try:
                user = User.objects.get(email=email)  # Get user by email
            except User.DoesNotExist:
                user = None

            if user is not None and user.check_password(password):  # Check password manually
                login(request, user)
                return redirect('profile_view')

            messages.error(request, 'Invalid email or password')  # Show error message

    form = LoginForm()
    return render(request, 'users/login.html', {'form': form, 'page': 'login'})




from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from orders.models import Order

@login_required
def profile_view(request):
    user_orders = Order.objects.filter(user=request.user)
    context = {
        'user': request.user,
        'orders': user_orders,
    }
    return render(request, 'users/profile.html', context)


@login_required
def update_profile(request):
    user_profile = request.user  # Since user is an instance of UserProfile

    if request.method == 'POST':
        # Get the new address from the form
        address = request.POST.get('address', '').strip()
        
        if address:  # If the address is provided
            user_profile.address = address  # Update the address field
            user_profile.save()  # Save the changes to the user profile
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('users:profile')  # Redirect back to the profile page
        else:
            messages.error(request, 'Address cannot be empty. Please provide a valid address.')

    return render(request, 'users/profile.html', {'user': user_profile})



def logout_view(request):
    logout(request)  # This will log the user out
    return redirect('login_view')  # Redirect to the login page or homepage
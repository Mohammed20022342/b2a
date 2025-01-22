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
            user = form.save(commit=False)  # Create user object but don't save it yet
            user.phone_verified = False  # Set initial phone verification status
            user.set_password(form.cleaned_data['password'])  # Set password correctly
            user.save()  # Save the user to the database

            # Proceed with OTP
            request.session['phone_number'] = user.phone_number  # Save phone number for OTP
            return redirect('send_otp')  # Redirect to send OTP

    else:
        form = RegistrationForm()  # Instantiate a blank form if not POST

    return render(request, 'users/register.html', {'form': form, 'page': 'register'})

def send_otp(request):
    phone_number = request.session.get('phone_number')
    if not phone_number:
        return redirect('register')  # If no phone, redirect to register

    otp = random.randint(1000, 9999)
    request.session['otp'] = otp  # Save OTP in session

    # Here you would send the OTP using an SMS service
    print(f"OTP for {phone_number}: {otp}")  # For testing purposes

    return render(request, 'users/otp.html')

def verify_otp(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        actual_otp = request.session.get('otp')

        if str(entered_otp) == str(actual_otp):
            phone_number = request.session.get('phone_number')
            user = UserProfile.objects.get(phone_number=phone_number)
            user.phone_verified = True
            user.save()
            login(request, user)
            return redirect('../..')

    return render(request, 'users/otp.html', {'error': 'Invalid OTP'})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request, 
                username=form.cleaned_data['username_or_phone'], 
                password=form.cleaned_data['password']
            )
            if user:
                login(request, user)

                # Check if the user is an admin and redirect to the admin interface
                if user.is_staff:
                    return redirect('/admin/')  # Redirect to the admin interface
                return redirect('../..')  # Or any other page you want non-admin users to go to

            messages.error(request, 'Invalid credentials')
            return render(request, 'users/login.html', {'error': 'Invalid credentials', 'page': 'login'})

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
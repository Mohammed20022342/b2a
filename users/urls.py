from django.urls import path
from . import views
from .views import login_view, register_view
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views  # This imports the built-in views


urlpatterns = [
    path('register/', register_view, name='register_view'),
    path('login/', login_view, name='login_view'),
    path('send-otp/', views.send_otp, name='send_otp'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('profile/', views.profile_view, name='profile_view'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('logout/', views.logout_view, name='logout_view'),

    path('password/change/', auth_views.PasswordChangeView.as_view(), name='change_password'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

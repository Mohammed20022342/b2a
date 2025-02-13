from django import forms
from .models import UserProfile

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'password']  # ✅ Use email instead of phone number


class LoginForm(forms.Form):
    email = forms.EmailField()  # ✅ Use email instead of username
    password = forms.CharField(widget=forms.PasswordInput)
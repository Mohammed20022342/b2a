from django import forms
from .models import UserProfile

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'password']

class LoginForm(forms.Form):
    username_or_phone = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

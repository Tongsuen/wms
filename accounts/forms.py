from django import forms
from .models import User
from django.contrib.auth import get_user_model

class LoginForm(forms.Form):
    email = forms.CharField(
        )
    password = forms.CharField(
        max_length=32
        )
class RegisterForm(forms.Form):
    email = forms.EmailField(

        )
    password = forms.CharField(
        max_length=32
        )
    password2 = forms.CharField(
        max_length=32
        )

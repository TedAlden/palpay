from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser

CURRENCY_OPTIONS = [
    ("GBP", "GBP"),
    ("USD", "USD"),
    ("EUR", "EUR"),
]


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(max_length=50, required=True)
    currency = forms.ChoiceField(choices=CURRENCY_OPTIONS, required=True)

    class Meta:
        model = CustomUser
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "currency",
            "password1",
            "password2",
        )

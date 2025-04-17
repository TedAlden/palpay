from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser

CURRENCY_OPTIONS = [
    ("GBP", "GBP"),
    ("USD", "USD"),
    ("EUR", "EUR"),
]


class RegisterForm(UserCreationForm):
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

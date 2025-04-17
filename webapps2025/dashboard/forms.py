from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

CustomUser = get_user_model()

CURRENCY_OPTIONS = [
    ("GBP", "GBP"),
    ("USD", "USD"),
    ("EUR", "EUR"),
]


class RegisterAdminForm(UserCreationForm):
    """A form for creating new users with admin privileges."""
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

    def save(self, commit=True):
        user = super().save(commit=False)
        # Set superuser to True before committing to the database
        user.is_superuser = True
        if commit:
            user.save()
        return user

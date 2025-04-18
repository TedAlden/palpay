from django.db import models
from django.contrib.auth.models import AbstractUser

from payment.helpers import convert_currency

STARTING_BALANCE = 750.00
CURRENCY_OPTIONS = [
    ("EUR", "Euros"),
    ("GBP", "Pounds"),
    ("USD", "US Dollars"),
]


class CustomUser(AbstractUser):
    currency = models.CharField(
        max_length=3,
        choices=CURRENCY_OPTIONS,
        default=CURRENCY_OPTIONS[0][0],
    )
    balance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=STARTING_BALANCE,
    )

    def save(self, *args, **kwargs):
        # Set default balance only when creating a new user, i.e. if the
        # user has no primary key (ID) yet.
        if not self.pk:
            # Convert the starting balance to the user's currency.
            self.balance = convert_currency("GBP", self.currency, STARTING_BALANCE)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.email} ({self.currency})"

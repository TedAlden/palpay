from django.db import models
from django.contrib.auth.models import AbstractUser

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

    def __str__(self):
        return f"{self.email} ({self.currency})"

from django.db import models
from django.conf import settings

TRANSACTION_TYPES = [
    ("Send", "Send"),
    ("Receive", "Receive"),
]
TRANSACTION_STATUS_TYPES = [
    ("Pending", "Pending"),
    ("Completed", "Completed"),
    ("Rejected", "Rejected"),
]
CURRENCY_TYPES = [
    ("EUR", "Euros"),
    ("GBP", "Pounds"),
    ("USD", "US Dollars"),
]


class Transaction(models.Model):
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sent_transactions",
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="received_transactions",
    )
    type = models.CharField(
        max_length=7,
        choices=TRANSACTION_TYPES,
        default="Send",
    )
    amount_sent = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    currency_sent = models.CharField(
        max_length=3,
        choices=CURRENCY_TYPES,
    )
    amount_received = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    currency_received = models.CharField(
        max_length=3,
        choices=CURRENCY_TYPES,
    )
    timestamp = models.DateTimeField(
        auto_now_add=True
    )
    status = models.CharField(
        max_length=9,
        choices=TRANSACTION_STATUS_TYPES,
        default="Pending",
    )

    def __str__(self):
        return (
            f"{self.sender.username} ({self.currency_sent} {self.amount_sent}) -> {self.receiver.username} ({self.currency_received} {self.amount_received})"
        )

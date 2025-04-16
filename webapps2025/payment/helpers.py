from django.db import transaction
from django.conf import settings

from decimal import Decimal

import urllib.parse
import requests


def convert_currency(from_currency, to_currency, amount):
    try:
        url = urllib.parse.urljoin(
            settings.API_BASE_URL,
            f"api/conversion/{from_currency}/{to_currency}/{amount}/",
        )

        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            return data["converted_amount"]
        else:
            raise ValueError(f"Error fetching conversion rate: {response.status_code}")

    except Exception as e:
        print(f"Currency conversion API error: {e}")
        return Decimal("1.0")


@transaction.atomic
def transfer_money(sender, receiver, amount_sent, amount_received):
    sender.balance -= amount_sent
    receiver.balance += amount_received
    sender.save()
    receiver.save()

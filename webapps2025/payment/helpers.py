from django.db import transaction


def get_conversion_rate(from_currency, to_currency):
    if from_currency == "EUR" and to_currency == "USD":
        return 1.1
    elif from_currency == "EUR" and to_currency == "GBP":
        return 0.85
    
    elif from_currency == "USD" and to_currency == "EUR":
        return 0.9
    elif from_currency == "USD" and to_currency == "GBP":
        return 0.75
    
    elif from_currency == "GBP" and to_currency == "EUR":
        return 1.18
    elif from_currency == "GBP" and to_currency == "USD":
        return 1.33

    return 1.0


@transaction.atomic
def transfer_money(sender, receiver, amount_sent, amount_received):
    sender.balance -= amount_sent
    receiver.balance += amount_received
    sender.save()
    receiver.save()


# @transaction.atomic
# def complete_transaction(transaction):
#     transaction.status = "Completed"
#     transaction.save()

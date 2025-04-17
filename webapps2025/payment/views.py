from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages

from decimal import Decimal

from .models import Transaction
from .forms import SendMoneyForm, RequestMoneyForm
from .helpers import convert_currency, transfer_money


def home(request):
    return render(request, "payment/home.html")


@login_required(login_url='login')
def send_money(request):
    if request.method == "POST":
        send_form = SendMoneyForm(request.POST)
        if send_form.is_valid():
            sender = request.user
            recipient_username = send_form.cleaned_data["recipient"]
            amount_sent = send_form.cleaned_data["amount"]

            # Find the recipient user
            User = get_user_model()
            try:
                recipient = User.objects.get(username=recipient_username)
            except User.DoesNotExist:
                send_form.add_error("recipient", "User does not exist.")
                return render(request, "payment/send.html", {"send_form": send_form})

            # Prevent sending money to yourself
            if sender == recipient:
                send_form.add_error("recipient", "Cannot send money to yourself.")
                return render(request, "payment/send.html", {"send_form": send_form})
            
            # Check if the sender has sufficient balance
            if sender.balance < amount_sent:
                send_form.add_error("amount", "Insufficient balance.")
                return render(request, "payment/send.html", {"send_form": send_form})

            # Handle currency conversion, using the convert_currency
            # helper function which makes the API call
            currency_sent = sender.currency
            currency_received = recipient.currency
            amount_received = Decimal(convert_currency(
                currency_sent, currency_received, amount_sent
            )).quantize(Decimal("0.01"))
            
            # Get timestamp
            timestamp = request.POST.get("timestamp")

            # Create the transaction record
            transaction = Transaction.objects.create(
                type="Send",
                sender=sender,
                receiver=recipient,
                amount_sent=amount_sent,
                currency_sent=currency_sent,
                amount_received=amount_received,
                currency_received=currency_received,
                timestamp=timestamp,
                status="Pending",
            )

            messages.success(
                request,
                f"Requested to send {currency_sent} {amount_sent} to {recipient.username} ({currency_received} {amount_received}).",
            )

            return redirect("send_money")

    send_form = SendMoneyForm()
    return render(request, "payment/send.html", {"send_form": send_form})


@login_required(login_url='login')
def request_money(request):
    if request.method == "POST":
        request_form = RequestMoneyForm(request.POST)
        if request_form.is_valid():
            recipient = request.user
            sender_username = request_form.cleaned_data["target_user"]
            amount_requested = request_form.cleaned_data["amount"]

            # Find the user to request money from
            User = get_user_model()
            try:
                sender = User.objects.get(username=sender_username)
            except User.DoesNotExist:
                request_form.add_error("target_user", "User does not exist.")
                return render(request, "payment/request.html", {"request_form": request_form})
            
            # Prevent requesting money from superusers (admins)
            if sender.is_superuser:
                request_form.add_error("target_user", "Cannot send money to superuser.")
                return render(request, "payment/request.html", {"request_form": request_form})

            # Prevent requesting money from yourself
            if recipient == sender:
                request_form.add_error("target_user", "Cannot send money to yourself.")
                return render(request, "payment/request.html", {"request_form": request_form})

            # Handle currency conversion, using the convert_currency
            # helper function which makes the API call
            currency_sent = sender.currency
            currency_received = recipient.currency
            amount_sent = Decimal(convert_currency(
                currency_received, currency_sent, amount_requested
            )).quantize(Decimal("0.01"))
            
            # Get timestamp
            timestamp = request.POST.get("timestamp")

            # Create the transaction record
            transaction = Transaction.objects.create(
                type="Receive",
                sender=sender,
                receiver=recipient,
                amount_sent=amount_sent,
                currency_sent=currency_sent,
                amount_received=amount_requested,
                currency_received=currency_received,
                timestamp=timestamp,
                status="Pending",
            )

            messages.success(
                request,
                f"Requested {currency_received} {amount_requested} ({currency_sent} {amount_sent}) from {recipient.username}.",
            )

            return redirect("request_money")

    request_form = RequestMoneyForm()
    return render(request, "payment/request.html", {"request_form": request_form})


@login_required(login_url='login')
def transaction_history(request):
    user = request.user

    # Get all transactions for the user. I.e. any transaction sent to or
    # received from the user.
    transactions = Transaction.objects.filter(
        sender=user
    ).union(Transaction.objects.filter(
        receiver=user
    )).order_by("-timestamp")

    return render(
        request,
        "payment/transactions.html",
        {
            "user": user,
            "transactions": transactions,
        },
    )


@login_required(login_url='login')
def notifications(request):
    user = request.user

    # Get all notifications for the user. I.e. any transaction sent to
    # or requested from the user that is still pending.
    notifications = Transaction.objects.filter(
        receiver=user,
        type="Send",
        status="Pending",
    ).union(Transaction.objects.filter(
        sender=user,
        type="Receive",
        status="Pending",
    )).order_by("-timestamp")

    return render(
        request,
        "payment/notifications.html",
        {
            "notifications": notifications
        },
    )


@csrf_protect
@login_required(login_url='login')
def accept_transaction(request, transaction_id):
    if request.method == "POST":
        # Update the transaction status to "Completed"
        transaction = get_object_or_404(
            Transaction,
            id=transaction_id,
            status="Pending"
        )
        transaction.status = "Completed"
        transaction.save()

        # Perform the money transfer
        transfer_money(
            transaction.sender,
            transaction.receiver,
            transaction.amount_sent,
            transaction.amount_received
        )

        messages.success(request, "Transaction accepted successfully.")

    return redirect('notifications')


@csrf_protect
@login_required(login_url='login')
def reject_transaction(request, transaction_id):
    if request.method == "POST":
        # Update the transaction record to "Rejected"
        transaction = get_object_or_404(
            Transaction,
            id=transaction_id,
            status="Pending"
        )
        transaction.status = "Rejected"
        transaction.save()

        # No need to perform any money transfer since the transaction is
        # rejected.

        messages.success(request, "Transaction rejected successfully.")

    return redirect('notifications')

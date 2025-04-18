from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.csrf import csrf_protect

from payment.models import Transaction
from .forms import RegisterAdminForm
from .helpers import user_is_admin


@csrf_protect
@user_passes_test(user_is_admin, login_url="login")
def register_admin(request):
    if request.method == "POST":
        form = RegisterAdminForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Admin registration successful.")
            return redirect("all_users")
        else:
            messages.error(
                request,
                "Unsuccessful registration. Invalid information."
            )

    form = RegisterAdminForm()
    return render(
        request,
        "dashboard/register_admin.html",
        {
            "register_admin": form,
        }
    )


@user_passes_test(user_is_admin, login_url="login")
def all_transactions(request):
    # Get all transactions for every user
    transactions = Transaction.objects.all().order_by("-timestamp")

    return render(
        request,
        "dashboard/all_transactions.html",
        {
            "transactions": transactions,
        }
    )


@user_passes_test(user_is_admin, login_url="login")
def all_users(request):
    # Get all users in the system, ordered by date joined
    User = get_user_model()
    users = User.objects.all().order_by("-date_joined")

    return render(
        request,
        "dashboard/users.html",
        {
            "users": users,
        }
    )

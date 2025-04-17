from django.urls import path
from . import views

urlpatterns = [
    path("register_admin", views.register_admin, name="register_admin"),
    path("transactions", views.all_transactions, name="all_transactions"),
    path("users", views.all_users, name="all_users"),
]

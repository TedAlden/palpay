from django.urls import path

from . import views

urlpatterns = [
    path(
        "conversion/<str:from_currency>/<str:to_currency>/<str:amount>/",
        views.currency_conversion,
        name="currency_conversion",
    ),
]

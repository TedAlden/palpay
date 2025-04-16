from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_GET


CURRENCY_CONVERSION_RATES = {
    ("EUR", "USD"): 1.1,
    ("EUR", "GBP"): 0.85,
    ("USD", "EUR"): 0.9,
    ("USD", "GBP"): 0.75,
    ("GBP", "EUR"): 1.18,
    ("GBP", "USD"): 1.33,
}

SUPPORTED_CURRENCIES = {
    cur for pair in CURRENCY_CONVERSION_RATES.keys() for cur in pair
}


@require_GET
def currency_conversion(request, from_currency, to_currency, amount):
    try:
        # Case-normalise the currency codes to uppercase
        from_currency = from_currency.upper()
        to_currency = to_currency.upper()

        # Validate the from_currency type
        if from_currency not in SUPPORTED_CURRENCIES:
            return JsonResponse(
                {"error": f"Unrecognised from_currency: {from_currency}"}, status=422
            )

        # Validate the to_currency type
        if to_currency not in SUPPORTED_CURRENCIES:
            return JsonResponse(
                {"error": f"Unrecognised to_currency: {to_currency}"}, status=422
            )

        # Validate the amount data type
        try:
            float(amount)
        except ValueError:
            return JsonResponse(
                {"error": f"Amount must be a number: {amount}"}, status=400
            )

        # Check that the amount is positive
        if float(amount) <= 0:
            return JsonResponse(
                {"error": f"Amount must be greater than zero: {amount}"}, status=422
            )

        # Calculate the converted amount, rounded to 2 decimal places
        rate = CURRENCY_CONVERSION_RATES.get((from_currency, to_currency))
        converted_amount = round(float(amount) * rate, 2)

        return JsonResponse(
            {
                "from_currency": from_currency,
                "to_currency": to_currency,
                "amount": float(amount),
                "converted_amount": converted_amount,
                "rate": rate,
            }
        )

    # Catch generic server error, if the above handling doesn't
    except Exception as e:
        return JsonResponse({"error": f"Server error: {e}"}, status=500)

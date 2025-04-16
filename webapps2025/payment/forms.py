from django import forms


class SendMoneyForm(forms.Form):
    recipient = forms.CharField(
        max_length=50,
        label="Recipient Username",
    )
    amount = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        label="Amount",
    )


class RequestMoneyForm(forms.Form):
    target_user = forms.CharField(
        max_length=50,
        label="Requested Username",
    )
    amount = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        label="Amount",
    )

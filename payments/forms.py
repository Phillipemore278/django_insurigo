from django import forms
from .models import Payment

from django import forms

from django import forms
from .models import Payment

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['payment_method', 'transaction_id']
        widgets = {
            'payment_method': forms.Select(choices=[
                ('bank_transfer', 'Bank Transfer'),
                ('credit_card', 'Credit Card'),
                ('ussd', 'USSD'),
                ('wallet', 'Wallet'),
            ]),
            'transaction_id': forms.TextInput(attrs={'placeholder': 'Payment Reference ID'}),
        }


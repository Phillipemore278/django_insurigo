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

    def __init__(self, *args, **kwargs):
        super(PaymentForm, self).__init__(*args, **kwargs)

        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({
                'class': 'form-control',
            })


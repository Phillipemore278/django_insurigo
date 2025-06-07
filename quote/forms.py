from django import forms

class QuoteForm(forms.Form):
    INSURANCE_CHOICES = [
        ('health', 'Health Insurance'),
        ('car', 'Car Insurance'),
    ]
    insurance_type = forms.ChoiceField(choices=INSURANCE_CHOICES, label="Select Insurance Type")

    # Health-specific fields
    health_plan_type = forms.ChoiceField(
        choices=[('hmo', 'HMO'), ('ppo', 'PPO'), ('epo', 'EPO')],
        required=False,
        label="Health Plan Type"
    )
    health_dependents = forms.IntegerField(min_value=0, max_value=10, required=False, initial=0)
    health_add_ons = forms.BooleanField(required=False, label="Include Add-Ons?")

    # Car-specific fields
    car_make = forms.CharField(max_length=50, required=False)
    car_model = forms.CharField(max_length=50, required=False)
    car_year = forms.IntegerField(min_value=1980, max_value=2100, required=False)
    car_driver_age = forms.IntegerField(min_value=16, max_value=100, required=False)

    def __init__(self, *args, **kwargs):
        super(QuoteForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if not isinstance(field, forms.BooleanField):
                field.widget.attrs.update({'class': 'form-control'})

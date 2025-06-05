from django import forms
from .models import Vehicle, CarPolicy


class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['make', 'model', 'year', 'vin', 'value', 'garage_address']
    def __init__(self, *args, **kwargs):
        super(VehicleForm, self).__init__(*args, **kwargs)

        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({
                'class': 'form-control',
            })

class CarPolicyForm(forms.ModelForm):
    class Meta:
        model = CarPolicy
        fields = ['coverage_type']

    def __init__(self, *args, **kwargs):
        super(CarPolicyForm, self).__init__(*args, **kwargs)

        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({
                'class': 'form-control',
            })

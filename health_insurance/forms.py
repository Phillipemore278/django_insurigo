# health_insurance/forms.py

from django import forms
from .models import HealthPolicy, Dependent, HealthHistory
from django.forms.widgets import DateInput
from django.utils import timezone


class HealthPolicyForm(forms.ModelForm):
    class Meta:
        model = HealthPolicy
        fields = ['plan_type', 'add_ons']


class DependentForm(forms.ModelForm):
    class Meta:
        model = Dependent
        fields = ['name', 'date_of_birth', 'relationship']
        widgets = {
            'date_of_birth': DateInput(attrs={'type': 'date'})
        }

    def clean_date_of_birth(self):
        dob = self.cleaned_data['date_of_birth']
        if dob > timezone.now().date():
            raise forms.ValidationError("Date of birth cannot be in the future.")
        return dob
    

class HealthHistoryForm(forms.ModelForm):
    class Meta:
        model = HealthHistory
        fields = ['conditions', 'medications', 'allergies']
        widgets = {
            'conditions': forms.Textarea(attrs={'rows': 2}),
            'medications': forms.Textarea(attrs={'rows': 2}),
            'allergies': forms.Textarea(attrs={'rows': 2}),
        }

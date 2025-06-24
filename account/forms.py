from django import forms
from django.contrib.auth.forms import AuthenticationForm
from captcha.fields import CaptchaField
from django.forms.widgets import DateInput

from .models import Customer, Profile

class CustomAuthenticationForm(AuthenticationForm):
    remember_me = forms.BooleanField(required=False, initial=False, label="Remember Me")
    def __init__(self, *args, **kwargs):
        super(CustomAuthenticationForm, self).__init__(*args, **kwargs)

        # Add Bootstrap class to each form field
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({
                'class': 'form-control',
                'placeholder': self.fields[field_name].label
            })
        # Only try to add class to 'remember_me' if it's defined
        if 'remember_me' in self.fields:
            self.fields['remember_me'].widget.attrs.update({'class': 'form-check-input'})


class CustomerRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Customer
        fields = ['email', 'full_name']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
        }
        
    captcha = CaptchaField()  # No need for API keys

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
        return password2

    def save(self, commit=True):
        customer = super().save(commit=False)
        customer.set_password(self.cleaned_data["password1"])
        if commit:
            customer.save()
        return customer


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['date_of_birth', 'address', 'phone', 'state', 'zip_code', 'country', "socials"]
        widgets = {
            'date_of_birth': DateInput(attrs={'type': 'date'})
        }
    
    def __init__(self, *args, **kwargs):
        # Pass a flag to disable fields if needed
        disable_fields = kwargs.pop('disable_fields', False)
        super().__init__(*args, **kwargs)

        # Change label of 'socials' to 'SSN'
        self.fields['socials'].label = 'SSN'

        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({
                'class': 'form-control',
            })
            if disable_fields:
                self.fields[field_name].disabled = True  # make field readonly

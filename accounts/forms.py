from django import forms
from .models import Address

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['full_name', 'phone', 'line1', 'line2', 'city', 'state', 'pincode', 'country', 'is_default']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'line1': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address Line 1'}),
            'line2': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address Line 2'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State'}),
            'pincode': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pincode'}),
            'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'}),
            'is_default': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
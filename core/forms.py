
from django import forms
from .models import Farmer, Produce, BuyerOrder


class FarmerForm(forms.ModelForm):
    class Meta:
        model = Farmer
        fields = [
            'name',
            'phone',
            'village'
        ]


class ProduceForm(forms.ModelForm):
    class Meta:
        model = Produce
        fields = [
            'farmer',
            'crop_name',
            'quantity_kg',
            'price_per_kg',
            'harvest_date'
        ]

        widgets = {
            'harvest_date': forms.DateInput(
                attrs={'type': 'date'}
            )
        }


class BuyerOrderForm(forms.ModelForm):
    class Meta:
        model = BuyerOrder
        fields = [
            'buyer_name',
            'crop_name',
            'required_quantity_kg',
            'target_price_per_kg',
            'delivery_location'
        ]

from django import forms
from .models import Product, Cart, Item


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'product_name',
            'price_ex_tax',
            'vat',
            'ordered_stock',
            'maximum_stock_available'
        ]

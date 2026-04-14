from django import forms
from .models import Product, RFQ, Order


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'category', 'description', 'price', 'currency', 'country',
                  'market_type', 'stock_quantity', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }


class RFQForm(forms.ModelForm):
    class Meta:
        model = RFQ
        fields = ['title', 'description', 'quantity', 'target_price', 'destination_country']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['quantity', 'payment_method', 'shipping_address', 'notes']
        widgets = {
            'shipping_address': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

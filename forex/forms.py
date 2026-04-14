from django import forms
from .models import ForexTransaction

CURRENCY_CHOICES = [
    ('USD', 'US Dollar'), ('CAD', 'Canadian Dollar'), ('UGX', 'Ugandan Shilling'),
    ('EUR', 'Euro'), ('KES', 'Kenyan Shilling'), ('JPY', 'Japanese Yen'),
    ('GBP', 'British Pound'),
]

class ForexTransactionForm(forms.ModelForm):
    from_currency = forms.ChoiceField(choices=CURRENCY_CHOICES)
    to_currency = forms.ChoiceField(choices=CURRENCY_CHOICES)

    class Meta:
        model = ForexTransaction
        fields = ['transaction_type', 'from_currency', 'to_currency', 'amount_from', 'notes']
        widgets = {'notes': forms.Textarea(attrs={'rows': 3})}

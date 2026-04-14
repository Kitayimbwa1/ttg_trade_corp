from django import forms
from .models import InsurancePolicy

class InsurancePolicyForm(forms.ModelForm):
    class Meta:
        model = InsurancePolicy
        fields = ['coverage_amount', 'premium_amount', 'premium_frequency', 
                 'start_date', 'end_date', 'beneficiary_name', 'beneficiary_relationship',
                 'paid_with_avon_points', 'avon_points_used']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

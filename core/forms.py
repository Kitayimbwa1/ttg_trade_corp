from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import TraderProfile, ContactMessage


class TraderRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=20)
    country_of_residence = forms.ChoiceField(choices=TraderProfile.COUNTRY_CHOICES)
    market_type = forms.ChoiceField(choices=TraderProfile.MARKET_CHOICES)
    trading_duration = forms.ChoiceField(choices=TraderProfile.DURATION_CHOICES)
    business_description = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}))
    declaration = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 5}),
        label="Declaration & Agreement",
        help_text="State your declaration and agreement to trade through T&TG Trade Corp."
    )
    declaration_file = forms.FileField(required=False, label="Upload Signed Declaration (PDF/DOC)")
    national_id_front = forms.ImageField(required=False, label="National ID - Front")
    national_id_back = forms.ImageField(required=False, label="National ID - Back")
    selfie = forms.ImageField(required=False, label="Selfie (for identity verification)")

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            TraderProfile.objects.create(
                user=user,
                phone_number=self.cleaned_data['phone_number'],
                country_of_residence=self.cleaned_data['country_of_residence'],
                market_type=self.cleaned_data['market_type'],
                trading_duration=self.cleaned_data['trading_duration'],
                business_description=self.cleaned_data['business_description'],
                declaration=self.cleaned_data['declaration'],
                declaration_file=self.cleaned_data.get('declaration_file'),
                national_id_front=self.cleaned_data.get('national_id_front'),
                national_id_back=self.cleaned_data.get('national_id_back'),
                selfie=self.cleaned_data.get('selfie'),
            )
        return user


class TraderProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = TraderProfile
        fields = ['profile_photo', 'bio', 'phone_number', 'business_description']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
            'business_description': forms.Textarea(attrs={'rows': 4}),
        }


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 5}),
        }

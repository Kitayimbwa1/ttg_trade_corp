from django.db import models
from django.contrib.auth.models import User
from ecommerce.models import COUNTRY_CHOICES


class InsuranceProduct(models.Model):
    """Insurance products offered"""
    PRODUCT_TYPES = [
        ('life', 'Life Insurance'),
        ('health', 'Health Insurance'),
        ('property', 'Property Insurance'),
        ('business', 'Business Insurance'),
        ('travel', 'Travel Insurance'),
    ]
    
    name = models.CharField(max_length=200)
    product_type = models.CharField(max_length=20, choices=PRODUCT_TYPES)
    description = models.TextField()
    coverage_details = models.TextField()
    min_premium = models.DecimalField(max_digits=10, decimal_places=2)
    max_premium = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=5, default='USD')
    available_countries = models.CharField(max_length=200, help_text="Comma-separated country codes")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} ({self.product_type})"


class InsurancePolicy(models.Model):
    """Insurance policies purchased by users"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
        ('claimed', 'Claimed'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='insurance_policies')
    product = models.ForeignKey(InsuranceProduct, on_delete=models.CASCADE, related_name='policies')
    policy_number = models.CharField(max_length=50, unique=True)
    
    # Coverage details
    coverage_amount = models.DecimalField(max_digits=12, decimal_places=2)
    premium_amount = models.DecimalField(max_digits=10, decimal_places=2)
    premium_frequency = models.CharField(max_length=20, 
                                        choices=[('monthly', 'Monthly'), ('quarterly', 'Quarterly'), 
                                                ('annual', 'Annual')])
    
    # Policy period
    start_date = models.DateField()
    end_date = models.DateField()
    
    # Payment with Avon Points
    paid_with_avon_points = models.BooleanField(default=False)
    avon_points_used = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    beneficiary_name = models.CharField(max_length=200, blank=True)
    beneficiary_relationship = models.CharField(max_length=100, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.policy_number} - {self.user.get_full_name()}"


class InsuranceClaim(models.Model):
    """Insurance claims filed by policyholders"""
    STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('paid', 'Paid'),
    ]
    
    policy = models.ForeignKey(InsurancePolicy, on_delete=models.CASCADE, related_name='claims')
    claim_number = models.CharField(max_length=50, unique=True)
    claim_amount = models.DecimalField(max_digits=12, decimal_places=2)
    claim_date = models.DateField()
    incident_date = models.DateField()
    incident_description = models.TextField()
    supporting_documents = models.FileField(upload_to='insurance_claims/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted')
    admin_notes = models.TextField(blank=True)
    settlement_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    settlement_date = models.DateField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Claim {self.claim_number} - {self.policy.policy_number}"

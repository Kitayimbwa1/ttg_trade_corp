from django.contrib import admin
from .models import InsuranceProduct, InsurancePolicy, InsuranceClaim

@admin.register(InsuranceProduct)
class InsuranceProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'product_type', 'min_premium', 'max_premium', 'is_active']
    list_filter = ['product_type', 'is_active']
    search_fields = ['name', 'description']

@admin.register(InsurancePolicy)
class InsurancePolicyAdmin(admin.ModelAdmin):
    list_display = ['policy_number', 'user', 'product', 'status', 'start_date', 'end_date']
    list_filter = ['status', 'product__product_type']
    search_fields = ['policy_number', 'user__username', 'user__email']
    date_hierarchy = 'start_date'

@admin.register(InsuranceClaim)
class InsuranceClaimAdmin(admin.ModelAdmin):
    list_display = ['claim_number', 'policy', 'claim_amount', 'status', 'claim_date']
    list_filter = ['status']
    search_fields = ['claim_number', 'policy__policy_number']
    date_hierarchy = 'claim_date'

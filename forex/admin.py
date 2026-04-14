from django.contrib import admin
from .models import ExchangeRate, ForexTransaction

@admin.register(ExchangeRate)
class ExchangeRateAdmin(admin.ModelAdmin):
    list_display = ['from_currency', 'to_currency', 'rate', 'updated_at']

@admin.register(ForexTransaction)
class ForexTransactionAdmin(admin.ModelAdmin):
    list_display = ['reference', 'user', 'from_currency', 'to_currency', 'amount_from', 'status', 'created_at']
    list_filter = ['status', 'transaction_type']

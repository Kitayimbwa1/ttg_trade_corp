from django.contrib import admin
from .models import CoffeeProduct, CoffeeOrder, ProductionLevel

@admin.register(CoffeeProduct)
class CoffeeProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'coffee_type', 'roast_level', 'price_per_kg', 'stock_kg', 'is_active']
    list_filter = ['coffee_type', 'roast_level', 'is_organic', 'is_active']
    search_fields = ['name', 'description']

@admin.register(CoffeeOrder)
class CoffeeOrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'customer', 'product', 'quantity_kg', 'total_amount', 'status', 'created_at']
    list_filter = ['status', 'customer_type', 'destination_country']
    search_fields = ['order_number', 'customer__username', 'customer__email']
    readonly_fields = ['order_number', 'total_amount']
    date_hierarchy = 'created_at'

@admin.register(ProductionLevel)
class ProductionLevelAdmin(admin.ModelAdmin):
    list_display = ['name', 'level_number', 'kg_per_week', 'monthly_revenue_min', 
                   'monthly_revenue_max', 'is_current']
    list_editable = ['is_current']

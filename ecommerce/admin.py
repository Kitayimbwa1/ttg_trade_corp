from django.contrib import admin
from .models import (Category, PartnerCompany, Product, RFQ, Order, 
                     AvonPointsAccount, AvonPointsTransaction, AvonPointsSellOrder)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(PartnerCompany)
class PartnerCompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'unique_id', 'country', 'is_active']
    list_filter = ['country', 'is_active']
    search_fields = ['name', 'unique_id', 'contact_person']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'country', 'market_type', 'stock_quantity', 'is_active']
    list_filter = ['market_type', 'country', 'is_active']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}

@admin.register(RFQ)
class RFQAdmin(admin.ModelAdmin):
    list_display = ['title', 'buyer', 'quantity', 'status', 'created_at']
    list_filter = ['status', 'destination_country']
    search_fields = ['title', 'buyer__username']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'buyer', 'product', 'total_amount', 'status', 'delivery_type', 'created_at']
    list_filter = ['status', 'delivery_type', 'destination_country']
    search_fields = ['buyer__username', 'product__title']
    readonly_fields = ['avon_points_earned']

@admin.register(AvonPointsAccount)
class AvonPointsAccountAdmin(admin.ModelAdmin):
    list_display = ['user', 'available_points', 'total_earned_points', 'total_redeemed_points']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['total_earned_points', 'total_redeemed_points']

@admin.register(AvonPointsTransaction)
class AvonPointsTransactionAdmin(admin.ModelAdmin):
    list_display = ['account', 'transaction_type', 'amount', 'source', 'created_at']
    list_filter = ['transaction_type']
    search_fields = ['account__user__username', 'source']
    date_hierarchy = 'created_at'

@admin.register(AvonPointsSellOrder)
class AvonPointsSellOrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'points_amount', 'quarter', 'usd_amount', 'status', 'created_at']
    list_filter = ['quarter', 'status']
    search_fields = ['user__username']
    date_hierarchy = 'created_at'

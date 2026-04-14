#!/bin/bash

cat > coffee/apps.py << 'EOF'
from django.apps import AppConfig

class CoffeeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'coffee'
EOF

cat > coffee/models.py << 'EOF'
from django.db import models
from django.contrib.auth.models import User
from ecommerce.models import COUNTRY_CHOICES


class CoffeeProduct(models.Model):
    """Roasted coffee products"""
    COFFEE_TYPES = [
        ('arabica', 'Arabica'),
        ('robusta', 'Robusta'),
        ('blend', 'Blend'),
    ]
    ROAST_LEVELS = [
        ('light', 'Light Roast'),
        ('medium', 'Medium Roast'),
        ('dark', 'Dark Roast'),
    ]
    
    name = models.CharField(max_length=200)
    coffee_type = models.CharField(max_length=20, choices=COFFEE_TYPES)
    roast_level = models.CharField(max_length=20, choices=ROAST_LEVELS)
    description = models.TextField()
    
    # Pricing per kg
    price_per_kg = models.DecimalField(max_digits=8, decimal_places=2, 
                                      help_text="Price in USD per kilogram")
    min_price = models.DecimalField(max_digits=8, decimal_places=2, default=35,
                                    help_text="Minimum price per kg")
    max_price = models.DecimalField(max_digits=8, decimal_places=2, default=55,
                                    help_text="Maximum price per kg")
    
    # Characteristics
    is_organic = models.BooleanField(default=True)
    texture_notes = models.TextField(help_text="Texture and flavor profile")
    origin_country = models.CharField(max_length=2, choices=COUNTRY_CHOICES, default='UG')
    
    # Inventory
    stock_kg = models.DecimalField(max_digits=10, decimal_places=2, default=0,
                                   help_text="Available stock in kilograms")
    
    image = models.ImageField(upload_to='coffee/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} - {self.roast_level}"


class CoffeeOrder(models.Model):
    """Coffee purchase orders"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('roasting', 'Roasting'),
        ('packaging', 'Packaging'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    CUSTOMER_TYPES = [
        ('consumer', 'Direct Consumer'),
        ('intermediary', 'Intermediary/Reseller'),
    ]
    
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='coffee_orders')
    product = models.ForeignKey(CoffeeProduct, on_delete=models.CASCADE, related_name='orders')
    customer_type = models.CharField(max_length=20, choices=CUSTOMER_TYPES, default='consumer')
    
    # Order details
    quantity_kg = models.DecimalField(max_digits=8, decimal_places=2, 
                                      help_text="Quantity in kilograms")
    unit_price = models.DecimalField(max_digits=8, decimal_places=2)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    
    # Delivery
    delivery_address = models.TextField()
    destination_country = models.CharField(max_length=2, choices=COUNTRY_CHOICES)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    order_number = models.CharField(max_length=50, unique=True)
    
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.order_number:
            import datetime
            self.order_number = f"CFE{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
        if not self.total_amount:
            self.total_amount = self.quantity_kg * self.unit_price
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.order_number} - {self.customer.get_full_name()}"


class ProductionLevel(models.Model):
    """Coffee production levels as per PDF"""
    name = models.CharField(max_length=50)
    level_number = models.IntegerField(unique=True, help_text="1, 2, 3, or 4")
    kg_per_week = models.DecimalField(max_digits=8, decimal_places=2)
    monthly_revenue_min = models.DecimalField(max_digits=12, decimal_places=2)
    monthly_revenue_max = models.DecimalField(max_digits=12, decimal_places=2)
    annual_revenue_min = models.DecimalField(max_digits=12, decimal_places=2)
    annual_revenue_max = models.DecimalField(max_digits=12, decimal_places=2)
    is_current = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['level_number']
    
    def __str__(self):
        return f"Level {self.level_number}: {self.kg_per_week}kg/week"
EOF

cat > coffee/admin.py << 'EOF'
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
EOF

cat > coffee/views.py << 'EOF'
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CoffeeProduct, CoffeeOrder, ProductionLevel

def coffee_home(request):
    """Coffee roasting business homepage"""
    products = CoffeeProduct.objects.filter(is_active=True)
    levels = ProductionLevel.objects.all()
    current_level = ProductionLevel.objects.filter(is_current=True).first()
    
    context = {
        'products': products,
        'levels': levels,
        'current_level': current_level,
    }
    return render(request, 'coffee/home.html', context)

def coffee_products(request):
    """List all coffee products"""
    products = CoffeeProduct.objects.filter(is_active=True)
    return render(request, 'coffee/products.html', {'products': products})

@login_required
def order_coffee(request, product_id):
    """Place a coffee order"""
    product = get_object_or_404(CoffeeProduct, pk=product_id, is_active=True)
    
    if request.method == 'POST':
        quantity_kg = float(request.POST.get('quantity_kg', 0))
        customer_type = request.POST.get('customer_type', 'consumer')
        delivery_address = request.POST.get('delivery_address', '')
        destination_country = request.POST.get('destination_country', 'UG')
        
        if quantity_kg > 0:
            order = CoffeeOrder.objects.create(
                customer=request.user,
                product=product,
                customer_type=customer_type,
                quantity_kg=quantity_kg,
                unit_price=product.price_per_kg,
                total_amount=quantity_kg * product.price_per_kg,
                delivery_address=delivery_address,
                destination_country=destination_country
            )
            messages.success(request, f'Coffee order {order.order_number} placed successfully!')
            return redirect('my_coffee_orders')
        else:
            messages.error(request, 'Please enter a valid quantity.')
    
    return render(request, 'coffee/order.html', {'product': product})

@login_required
def my_coffee_orders(request):
    """View user's coffee orders"""
    orders = CoffeeOrder.objects.filter(customer=request.user).order_by('-created_at')
    return render(request, 'coffee/my_orders.html', {'orders': orders})
EOF

cat > coffee/urls.py << 'EOF'
from django.urls import path
from . import views

urlpatterns = [
    path('', views.coffee_home, name='coffee_roasting'),
    path('products/', views.coffee_products, name='coffee_products'),
    path('order/<int:product_id>/', views.order_coffee, name='order_coffee'),
    path('my-orders/', views.my_coffee_orders, name='my_coffee_orders'),
]
EOF

echo "Coffee roasting app created successfully"

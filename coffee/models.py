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

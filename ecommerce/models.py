from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal


COUNTRY_CHOICES = [
    ('CA', 'Canada'), ('UG', 'Uganda'), ('US', 'USA'),
    ('NL', 'Netherlands'), ('KE', 'Kenya'),
]


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=100, blank=True, help_text="Font Awesome icon class")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class PartnerCompany(models.Model):
    """Partner companies that can list products and refer buyers"""
    name = models.CharField(max_length=200)
    unique_id = models.CharField(max_length=50, unique=True, help_text="Unique ID issued by management")
    country = models.CharField(max_length=2, choices=COUNTRY_CHOICES)
    contact_person = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Partner Companies'

    def __str__(self):
        return f"{self.name} ({self.unique_id})"


class Product(models.Model):
    MARKET_CHOICES = [('local', 'Local'), ('international', 'International'), ('both', 'Both')]

    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    partner_company = models.ForeignKey(PartnerCompany, on_delete=models.SET_NULL, 
                                       null=True, blank=True, related_name='products')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')
    title = models.CharField(max_length=300)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=5, default='USD')
    country = models.CharField(max_length=2, choices=COUNTRY_CHOICES)
    market_type = models.CharField(max_length=20, choices=MARKET_CHOICES, default='local')
    stock_quantity = models.PositiveIntegerField(default=1)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    video_url = models.URLField(blank=True, help_text="YouTube or product video URL")
    is_active = models.BooleanField(default=True)
    views_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class RFQ(models.Model):
    """Request for Quotation"""
    STATUS_CHOICES = [
        ('pending', 'Pending'), ('responded', 'Responded'), ('closed', 'Closed')
    ]
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rfqs')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='rfqs', null=True, blank=True)
    title = models.CharField(max_length=300)
    description = models.TextField()
    quantity = models.PositiveIntegerField(default=1)
    target_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    destination_country = models.CharField(max_length=2, choices=COUNTRY_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"RFQ: {self.title} by {self.buyer.get_full_name()}"


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Payment'),
        ('paid', 'Paid'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    PAYMENT_CHOICES = [
        ('mobile_money', 'Mobile Money'),
        ('etransfer', 'E-Transfer'),
        ('bank', 'Bank Transfer'),
    ]
    DELIVERY_CHOICES = [
        ('express', 'Express (Quick delivery - Higher shipping costs)'),
        ('ordinary', 'Ordinary (Normal delivery - Low shipping costs)'),
    ]

    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='orders')
    quantity = models.PositiveIntegerField(default=1)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=5, default='USD')
    payment_method = models.CharField(max_length=30, choices=PAYMENT_CHOICES)
    payment_reference = models.CharField(max_length=200, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Shipping details
    shipping_address = models.TextField()
    destination_country = models.CharField(max_length=2, choices=COUNTRY_CHOICES)
    delivery_type = models.CharField(max_length=20, choices=DELIVERY_CHOICES, default='ordinary')
    expected_delivery_date = models.DateField(null=True, blank=True)
    expected_delivery_time = models.TimeField(null=True, blank=True)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Referral tracking
    referred_by_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, 
                                         related_name='referred_orders')
    referred_by_company = models.ForeignKey(PartnerCompany, on_delete=models.SET_NULL, 
                                           null=True, blank=True, related_name='referred_orders')
    
    # Avon Points
    avon_points_earned = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    avon_points_awarded = models.BooleanField(default=False)
    
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Calculate Avon Points before saving
        if not self.avon_points_awarded and self.status == 'delivered':
            self.calculate_avon_points()
        super().save(*args, **kwargs)

    def calculate_avon_points(self):
        """
        Calculate Avon Points based on order type:
        - End user (no referral): 5.5% of total amount
        - Referred purchase: 8.5% of total amount
        Formula: (Price * Quantity) * percentage
        """
        base_amount = self.total_amount
        
        if self.referred_by_user or self.referred_by_company:
            # Referred purchase: 8.5%
            percentage = Decimal('0.085')
        else:
            # End user: 5.5%
            percentage = Decimal('0.055')
        
        self.avon_points_earned = base_amount * percentage
        return self.avon_points_earned

    def __str__(self):
        return f"Order #{self.pk} - {self.buyer.get_full_name()}"


class AvonPointsAccount(models.Model):
    """User's Avon Points account"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='avon_account')
    available_points = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_earned_points = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_redeemed_points = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.available_points} points"

    def add_points(self, amount, source):
        """Add points to account"""
        self.available_points += Decimal(str(amount))
        self.total_earned_points += Decimal(str(amount))
        self.save()
        
        # Create transaction record
        AvonPointsTransaction.objects.create(
            account=self,
            transaction_type='earn',
            amount=amount,
            source=source,
            balance_after=self.available_points
        )

    def redeem_points(self, amount, purpose):
        """Redeem points from account"""
        if self.available_points >= Decimal(str(amount)):
            self.available_points -= Decimal(str(amount))
            self.total_redeemed_points += Decimal(str(amount))
            self.save()
            
            # Create transaction record
            AvonPointsTransaction.objects.create(
                account=self,
                transaction_type='redeem',
                amount=amount,
                source=purpose,
                balance_after=self.available_points
            )
            return True
        return False


class AvonPointsTransaction(models.Model):
    """Transaction history for Avon Points"""
    TRANSACTION_TYPES = [
        ('earn', 'Earned'),
        ('redeem', 'Redeemed'),
        ('transfer', 'Transfer'),
    ]
    
    account = models.ForeignKey(AvonPointsAccount, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    source = models.CharField(max_length=200, help_text="Order ID, referral, conversion, etc.")
    balance_after = models.DecimalField(max_digits=15, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.transaction_type} - {self.amount} points ({self.created_at.date()})"


class AvonPointsSellOrder(models.Model):
    """Sell orders for Avon Points (quarterly system)"""
    QUARTER_CHOICES = [
        ('Q1', 'Quarter 1 (Jan-Mar)'),
        ('Q2', 'Quarter 2 (Apr-Jun)'),
        ('Q3', 'Quarter 3 (Jul-Sep)'),
        ('Q4', 'Quarter 4 (Oct-Dec)'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='points_sell_orders')
    points_amount = models.DecimalField(max_digits=12, decimal_places=2)
    quarter = models.CharField(max_length=2, choices=QUARTER_CHOICES)
    conversion_rate = models.DecimalField(max_digits=8, decimal_places=4, 
                                         help_text="Points to USD conversion rate")
    usd_amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    execution_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.points_amount} pts ({self.quarter})"

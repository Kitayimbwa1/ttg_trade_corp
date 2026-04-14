# Migration Guide - Upgrading to Enhanced T&TG System

## Overview
This guide helps you migrate from the original T&TG Trade Corp system to the enhanced version with Avon Points, Insurance, and Coffee modules.

## Pre-Migration Checklist

- [ ] Backup your current database
- [ ] Note down all custom settings
- [ ] Export any important data
- [ ] Test on a development environment first

## Step-by-Step Migration

### 1. Backup Current System
```bash
# Backup database
cp db.sqlite3 db.sqlite3.backup

# Backup media files
cp -r media media_backup
```

### 2. Install Updated Code
```bash
# Replace old directory with updated version
# (Keep your .env file and any custom configurations)
```

### 3. Update Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run New Migrations
```bash
# Create migrations for new apps
python manage.py makemigrations insurance
python manage.py makemigrations coffee
python manage.py makemigrations ecommerce

# Apply all migrations
python manage.py migrate
```

### 5. Create Avon Points Accounts for Existing Users
```bash
python manage.py shell
```

```python
from django.contrib.auth.models import User
from ecommerce.models import AvonPointsAccount
from decimal import Decimal

# Create Avon accounts for all existing users
for user in User.objects.all():
    account, created = AvonPointsAccount.objects.get_or_create(user=user)
    if created:
        # Optional: Give welcome bonus
        account.add_points(Decimal('100.00'), 'Migration welcome bonus')
        print(f"Created Avon account for {user.username}")
```

### 6. Update Partner Companies (if you have existing suppliers)
```bash
python manage.py shell
```

```python
from ecommerce.models import PartnerCompany

# Create partner company records for your existing partners
PartnerCompany.objects.create(
    name='Your Partner Name',
    unique_id='PARTNER001',
    country='UG',
    contact_person='Contact Name',
    email='partner@example.com',
    phone='+256700000000',
    is_active=True
)
```

### 7. Seed New Module Data (Optional)
```bash
# Load insurance products, coffee products, production levels
python manage.py seed_data_updated
```

**Note**: This will create sample data. Skip if you want to add your own products.

### 8. Update Existing Orders (if needed)
```bash
python manage.py shell
```

```python
from ecommerce.models import Order
from decimal import Decimal

# Calculate and award Avon Points for delivered orders
delivered_orders = Order.objects.filter(
    status='delivered',
    avon_points_awarded=False
)

for order in delivered_orders:
    points = order.calculate_avon_points()
    order.avon_points_awarded = True
    order.save()
    
    # Add points to user's account
    account = order.buyer.avon_account
    account.add_points(points, f'Order #{order.id}')
    print(f"Awarded {points} points for Order #{order.id}")
```

### 9. Verify Navigation
The main navigation has been updated:
- "Forex" is now under "Financial Services & Investments" dropdown
- New "Coffee" menu item added
- Avon Points badge appears in navbar for logged-in users

### 10. Test Core Features
- [ ] User login/registration
- [ ] Product browsing
- [ ] Order placement with delivery options
- [ ] Avon Points earning on orders
- [ ] Insurance product viewing
- [ ] Coffee product viewing
- [ ] Dashboard access

## Database Schema Changes

### New Tables:
- `ecommerce_partnercompany` - Partner companies
- `ecommerce_avonpointsaccount` - User points accounts
- `ecommerce_avonpointstransaction` - Transaction history
- `ecommerce_avonpointssellorder` - Quarterly sell orders
- `insurance_insuranceproduct` - Insurance products
- `insurance_insurancepolicy` - User policies
- `insurance_insuranceclaim` - Claims
- `coffee_coffeeproduct` - Coffee products
- `coffee_coffeeorder` - Coffee orders
- `coffee_productionlevel` - Production tiers

### Modified Tables:
- `ecommerce_order` - Added delivery_type, expected_delivery_date, expected_delivery_time, shipping_cost, referred_by_user, referred_by_company, avon_points_earned, avon_points_awarded
- `ecommerce_product` - Added partner_company, video_url

## Configuration Updates

### settings.py
```python
INSTALLED_APPS = [
    # ... existing apps ...
    'insurance',  # NEW
    'coffee',     # NEW
]
```

### urls.py
```python
urlpatterns = [
    # ... existing patterns ...
    path('insurance/', include('insurance.urls')),  # NEW
    path('coffee/', include('coffee.urls')),        # NEW
]
```

## Troubleshooting

### Issue: Migration conflicts
**Solution**: 
```bash
python manage.py migrate --fake-initial
```

### Issue: Avon Points not appearing
**Solution**: Ensure user has an AvonPointsAccount
```python
from ecommerce.models import AvonPointsAccount
account, created = AvonPointsAccount.objects.get_or_create(user=request.user)
```

### Issue: Missing templates
**Solution**: Ensure all template directories exist:
```bash
mkdir -p templates/insurance
mkdir -p templates/coffee
mkdir -p templates/ecommerce/avon
```

## Rollback Plan

If you need to rollback:

```bash
# Restore database backup
cp db.sqlite3.backup db.sqlite3

# Restore media files
cp -r media_backup media

# Revert code to previous version
```

## Post-Migration Tasks

1. **Update Admin Panel**
   - Add insurance products
   - Set up coffee production levels
   - Configure Avon Points conversion rates

2. **Configure Email Notifications**
   - Order confirmations with Avon Points details
   - Insurance policy confirmations
   - Quarterly sell order notifications

3. **Test Workflows**
   - Complete order with referral
   - Verify Avon Points calculation
   - Create insurance policy
   - Place coffee order

4. **Update Documentation**
   - User guides for Avon Points
   - Partner company onboarding
   - Insurance claim process

## Support

If you encounter issues during migration:
1. Check logs: `tail -f debug.log`
2. Verify database migrations: `python manage.py showmigrations`
3. Test in Django shell: `python manage.py shell`

---

**Migration Version**: 1.0 → 2.0  
**Estimated Time**: 30-60 minutes  
**Complexity**: Medium

# T&TG Trade Corporation - System Updates
## PDF Implementation Summary

This updated version implements all requirements from the Business_Details PDF document.

## 🆕 New Features Implemented

### 1. **Financial Services & Investments** (renamed from Forex)
The main menu now features "Financial Services & Investments" with three sub-sections:
- **Insurance** - Full insurance module with policies and claims
- **Online Shopping Platform** - Enhanced marketplace with Avon Points
- **T&TG Brokerage** - Forex trading platform

### 2. **Avon Points Rewards System** ⭐
Complete loyalty rewards system as specified in PDF:

#### Earning Points:
- **5.5%** of purchase amount for end users/consumers
- **8.5%** of purchase amount for referred purchases
- Points awarded only on delivered orders

#### Using Points:
- Convert to funds through **quarterly sell orders** (Q1, Q2, Q3, Q4)
- **Minimum 3-month execution period** for sell orders
- Pay **insurance premiums** with Avon Points
- Transfer to **trading platform**
- **Invest in real estate**
- **Cash withdrawals**

#### Models:
- `AvonPointsAccount` - User balance and totals
- `AvonPointsTransaction` - Complete transaction history
- `AvonPointsSellOrder` - Quarterly conversion system

### 3. **Enhanced Order System**
Following PDF workflow (Steps 1-4):

#### Delivery Options:
- **Express** - Quick delivery, higher shipping costs
- **Ordinary** - Normal delivery, low shipping costs
- Expected delivery date/time selection

#### Referral Tracking:
- Partner company referrals with unique IDs
- Individual user referrals
- Automatic Avon Points calculation based on referral status

#### Market Types:
- **Local Market** - Individuals can buy, Partners & Individuals can refer
- **International Market** - Partner companies only for both buying and referring

### 4. **Partner Company System**
Manage business partnerships across countries:
- Unique ID issuance from management
- Partner companies can list products
- Refer buyers and earn commissions
- Track referral performance

### 5. **Insurance Module** 🛡️
Full insurance product management:

#### Products:
- Life Insurance
- Health Insurance
- Property Insurance
- Business Insurance
- Travel Insurance

#### Features:
- Policy management with policy numbers
- Premium frequency (monthly, quarterly, annual)
- Beneficiary designation
- Claims processing system
- Pay premiums with **Avon Points**

### 6. **Coffee Roasting Business** ☕
Complete coffee roasting company module per PDF specifications:

#### Production Levels (as per PDF):
- **Level 1**: 25 kg/week → $875-$1,375/month → $10,500-$16,500/year
- **Level 2**: 50 kg/week → $1,750-$2,750/month → $21,000-$33,000/year
- **Level 3**: 75 kg/week → $2,625-$4,125/month → $31,500-$49,500/year
- **Level 4**: 100 kg/week → $14,000-$22,000/month → $168,000-$264,000/year

#### Coffee Features:
- **100% Organic** Arabica coffee
- **Superior texture** and flavor profiles
- Price range: **$35-$55 per kg**
- Origin: Uganda
- Multiple roast levels (Light, Medium, Dark)
- Direct to consumers or intermediaries

### 7. **Updated Countries**
Now operating in 5 countries as specified:
- 🇨🇦 **Canada** (HQ - Toronto)
- 🇺🇬 **Uganda**
- 🇺🇸 **USA**
- 🇳🇱 **Netherlands**
- 🇰🇪 **Kenya**

## 📁 New Apps Structure

```
ttg_trade_updated/
├── insurance/          # NEW - Insurance products, policies, claims
├── coffee/            # NEW - Coffee roasting business
├── ecommerce/         # ENHANCED - Now with Avon Points & referrals
│   ├── models.py      # Added: PartnerCompany, Avon* models
│   ├── avon_views.py  # NEW - Avon Points management
│   └── ...
└── ...
```

## 🗄️ Database Models Added/Updated

### New Models:
1. `PartnerCompany` - Partner company management
2. `AvonPointsAccount` - User rewards account
3. `AvonPointsTransaction` - Transaction history
4. `AvonPointsSellOrder` - Quarterly sell orders
5. `InsuranceProduct` - Insurance offerings
6. `InsurancePolicy` - User policies
7. `InsuranceClaim` - Claims processing
8. `CoffeeProduct` - Roasted coffee products
9. `CoffeeOrder` - Coffee purchase orders
10. `ProductionLevel` - Coffee production tiers

### Enhanced Models:
- `Order` - Added delivery options, referral tracking, Avon Points
- `Product` - Added partner company link, video URL field

## 🔄 Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Load Seed Data
```bash
python manage.py seed_data_updated
```

This creates:
- Admin user (admin/admin123)
- Leadership team (tom, edgar, michael, francis)
- Partner companies with unique IDs
- Sample products across all categories
- Avon Points accounts with welcome bonuses
- Insurance products
- Coffee products with production levels
- Training courses

### 4. Create Superuser (if needed)
```bash
python manage.py createsuperuser
```

### 5. Run Development Server
```bash
python manage.py runserver
```

## 🎯 Key URLs

### Public Pages:
- `/` - Homepage
- `/insurance/` - Insurance products
- `/coffee/` - Coffee roasting business
- `/trade/` - Marketplace

### User Dashboard:
- `/dashboard/` - Main user dashboard
- `/avon/` - Avon Points dashboard
- `/avon/sell-order/` - Create quarterly sell order
- `/avon/redeem/` - Redeem points
- `/avon/referrals/` - Referral tracking
- `/insurance/my-policies/` - My insurance policies
- `/coffee/my-orders/` - My coffee orders

### Admin:
- `/admin/` - Django admin panel

## 💰 Avon Points Calculation Examples

### End User Purchase:
```
Product: Laptop @ $1,000
Quantity: 1
Points Earned: $1,000 × 5.5% = 55 Avon Points
```

### Referred Purchase:
```
Product: Printer @ $500
Quantity: 2
Total: $1,000
Points Earned: $1,000 × 8.5% = 85 Avon Points
```

### Quarterly Sell Order:
```
Available Points: 1,000
Conversion Rate: $0.95 per point
USD Amount: 1,000 × $0.95 = $950.00
Execution: Minimum 3 months (Q1, Q2, Q3, or Q4)
```

## 📊 Business Model Implementation

### Marketplace Platform:
✅ Connects buyers and sellers globally
✅ Local & International market separation
✅ Partner company integration
✅ Referral commission system

### Revenue Streams:
✅ Product sales commissions
✅ Insurance premiums
✅ Coffee roasting operations
✅ Forex brokerage fees
✅ Training course sales
✅ Affiliate/advertising (Google Ads ready)

### Avon Points Economics:
✅ Encourages repeat purchases
✅ Rewards referrals
✅ Quarterly liquidation system
✅ Multi-use redemption (insurance, trading, real estate, cash)

## 🎨 Design System

### Colors:
- **Navy**: #0a0f1e (Primary background)
- **Gold**: #c9a84c (Accents, CTAs)
- **Cream**: #fdf8ef (Text)

### Typography:
- **Headings**: Cormorant Garamond (serif)
- **Body**: DM Sans (sans-serif)

## 📱 Navigation Structure

```
Home
About
Marketplace
Financial Services & Investments ▾
  ├─ Insurance
  ├─ Online Shopping Platform
  └─ T&TG Brokerage
Training
Coffee
Contact
[Avon Points Badge] [Notifications] [Dashboard]
```

## 🔐 User Roles & Permissions

### End Users/Consumers:
- Purchase products
- Earn 5.5% Avon Points
- Refer others for 8.5% rate
- Buy insurance
- Order coffee
- Create sell orders

### Partner Companies:
- List products on platform
- Refer buyers (international market)
- Receive unique IDs from management
- Track referral earnings

### Admin:
- Manage all products
- Process insurance claims
- Approve sell orders
- Manage production levels
- Monitor Avon Points system

## 📈 Production Levels Dashboard

The coffee module tracks current production level and displays projections for all four tiers, making it easy to visualize growth targets.

## 🌍 Multi-Currency Support

- Primary: USD
- Supports: CAD, UGX, EUR, GBP, KES
- Forex rates managed through admin

## 🛠️ Technical Stack

- **Backend**: Django 4.2+
- **Frontend**: Bootstrap 5, vanilla JS
- **Database**: SQLite (dev), PostgreSQL-ready
- **Forms**: Django Forms with custom widgets
- **Admin**: Enhanced Django Admin

## 📝 Notes for Deployment

1. Update `SECRET_KEY` in production
2. Set `DEBUG = False`
3. Configure `ALLOWED_HOSTS`
4. Set up PostgreSQL database
5. Configure email backend for notifications
6. Set up media file storage (S3/CloudFront)
7. Configure payment gateway for Avon Points conversions
8. Set up SSL certificate

## 🚀 Future Enhancements (Not in Current Version)

- Real-time Avon Points conversion rates
- Automated quarterly sell order execution
- Real estate investment portal
- Mobile apps (iOS/Android)
- Payment gateway integration
- Google Ads integration
- Advanced analytics dashboard

## 📞 Support

For technical support or business inquiries:
- Email: info@ttgtrade.com
- Based in: Toronto, Canada

---

**Version**: 2.0 (PDF Implementation Complete)  
**Last Updated**: April 2026  
**Company**: T&TG Trade Corporation

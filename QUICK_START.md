# Quick Start Guide - T&TG Trade Corp

## 🚀 Get Started in 3 Steps

### 1️⃣ Extract & Navigate
```bash
unzip ttg_trade_corp_updated.zip
cd ttg_trade_updated
```

### 2️⃣ Run Setup
```bash
# Windows (Git Bash)
bash SETUP.sh

# Mac/Linux
./SETUP.sh
```

### 3️⃣ Start Server
```bash
python manage.py runserver
```

Visit: **http://127.0.0.1:8000**

## 🔑 Login Credentials

### Admin Panel
- URL: http://127.0.0.1:8000/admin
- Username: `admin`
- Password: `admin123`

### Test Users
- `tom` / `demo123` (CEO)
- `edgar` / `demo123` (Manager)
- `buyer1` / `demo123` (Customer)

## 🎯 Key Features to Try

### 1. Avon Points System
1. Login as `buyer1`
2. Go to **Dashboard** → **Avon Points**
3. View your 500 welcome bonus points
4. Create a **Sell Order** for Q1-Q4

### 2. Make a Purchase & Earn Points
1. Browse **Marketplace**
2. Add product to cart
3. Complete order (choose Express/Ordinary delivery)
4. Earn **5.5%** in Avon Points when order is delivered

### 3. Use a Referral Code
1. When ordering, enter referral code: `TTG000002`
2. Referrer earns **8.5%** instead of 5.5%

### 4. Browse Insurance
1. Go to **Financial Services** → **Insurance**
2. View insurance products
3. Purchase policy (can pay with Avon Points!)

### 5. Order Coffee
1. Go to **Coffee** menu
2. View production levels
3. Order roasted coffee (organic Arabica from Uganda)

## 📱 Navigation Map

```
Home → Company overview
About → Leadership & team
Marketplace → Products with Avon Points
Financial Services ▾
  ├─ Insurance → Policies & claims
  ├─ Shopping Platform → Same as Marketplace
  └─ T&TG Brokerage → Forex trading
Training → Courses
Coffee → Roasting business
Contact → Get in touch
```

## 💡 Pro Tips

### Earning More Avon Points
- **Refer friends**: Share code `TTG00000X` (where X is your user ID)
- **Bulk orders**: More quantity = more points
- **Be a reseller**: Partner companies get special rates

### Redeeming Points
- Min sell order: **100 points**
- Conversion rate: **~$0.95 per point**
- Execution time: **3+ months**
- Use for: Insurance, trading, real estate, cash

### Coffee Business
- Current: **Level 1** (25kg/week)
- Revenue: **$10,500-$16,500/year**
- Price range: **$35-$55/kg**
- Roast levels: Light, Medium, Dark

## 🛠️ Admin Tasks

### Add Products
1. Login to `/admin`
2. Go to **Ecommerce** → **Products**
3. Click **Add Product**
4. Set market type (Local/International/Both)

### Manage Partner Companies
1. **Ecommerce** → **Partner Companies**
2. Add company with **Unique ID**
3. They can now list products & refer buyers

### Process Insurance Claims
1. **Insurance** → **Insurance Claims**
2. Review submitted claims
3. Update status & settlement amount

### Update Production Level
1. **Coffee** → **Production Levels**
2. Mark current level (sets "Current" badge)

## 📊 Understanding the System

### Market Types
- **Local**: Individuals buy & refer
- **International**: Partner companies only
- **Both**: Available to all

### Delivery Options
- **Express**: Fast, higher cost
- **Ordinary**: Normal, low cost

### User Types
- **End User**: 5.5% points on own purchases
- **Referrer**: 8.5% points when someone uses their code
- **Partner Company**: Can list products & refer

## 🐛 Common Issues

**Issue**: Server won't start  
**Fix**: Check if port 8000 is in use
```bash
python manage.py runserver 8080
```

**Issue**: No Avon Points showing  
**Fix**: Ensure order status is "delivered"

**Issue**: Can't login  
**Fix**: Reset password in admin panel

## 📚 Documentation

- Full documentation: `README_UPDATES.md`
- Migration guide: `MIGRATION_GUIDE.md`
- Original README: `README.md`

## 🌍 Countries Supported

🇨🇦 Canada (HQ) | 🇺🇬 Uganda | 🇺🇸 USA | 🇳🇱 Netherlands | 🇰🇪 Kenya

## 💬 Need Help?

Check these files:
- `README_UPDATES.md` - Feature details
- `MIGRATION_GUIDE.md` - Upgrading guide
- Django admin - Live system configuration

---

**Happy Trading!** 🚀

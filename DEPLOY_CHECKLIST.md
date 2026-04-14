# ✅ Render Deployment Checklist

Quick checklist for deploying T&TG Trade Corp to Render.

---

## 🎯 Before You Start

- [ ] GitHub account created
- [ ] Render account created (free tier OK)
- [ ] Git installed on your computer

---

## 📦 Step 1: Push to GitHub (5 minutes)

```bash
cd ttg_trade_updated
git init
git add .
git commit -m "Ready for deployment"
git remote add origin https://github.com/YOUR_USERNAME/ttg-trade-corp.git
git push -u origin main
```

- [ ] Code pushed to GitHub successfully
- [ ] Repository is public or Render has access

---

## 🗄️ Step 2: Create Database (2 minutes)

On Render Dashboard:

1. Click **New +** → **PostgreSQL**
2. Fill in:
   - [ ] Name: `ttg-trade-db`
   - [ ] Database: `ttg_trade_db`
   - [ ] User: `ttg_trade_user`
   - [ ] Region: Oregon (Free)
   - [ ] Plan: Free
3. Click **Create Database**
4. [ ] Copy **Internal Database URL** (save it!)

---

## 🚀 Step 3: Create Web Service (5 minutes)

On Render Dashboard:

1. Click **New +** → **Web Service**
2. Connect GitHub repository
3. Configure:
   - [ ] Name: `ttg-trade-corp`
   - [ ] Region: Oregon
   - [ ] Branch: `main`
   - [ ] Build Command: `./build.sh`
   - [ ] Start Command: `gunicorn ttg_trade.wsgi:application`
   - [ ] Plan: Free

---

## 🔐 Step 4: Set Environment Variables (3 minutes)

Click **Add Environment Variable** for each:

- [ ] `PYTHON_VERSION` = `3.11.0`
- [ ] `DJANGO_DEBUG` = `False`
- [ ] `SECRET_KEY` = Click **Generate**
- [ ] `DATABASE_URL` = Paste Internal Database URL from Step 2
- [ ] `ALLOWED_HOSTS` = `your-app-name.onrender.com`

Then:
- [ ] Click **Create Web Service**

---

## ⏳ Step 5: Wait for Deployment (5-10 minutes)

Watch the logs. You should see:

- [ ] Installing dependencies...
- [ ] Running collectstatic...
- [ ] Running migrations...
- [ ] Creating superuser...
- [ ] Loading seed data...
- [ ] **Deploy successful!** ✅

---

## 🎉 Step 6: Test Your Site (5 minutes)

Visit: `https://your-app-name.onrender.com`

Test these features:

- [ ] Homepage loads
- [ ] Can browse marketplace
- [ ] Can view insurance products
- [ ] Can view coffee products
- [ ] Navigation dropdown works
- [ ] Admin panel accessible at `/admin`

---

## 🔑 Step 7: Secure Admin (2 minutes)

1. Login to admin: 
   - Username: `admin`
   - Password: `Admin2026!SecurePassword`
2. [ ] Change password immediately
3. [ ] Create your personal admin account

---

## 🧪 Step 8: Test Core Features (10 minutes)

Create a test user and verify:

- [ ] User registration works
- [ ] User can login
- [ ] User can view Avon Points dashboard (500 welcome points)
- [ ] User can browse products
- [ ] User can place an order
- [ ] Delivery options appear (Express/Ordinary)
- [ ] Avon Points are calculated correctly

---

## 📧 Step 9: Configure Email (Optional, 10 minutes)

If you want email notifications:

- [ ] Set up SendGrid account (free tier)
- [ ] Add SendGrid API key to environment variables
- [ ] Test password reset email

---

## 🌐 Step 10: Custom Domain (Optional, 30 minutes)

If you have a domain:

- [ ] Add custom domain in Render dashboard
- [ ] Update DNS records at your registrar
- [ ] Wait for SSL certificate (automatic)
- [ ] Update `ALLOWED_HOSTS` environment variable

---

## ✅ Final Verification

All systems go?

- [ ] Site loads on custom domain (or .onrender.com)
- [ ] HTTPS is working (green padlock)
- [ ] Admin panel secured
- [ ] Database connected
- [ ] Static files loading
- [ ] No errors in logs

---

## 🎊 You're Live!

**Your URL**: `https://your-app-name.onrender.com`

### What's Included:

✅ **Avon Points System** - Users earning 5.5% / 8.5% rewards
✅ **Insurance Module** - 5 product types ready
✅ **Coffee Business** - 4 production levels configured
✅ **Partner System** - Referral tracking active
✅ **E-commerce** - Full marketplace with delivery options

### Pre-loaded Demo Data:

- **Admin**: admin / (password you set)
- **Test Users**: tom, edgar, michael, francis / demo123
- **Products**: Sample laptops, printers, coffee
- **Insurance**: 3 products ready
- **Avon Points**: All users have 500 point welcome bonus

---

## 📊 Monitoring Your App

Check regularly:

- **Logs**: Dashboard → Service → Logs
- **Metrics**: Dashboard → Service → Metrics
- **Database**: Dashboard → Database → Usage

---

## 🆘 If Something Goes Wrong

1. Check build logs for errors
2. Verify all environment variables are set
3. Confirm DATABASE_URL is the Internal URL
4. Review `RENDER_DEPLOYMENT_GUIDE.md` for detailed troubleshooting

---

## 📞 Quick Links

- **Your Site**: https://your-app-name.onrender.com
- **Admin Panel**: https://your-app-name.onrender.com/admin
- **Render Dashboard**: https://dashboard.render.com
- **Database**: https://dashboard.render.com (your database)

---

**Total Time**: ~30-45 minutes
**Cost**: $0/month (Free tier)

🚀 **Congratulations! T&TG Trade Corp is now live!**

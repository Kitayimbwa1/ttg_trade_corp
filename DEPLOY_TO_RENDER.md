# 🚀 Deploy to Render - Quick Guide

## ⚡ Fast Track (5 Minutes)

### 1️⃣ Push to GitHub
```bash
git init
git add .
git commit -m "T&TG Trade Corp - Ready for Render"
git remote add origin https://github.com/YOUR-USERNAME/ttg-trade-corp.git
git push -u origin main
```

### 2️⃣ Create Render Services

#### Database First:
1. Go to https://render.com/dashboard
2. Click **New +** → **PostgreSQL**
3. Settings:
   - Name: `ttg-trade-db`
   - Database: `ttgtrade`
   - Region: Oregon (or closest)
   - Plan: **Free** (or Starter $7/mo)
4. Click **Create Database**
5. **📋 COPY the "Internal Database URL"** - you need this!

#### Web Service:
1. Click **New +** → **Web Service**
2. Connect your GitHub repo
3. Settings:
   - Name: `ttg-trade-corp` (or your choice)
   - Region: Oregon (same as database!)
   - Runtime: **Python 3**
   - Build Command: `./build.sh`
   - Start Command: `gunicorn ttg_trade.wsgi:application`
   - Plan: **Free** (or Starter $7/mo)

### 3️⃣ Environment Variables

Click "Advanced" → Add these environment variables:

| Key | Value |
|-----|-------|
| `PYTHON_VERSION` | `3.11.0` |
| `DJANGO_SETTINGS_MODULE` | `ttg_trade.settings_production` |
| `DJANGO_DEBUG` | `False` |
| `DJANGO_SECRET_KEY` | *Click "Generate"* |
| `DATABASE_URL` | *Paste from Step 2* |
| `ALLOWED_HOSTS` | `your-app-name.onrender.com` |
| `DJANGO_SUPERUSER_USERNAME` | `admin` |
| `DJANGO_SUPERUSER_EMAIL` | `admin@ttgtrade.com` |
| `DJANGO_SUPERUSER_PASSWORD` | *Create secure password* |

### 4️⃣ Deploy!
Click **Create Web Service** → Wait 5-10 minutes

### 5️⃣ Access Your Site
- **Website**: `https://your-app-name.onrender.com`
- **Admin**: `https://your-app-name.onrender.com/admin`
- **Login**: Use the superuser credentials from Step 3

---

## 🎯 Post-Deployment

### Load Demo Data
1. Go to Render Dashboard → Your Service → **Shell**
2. Run:
```bash
python manage.py seed_data_updated
```

### Test Features
- ✅ Login to admin panel
- ✅ Browse marketplace
- ✅ Check Avon Points system
- ✅ View insurance products
- ✅ Browse coffee catalog

---

## ⚙️ Important Settings

### Update Allowed Hosts
After deployment, update the environment variable:
```
ALLOWED_HOSTS=ttg-trade-corp.onrender.com,www.yourdomain.com
```

### Media Files Warning
**Free tier**: Uploaded files are deleted on each deployment.

**Solutions**:
- Upgrade to Starter plan ($7/mo) for persistent storage
- Use AWS S3 / Cloudinary for media files

---

## 💡 Quick Tips

**Build Taking Too Long?**
- Check build logs for errors
- First build takes 5-10 minutes
- Subsequent builds: 2-3 minutes

**500 Error on First Visit?**
- Check logs: Dashboard → Logs
- Verify DATABASE_URL is set
- Ensure build completed successfully

**Static Files Not Loading?**
- Build script runs `collectstatic` automatically
- Clear browser cache
- Check `whitenoise` is in MIDDLEWARE

---

## 📚 Full Documentation

For complete details, see:
- **RENDER_DEPLOYMENT_GUIDE.md** - Comprehensive deployment guide
- **README_UPDATES.md** - Feature documentation
- **QUICK_START.md** - Local development guide

---

## 🆘 Common Issues

| Issue | Solution |
|-------|----------|
| Build fails | Check `requirements.txt`, verify Python version |
| Database error | Verify `DATABASE_URL` environment variable |
| Static files missing | Ensure `./build.sh` runs successfully |
| Admin CSS broken | Run `collectstatic`, clear browser cache |
| Can't login | Check superuser was created in build logs |

---

## 💰 Costs

- **Free**: $0/month (web service free for 750 hrs, DB free for 90 days)
- **Basic**: $14/month (web + database on Starter plan)
- **Production**: $45/month (Standard plans)

---

## ✅ Deployment Checklist

- [ ] Code pushed to GitHub
- [ ] PostgreSQL database created on Render
- [ ] Internal Database URL copied
- [ ] Web service created
- [ ] All environment variables set
- [ ] Build completed successfully
- [ ] Site accessible via HTTPS
- [ ] Admin panel works
- [ ] Superuser can login
- [ ] Demo data loaded (optional)

---

**Your T&TG Trade Corp is now LIVE! 🎉**

Next: Custom domain, email setup, monitoring

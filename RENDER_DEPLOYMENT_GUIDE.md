# 🚀 Render Deployment Guide - T&TG Trade Corp

Complete step-by-step guide to deploy T&TG Trade Corp on Render with PostgreSQL.

---

## 📋 Prerequisites

- GitHub account
- Render account (free tier works)
- Git installed locally

---

## 🎯 Deployment Steps

### Step 1: Push to GitHub

```bash
# Navigate to project directory
cd ttg_trade_updated

# Initialize git repository
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - T&TG Trade Corp ready for Render"

# Create repository on GitHub (via web interface)
# Then link and push:
git remote add origin https://github.com/YOUR_USERNAME/ttg-trade-corp.git
git branch -M main
git push -u origin main
```

---

### Step 2: Create Render Account

1. Go to [render.com](https://render.com)
2. Sign up (can use GitHub OAuth)
3. Verify email

---

### Step 3: Deploy PostgreSQL Database

1. From Render Dashboard, click **"New +"**
2. Select **"PostgreSQL"**
3. Configure:
   - **Name**: `ttg-trade-db`
   - **Database**: `ttg_trade_db`
   - **User**: `ttg_trade_user`
   - **Region**: Oregon (Free)
   - **Plan**: Free
4. Click **"Create Database"**
5. Wait for database to provision (~2 minutes)
6. **Save the Internal Database URL** (you'll need it)

---

### Step 4: Deploy Web Service

1. From Render Dashboard, click **"New +"**
2. Select **"Web Service"**
3. Connect your GitHub repository
4. Configure:

**Basic Settings:**
- **Name**: `ttg-trade-corp`
- **Region**: Oregon (Free)
- **Branch**: `main`
- **Root Directory**: (leave empty)
- **Environment**: Python 3
- **Build Command**: `./build.sh`
- **Start Command**: `gunicorn ttg_trade.wsgi:application`

**Environment Variables** (click "Add Environment Variable"):

| Key | Value |
|-----|-------|
| `PYTHON_VERSION` | `3.11.0` |
| `DJANGO_DEBUG` | `False` |
| `SECRET_KEY` | Click "Generate" button |
| `DATABASE_URL` | Paste Internal Database URL from Step 3 |
| `ALLOWED_HOSTS` | `your-app-name.onrender.com` |

**Advanced Settings:**
- **Plan**: Free
- **Auto-Deploy**: Yes

5. Click **"Create Web Service"**

---

### Step 5: Monitor Deployment

1. Watch the build logs in real-time
2. Build process will:
   - Install dependencies
   - Run migrations
   - Collect static files
   - Create superuser
   - Load seed data
3. Wait for **"Deploy successful"** message (~5-10 minutes)

---

### Step 6: Access Your Application

Your app will be live at:
```
https://your-app-name.onrender.com
```

**Admin Panel:**
```
https://your-app-name.onrender.com/admin
Username: admin
Password: Admin2026!SecurePassword
```

**⚠️ IMPORTANT**: Change the admin password immediately after first login!

---

## 🔧 Configuration Details

### Environment Variables Explained

| Variable | Purpose | Required |
|----------|---------|----------|
| `DATABASE_URL` | PostgreSQL connection string | ✅ Yes |
| `SECRET_KEY` | Django secret key for security | ✅ Yes |
| `DJANGO_DEBUG` | Debug mode (False in production) | ✅ Yes |
| `ALLOWED_HOSTS` | Allowed domain names | ✅ Yes |
| `PYTHON_VERSION` | Python runtime version | ✅ Yes |

### Build Script (build.sh)

Automatically runs on each deployment:
```bash
1. Install dependencies (pip install -r requirements.txt)
2. Collect static files (collectstatic)
3. Run database migrations
4. Create superuser if doesn't exist
5. Load initial data (products, insurance, coffee, etc.)
```

---

## 📊 Database Management

### Access PostgreSQL Shell

1. Go to your database on Render Dashboard
2. Click **"Connect"** → **"PSQL Command"**
3. Copy command and run locally:
```bash
PGPASSWORD=your_password psql -h hostname -U username database_name
```

### Database Backups

Render Free tier includes:
- Automatic daily backups (7 days retention)
- Manual backups available

To create manual backup:
1. Go to database dashboard
2. Click **"Backups"**
3. Click **"Create Backup"**

---

## 🔒 Security Checklist

After deployment, ensure:

- [ ] Changed default admin password
- [ ] `DJANGO_DEBUG` is `False`
- [ ] `SECRET_KEY` is unique and secure
- [ ] `ALLOWED_HOSTS` contains only your domains
- [ ] SSL/HTTPS is enabled (automatic on Render)
- [ ] Database password is strong

---

## 📁 Static Files & Media

### Static Files (CSS, JS)
- Handled by **WhiteNoise** (configured)
- Automatically served from `/staticfiles/`
- Compressed for performance

### Media Files (User Uploads)
**⚠️ Important**: Render's free tier has ephemeral storage

For production, configure cloud storage:

**Option 1: AWS S3** (Recommended)
```python
# Add to settings_production.py
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
```

**Option 2: Cloudinary** (Free tier available)
```python
# Install: pip install django-cloudinary-storage
# Add to INSTALLED_APPS
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.environ.get('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': os.environ.get('CLOUDINARY_API_KEY'),
    'API_SECRET': os.environ.get('CLOUDINARY_API_SECRET'),
}
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
```

---

## 🐛 Troubleshooting

### Issue: Build Fails

**Check:**
1. Build logs for specific error
2. `requirements.txt` has all dependencies
3. `build.sh` has execute permissions
4. Python version matches `runtime.txt`

**Solution:**
```bash
# Test locally first
pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
```

### Issue: Database Connection Error

**Check:**
1. `DATABASE_URL` environment variable is set
2. Database is running (check Render dashboard)
3. Internal Database URL is used (not External)

**Solution:**
- Copy Internal Database URL from database dashboard
- Update `DATABASE_URL` environment variable
- Redeploy

### Issue: Static Files Not Loading

**Check:**
1. WhiteNoise is in `MIDDLEWARE`
2. `STATIC_ROOT` is set correctly
3. `collectstatic` ran during build

**Solution:**
```bash
# Manual trigger
python manage.py collectstatic --no-input
```

### Issue: Admin Login Fails

**Reset admin password:**
1. Access Render Shell:
   - Dashboard → Your Service → Shell
2. Run:
```python
python manage.py shell
from django.contrib.auth import get_user_model
User = get_user_model()
admin = User.objects.get(username='admin')
admin.set_password('NewSecurePassword123!')
admin.save()
exit()
```

### Issue: 502 Bad Gateway

**Causes:**
- App crashed during startup
- Port binding issue
- Gunicorn not starting

**Solution:**
- Check logs: Dashboard → Service → Logs
- Ensure `gunicorn` is in `requirements.txt`
- Verify start command: `gunicorn ttg_trade.wsgi:application`

---

## 📈 Performance Optimization

### Free Tier Limitations
- App spins down after 15 minutes of inactivity
- First request after spin-down takes ~30 seconds
- 512 MB RAM
- Shared CPU

### Upgrade to Paid Plan ($7/month)
Benefits:
- No spin-down
- 512 MB - 8 GB RAM options
- Dedicated CPU
- More concurrent requests

### Optimization Tips
1. **Database Query Optimization**
   - Use `select_related()` and `prefetch_related()`
   - Add database indexes
   
2. **Caching**
   - Add Redis for session storage
   - Cache expensive queries

3. **Static File CDN**
   - Serve static files via CDN
   - Reduces server load

---

## 🔄 Continuous Deployment

### Auto-Deploy on Git Push

Already configured! Every push to `main` branch triggers:
1. Automatic rebuild
2. New deployment
3. Zero-downtime rollout

### Manual Deploy

From Render Dashboard:
1. Go to your service
2. Click **"Manual Deploy"** 
3. Select branch
4. Click **"Deploy"**

---

## 📊 Monitoring & Logs

### View Logs
Dashboard → Service → **Logs**

Shows:
- Application logs
- Error messages
- Request logs
- Django system logs

### Metrics
Dashboard → Service → **Metrics**

Monitor:
- Memory usage
- CPU usage
- Request count
- Response time

---

## 🌐 Custom Domain Setup

### Add Custom Domain

1. Purchase domain (Namecheap, GoDaddy, etc.)
2. In Render Dashboard:
   - Service → Settings → **Custom Domains**
   - Click **"Add Custom Domain"**
   - Enter: `www.ttgtrade.com`
3. Add DNS records at your registrar:

**CNAME Record:**
```
Name: www
Type: CNAME
Value: your-app-name.onrender.com
TTL: 3600
```

4. Wait for DNS propagation (~24 hours)
5. SSL certificate automatically provisioned

### Update Django Settings

Add to `ALLOWED_HOSTS`:
```python
ALLOWED_HOSTS = [
    'your-app-name.onrender.com',
    'www.ttgtrade.com',
    'ttgtrade.com',
]
```

---

## 📧 Email Configuration (Optional)

### Gmail SMTP

Add environment variables:
```
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

**Note**: Use App Password, not regular password
- Google Account → Security → App Passwords

### SendGrid (Recommended for production)

Free tier: 100 emails/day
```
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.sendgrid.net
EMAIL_PORT=587
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=your-sendgrid-api-key
```

---

## 💾 Data Persistence

### What Persists:
✅ PostgreSQL database
✅ User accounts
✅ Orders, products, insurance policies
✅ Avon Points balances
✅ All database data

### What Doesn't Persist:
❌ Uploaded files (media)
❌ Local filesystem changes

**Solution**: Use cloud storage (S3/Cloudinary) for uploads

---

## 🚦 Health Checks

Render automatically monitors:
- HTTP health checks every 30 seconds
- Restarts app if unresponsive
- Sends alerts on failures

Custom health check endpoint:
```python
# Add to core/views.py
from django.http import JsonResponse

def health_check(request):
    return JsonResponse({'status': 'healthy'})

# Add to core/urls.py
path('health/', views.health_check, name='health_check'),
```

---

## 📚 Useful Commands

### Local Development
```bash
# Run locally with production settings
export RENDER=true
python manage.py runserver

# Reset database locally
python manage.py flush
python manage.py migrate
python manage.py seed_data_updated
```

### Render Shell Access
Dashboard → Service → **Shell**
```bash
# Access Django shell
python manage.py shell

# Run management commands
python manage.py createsuperuser
python manage.py migrate
python manage.py collectstatic
```

---

## 🎓 Next Steps After Deployment

1. **Change Admin Password**
   ```
   /admin → Change password
   ```

2. **Configure Email** (for notifications)
   - Set up SendGrid or Gmail SMTP
   - Test with password reset

3. **Add Custom Domain**
   - Purchase domain
   - Configure DNS
   - Update ALLOWED_HOSTS

4. **Set Up Cloud Storage**
   - AWS S3 or Cloudinary
   - For user uploads (images, documents)

5. **Monitor Application**
   - Check logs regularly
   - Review error reports
   - Monitor database size

6. **Backup Strategy**
   - Enable automatic backups
   - Test restore process
   - Export important data periodically

---

## 📞 Support Resources

**Render Documentation:**
- https://render.com/docs

**Django Deployment:**
- https://docs.djangoproject.com/en/4.2/howto/deployment/

**Community:**
- Render Community Forum
- Django Discord Server

---

## ✅ Deployment Checklist

Pre-deployment:
- [ ] Code pushed to GitHub
- [ ] All tests passing
- [ ] Environment variables documented
- [ ] Static files configured

During deployment:
- [ ] PostgreSQL database created
- [ ] Environment variables set
- [ ] Build successful
- [ ] Migrations completed

Post-deployment:
- [ ] Admin panel accessible
- [ ] Admin password changed
- [ ] Test user registration
- [ ] Test product ordering
- [ ] Test Avon Points system
- [ ] Verify email functionality (if configured)
- [ ] Check all pages load correctly
- [ ] Test mobile responsiveness

---

**Deployment Status**: ✅ Ready for Render
**Estimated Setup Time**: 15-20 minutes
**Monthly Cost**: $0 (Free tier) or $7 (Starter plan)

🎉 **Your T&TG Trade Corp is ready for the world!**

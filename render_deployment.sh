#!/bin/bash

echo "================================================"
echo "  Preparing T&TG Trade Corp for Render Deploy"
echo "================================================"
echo ""

# 1. Create render.yaml
cat > render.yaml << 'YAML_EOF'
services:
  # Web Service
  - type: web
    name: ttg-trade-corp
    env: python
    region: oregon
    plan: free
    branch: main
    buildCommand: "./build.sh"
    startCommand: "gunicorn ttg_trade.wsgi:application"
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
      - key: DATABASE_URL
        fromDatabase:
          name: ttg-trade-db
          property: connectionString
      - key: SECRET_KEY
        generateValue: true
      - key: DJANGO_DEBUG
        value: False
      - key: ALLOWED_HOSTS
        sync: false
    
  # PostgreSQL Database
  - type: pgsql
    name: ttg-trade-db
    region: oregon
    plan: free
    databaseName: ttg_trade_db
    databaseUser: ttg_trade_user
YAML_EOF

# 2. Create build.sh
cat > build.sh << 'BUILD_EOF'
#!/usr/bin/env bash
# exit on error
set -o errexit

pip install --upgrade pip
pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

# Create superuser if it doesn't exist
python manage.py shell << SHELL_EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@ttgtrade.com', 'Admin2026!SecurePassword')
    print('Superuser created')
else:
    print('Superuser already exists')
SHELL_EOF

# Load initial data
python manage.py seed_data_updated
BUILD_EOF

chmod +x build.sh

# 3. Update requirements.txt for production
cat > requirements.txt << 'REQ_EOF'
# Core Django
Django==4.2.11
django-crispy-forms==2.1

# Database
psycopg2-binary==2.9.9
dj-database-url==2.1.0

# Web Server
gunicorn==21.2.0
whitenoise==6.6.0

# Environment
python-decouple==3.8

# Utilities
Pillow==10.2.0
REQ_EOF

# 4. Update settings.py for production
cat > ttg_trade/settings_production.py << 'SETTINGS_EOF'
"""
Production Settings for T&TG Trade Corp on Render
"""
import os
import dj_database_url
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Security Settings
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-change-me-in-production')
DEBUG = os.environ.get('DJANGO_DEBUG', 'False') == 'True'

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '*').split(',')
ALLOWED_HOSTS.append('.onrender.com')

# HTTPS Settings
SECURE_SSL_REDIRECT = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    
    # Apps
    'core.apps.CoreConfig',
    'ecommerce',
    'forex',
    'insurance',
    'coffee',
    'training',
    'notifications.apps.NotificationsConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Whitenoise for static files
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ttg_trade.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.site_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'ttg_trade.wsgi.application'

# Database - PostgreSQL on Render
DATABASES = {
    'default': dj_database_url.config(
        default='postgresql://postgres:postgres@localhost:5432/ttg_trade',
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/Toronto'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Whitenoise configuration for static files
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Auth URLs
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/'

# Session settings
SESSION_COOKIE_AGE = 60 * 60 * 24 * 14  # 2 weeks

# File upload settings
FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10MB

# Messages
from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.DEBUG: 'info',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'danger',
}

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
SETTINGS_EOF

# 5. Update main settings.py to use production settings
cat > ttg_trade/settings.py << 'MAIN_SETTINGS_EOF'
"""
T&TG Trade Corp — Django Settings
Auto-detects environment and loads appropriate settings
"""
import os

# Determine if we're on Render
IS_RENDER = os.environ.get('RENDER', False)

if IS_RENDER:
    # Use production settings on Render
    from .settings_production import *
else:
    # Use development settings locally
    from pathlib import Path
    
    BASE_DIR = Path(__file__).resolve().parent.parent
    
    SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-ttg-trade-corp-dev-key-2026')
    DEBUG = True
    ALLOWED_HOSTS = ['*']
    
    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'django.contrib.humanize',
        'core.apps.CoreConfig',
        'ecommerce',
        'forex',
        'insurance',
        'coffee',
        'training',
        'notifications.apps.NotificationsConfig',
    ]
    
    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]
    
    ROOT_URLCONF = 'ttg_trade.urls'
    
    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [BASE_DIR / 'templates'],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                    'core.context_processors.site_context',
                ],
            },
        },
    ]
    
    WSGI_APPLICATION = 'ttg_trade.wsgi.application'
    
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
    
    AUTH_PASSWORD_VALIDATORS = [
        {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
        {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
        {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
        {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
    ]
    
    LANGUAGE_CODE = 'en-us'
    TIME_ZONE = 'America/Toronto'
    USE_I18N = True
    USE_TZ = True
    
    STATIC_URL = '/static/'
    STATICFILES_DIRS = [BASE_DIR / 'static']
    STATIC_ROOT = BASE_DIR / 'staticfiles'
    MEDIA_URL = '/media/'
    MEDIA_ROOT = BASE_DIR / 'media'
    
    DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
    LOGIN_URL = '/accounts/login/'
    LOGIN_REDIRECT_URL = '/dashboard/'
    LOGOUT_REDIRECT_URL = '/'
    
    SESSION_COOKIE_AGE = 60 * 60 * 24 * 14
    FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024
    DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024
    
    from django.contrib.messages import constants as messages
    MESSAGE_TAGS = {
        messages.DEBUG: 'info',
        messages.INFO: 'info',
        messages.SUCCESS: 'success',
        messages.WARNING: 'warning',
        messages.ERROR: 'danger',
    }
MAIN_SETTINGS_EOF

# 6. Create .gitignore
cat > .gitignore << 'GIT_EOF'
# Python
*.py[cod]
__pycache__/
*.so
*.egg
*.egg-info/
dist/
build/

# Django
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal
/media
/staticfiles

# Environment
.env
.venv
env/
venv/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Backup files
*.backup
*_backup.*
GIT_EOF

# 7. Create .env.example
cat > .env.example << 'ENV_EOF'
# Production Environment Variables for Render

# Django Settings
SECRET_KEY=your-secret-key-here
DJANGO_DEBUG=False
ALLOWED_HOSTS=your-app-name.onrender.com,www.ttgtrade.com

# Database (automatically set by Render)
DATABASE_URL=postgresql://user:password@host:port/database

# Email (optional - configure for production notifications)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-email-password

# Security (for production)
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
ENV_EOF

# 8. Create runtime.txt for Python version
cat > runtime.txt << 'RUNTIME_EOF'
python-3.11.0
RUNTIME_EOF

echo ""
echo "✅ Render deployment files created!"
echo ""
echo "Files created:"
echo "  - render.yaml (Render configuration)"
echo "  - build.sh (Build script)"
echo "  - requirements.txt (Updated for production)"
echo "  - ttg_trade/settings.py (Auto-detects environment)"
echo "  - ttg_trade/settings_production.py (Production settings)"
echo "  - .gitignore (Git ignore rules)"
echo "  - .env.example (Environment variables template)"
echo "  - runtime.txt (Python version)"
echo ""

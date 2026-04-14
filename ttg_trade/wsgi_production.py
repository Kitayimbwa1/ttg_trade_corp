"""
WSGI config for T&TG Trade Corp production.
"""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ttg_trade.settings_production')

application = get_wsgi_application()

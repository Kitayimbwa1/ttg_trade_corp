#!/usr/bin/env python
"""
T&TG Trade Corp — Seed Data Script
Run: python seed.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ttg_trade.settings')
django.setup()

from ecommerce.models import Category
from forex.models import ExchangeRate
from training.models import TrainingProgram

# Categories
cats = [
    ('Agriculture & Food', 'agriculture-food', 'fa-seedling'),
    ('Electronics & Tech', 'electronics-tech', 'fa-microchip'),
    ('Textiles & Fashion', 'textiles-fashion', 'fa-tshirt'),
    ('Construction & Materials', 'construction-materials', 'fa-hard-hat'),
    ('Pharmaceuticals', 'pharmaceuticals', 'fa-pills'),
    ('Automotive & Parts', 'automotive-parts', 'fa-car'),
    ('Financial Instruments', 'financial-instruments', 'fa-chart-line'),
    ('Services & Consulting', 'services-consulting', 'fa-briefcase'),
]
for name, slug, icon in cats:
    Category.objects.get_or_create(slug=slug, defaults={'name': name, 'icon': icon})
print(f"✅ {len(cats)} categories seeded")

# Exchange rates (approximate 2026 rates)
rates = [
    ('USD', 'CAD', 1.36),
    ('USD', 'UGX', 3750.00),
    ('USD', 'KES', 130.00),
    ('USD', 'JPY', 149.50),
    ('USD', 'EUR', 0.92),
    ('CAD', 'USD', 0.735),
    ('CAD', 'UGX', 2757.00),
    ('EUR', 'USD', 1.087),
    ('EUR', 'UGX', 4076.00),
    ('GBP', 'USD', 1.27),
]
for fc, tc, r in rates:
    ExchangeRate.objects.update_or_create(
        from_currency=fc, to_currency=tc,
        defaults={'rate': r}
    )
print(f"✅ {len(rates)} exchange rates seeded")

# Training programs
programs = [
    {
        'title': 'Introduction to Modern & Precision Farming',
        'slug': 'intro-precision-farming',
        'category': 'farming',
        'description': 'Learn drone-assisted crop monitoring, soil sensor technology, and data-driven agricultural practices used across East Africa and beyond.',
        'duration_hours': 12,
        'certificate_fee_usd': 500,
    },
    {
        'title': 'Agri-Business & Export Marketing',
        'slug': 'agri-business-export',
        'category': 'farming',
        'description': 'From farm to global market — learn how to position and export agricultural products through T&TG international channels.',
        'duration_hours': 8,
        'certificate_fee_usd': 750,
    },
    {
        'title': 'Mid-Market Enterprise Management',
        'slug': 'enterprise-management',
        'category': 'enterprise',
        'description': 'Corporate strategy, operational leadership, cross-border team management, and mid-market enterprise growth frameworks.',
        'duration_hours': 20,
        'certificate_fee_usd': 2000,
    },
    {
        'title': 'International Trade & Import/Export',
        'slug': 'international-trade-import-export',
        'category': 'enterprise',
        'description': 'End-to-end guide to international trade: Incoterms, customs documentation, partner negotiation, and logistics across T&TG corridors.',
        'duration_hours': 15,
        'certificate_fee_usd': 1500,
    },
    {
        'title': 'Foreign Exchange & Currency Management',
        'slug': 'forex-currency-management',
        'category': 'finance',
        'description': 'Multi-currency trading, hedging strategies, forex risk management, and cross-border payment system fundamentals.',
        'duration_hours': 10,
        'certificate_fee_usd': 1000,
    },
    {
        'title': 'Investment Strategy & Portfolio Management',
        'slug': 'investment-strategy-portfolio',
        'category': 'finance',
        'description': 'Equity, fixed income, alternative assets, and portfolio construction strategies applicable to emerging market investments.',
        'duration_hours': 18,
        'certificate_fee_usd': 5000,
    },
]
for p in programs:
    TrainingProgram.objects.get_or_create(slug=p['slug'], defaults=p)
print(f"✅ {len(programs)} training programs seeded")

print("\n🎉 Seed complete. Run: python manage.py runserver")

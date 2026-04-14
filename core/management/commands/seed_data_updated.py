"""
T&TG Trade Corp - Enhanced Seed Data with Avon Points, Insurance, Coffee
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils.text import slugify
from decimal import Decimal
import datetime

from ecommerce.models import (Category, PartnerCompany, Product, AvonPointsAccount, 
                              AvonPointsTransaction, Order)
from insurance.models import InsuranceProduct, InsurancePolicy
from coffee.models import CoffeeProduct, ProductionLevel
from forex.models import CurrencyPair
from training.models import Course
from notifications.models import Notification


class Command(BaseCommand):
    help = 'Seed database with sample data including new features'

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting comprehensive data seeding...')
        
        # Create users
        self.create_users()
        
        # Create partner companies
        self.create_partner_companies()
        
        # Create e-commerce data
        self.create_ecommerce_data()
        
        # Create Avon Points accounts
        self.create_avon_accounts()
        
        # Create insurance products
        self.create_insurance_products()
        
        # Create coffee products and production levels
        self.create_coffee_data()
        
        # Create forex pairs
        self.create_forex_data()
        
        # Create training courses
        self.create_training_data()
        
        self.stdout.write(self.style.SUCCESS('✓ All data seeded successfully!'))

    def create_users(self):
        self.stdout.write('Creating users...')
        
        # Admin user
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@ttgtrade.com',
                password='admin123',
                first_name='Admin',
                last_name='User'
            )
        
        # Leadership
        users_data = [
            {'username': 'tom', 'email': 'tom@ttgtrade.com', 'first_name': 'Tom', 
             'last_name': 'Ssembiito', 'password': 'demo123'},
            {'username': 'edgar', 'email': 'edgar@ttgtrade.com', 'first_name': 'Kitayimbwa', 
             'last_name': 'Edgar', 'password': 'demo123'},
            {'username': 'michael', 'email': 'michael@ttgtrade.com', 'first_name': 'Kumagum', 
             'last_name': 'Michael', 'password': 'demo123'},
            {'username': 'francis', 'email': 'francis@ttgtrade.com', 'first_name': 'Musana', 
             'last_name': 'Francis', 'password': 'demo123'},
            # Regular users
            {'username': 'buyer1', 'email': 'buyer1@example.com', 'first_name': 'John', 
             'last_name': 'Doe', 'password': 'demo123'},
            {'username': 'buyer2', 'email': 'buyer2@example.com', 'first_name': 'Jane', 
             'last_name': 'Smith', 'password': 'demo123'},
        ]
        
        for user_data in users_data:
            if not User.objects.filter(username=user_data['username']).exists():
                User.objects.create_user(**user_data)
        
        self.stdout.write('  ✓ Users created')

    def create_partner_companies(self):
        self.stdout.write('Creating partner companies...')
        
        companies = [
            {
                'name': 'Uganda Tech Solutions Ltd',
                'unique_id': 'PARTNER001',
                'country': 'UG',
                'contact_person': 'Samuel Okello',
                'email': 'info@ugangatech.com',
                'phone': '+256700123456',
            },
            {
                'name': 'Kenya Export Partners',
                'unique_id': 'PARTNER002',
                'country': 'KE',
                'contact_person': 'Mary Wanjiku',
                'email': 'contact@kenyaexport.co.ke',
                'phone': '+254722334455',
            },
            {
                'name': 'Netherlands Trade BV',
                'unique_id': 'PARTNER003',
                'country': 'NL',
                'contact_person': 'Jan de Vries',
                'email': 'info@nltrade.nl',
                'phone': '+31206543210',
            },
        ]
        
        for comp_data in companies:
            PartnerCompany.objects.get_or_create(
                unique_id=comp_data['unique_id'],
                defaults=comp_data
            )
        
        self.stdout.write('  ✓ Partner companies created')

    def create_ecommerce_data(self):
        self.stdout.write('Creating e-commerce data...')
        
        # Categories
        categories = [
            {'name': 'Electronics', 'icon': 'fa-laptop'},
            {'name': 'Office Equipment', 'icon': 'fa-print'},
            {'name': 'Pharmaceuticals', 'icon': 'fa-pills'},
            {'name': 'Green Coffee', 'icon': 'fa-seedling'},
            {'name': 'Roasted Coffee', 'icon': 'fa-coffee'},
        ]
        
        for cat_data in categories:
            Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'slug': slugify(cat_data['name']), 'icon': cat_data['icon']}
            )
        
        # Products
        seller = User.objects.get(username='edgar')
        electronics_cat = Category.objects.get(name='Electronics')
        office_cat = Category.objects.get(name='Office Equipment')
        
        products = [
            {
                'seller': seller,
                'category': electronics_cat,
                'title': 'Apple MacBook Pro 16"',
                'slug': 'apple-macbook-pro-16',
                'description': 'Latest M3 chip, 32GB RAM, 1TB SSD. Perfect for professionals.',
                'price': Decimal('2499.00'),
                'country': 'CA',
                'market_type': 'both',
                'stock_quantity': 15,
            },
            {
                'seller': seller,
                'category': office_cat,
                'title': 'HP LaserJet Enterprise Printer',
                'slug': 'hp-laserjet-enterprise',
                'description': 'High-volume commercial printer with duplex printing.',
                'price': Decimal('899.00'),
                'country': 'US',
                'market_type': 'international',
                'stock_quantity': 25,
            },
        ]
        
        for prod_data in products:
            Product.objects.get_or_create(
                slug=prod_data['slug'],
                defaults=prod_data
            )
        
        self.stdout.write('  ✓ E-commerce data created')

    def create_avon_accounts(self):
        self.stdout.write('Creating Avon Points accounts...')
        
        for user in User.objects.filter(is_superuser=False):
            account, created = AvonPointsAccount.objects.get_or_create(user=user)
            
            if created:
                # Give some initial points for demo
                initial_points = Decimal('500.00')
                account.available_points = initial_points
                account.total_earned_points = initial_points
                account.save()
                
                # Create initial transaction
                AvonPointsTransaction.objects.create(
                    account=account,
                    transaction_type='earn',
                    amount=initial_points,
                    source='Welcome bonus',
                    balance_after=initial_points
                )
        
        self.stdout.write('  ✓ Avon Points accounts created')

    def create_insurance_products(self):
        self.stdout.write('Creating insurance products...')
        
        insurance_products = [
            {
                'name': 'Comprehensive Life Insurance',
                'product_type': 'life',
                'description': 'Complete life coverage for you and your family.',
                'coverage_details': 'Death benefit, critical illness, disability coverage.',
                'min_premium': Decimal('50.00'),
                'max_premium': Decimal('500.00'),
                'available_countries': 'CA,UG,US,KE',
            },
            {
                'name': 'Small Business Protection',
                'product_type': 'business',
                'description': 'Protect your business assets and operations.',
                'coverage_details': 'Property damage, liability, business interruption.',
                'min_premium': Decimal('100.00'),
                'max_premium': Decimal('1000.00'),
                'available_countries': 'CA,UG,US,NL,KE',
            },
            {
                'name': 'Travel Insurance Plus',
                'product_type': 'travel',
                'description': 'Comprehensive travel protection worldwide.',
                'coverage_details': 'Medical emergencies, trip cancellation, lost luggage.',
                'min_premium': Decimal('25.00'),
                'max_premium': Decimal('200.00'),
                'available_countries': 'CA,US,NL,KE',
            },
        ]
        
        for ins_data in insurance_products:
            InsuranceProduct.objects.get_or_create(
                name=ins_data['name'],
                defaults=ins_data
            )
        
        self.stdout.write('  ✓ Insurance products created')

    def create_coffee_data(self):
        self.stdout.write('Creating coffee products and production levels...')
        
        # Production levels
        levels_data = [
            {
                'name': 'Starter',
                'level_number': 1,
                'kg_per_week': Decimal('25'),
                'monthly_revenue_min': Decimal('875'),
                'monthly_revenue_max': Decimal('1375'),
                'annual_revenue_min': Decimal('10500'),
                'annual_revenue_max': Decimal('16500'),
                'is_current': True,
            },
            {
                'name': 'Growth',
                'level_number': 2,
                'kg_per_week': Decimal('50'),
                'monthly_revenue_min': Decimal('1750'),
                'monthly_revenue_max': Decimal('2750'),
                'annual_revenue_min': Decimal('21000'),
                'annual_revenue_max': Decimal('33000'),
                'is_current': False,
            },
            {
                'name': 'Established',
                'level_number': 3,
                'kg_per_week': Decimal('75'),
                'monthly_revenue_min': Decimal('2625'),
                'monthly_revenue_max': Decimal('4125'),
                'annual_revenue_min': Decimal('31500'),
                'annual_revenue_max': Decimal('49500'),
                'is_current': False,
            },
            {
                'name': 'Enterprise',
                'level_number': 4,
                'kg_per_week': Decimal('100'),
                'monthly_revenue_min': Decimal('14000'),
                'monthly_revenue_max': Decimal('22000'),
                'annual_revenue_min': Decimal('168000'),
                'annual_revenue_max': Decimal('264000'),
                'is_current': False,
            },
        ]
        
        for level_data in levels_data:
            ProductionLevel.objects.get_or_create(
                level_number=level_data['level_number'],
                defaults=level_data
            )
        
        # Coffee products
        coffee_products = [
            {
                'name': 'Premium Arabica - Light Roast',
                'coffee_type': 'arabica',
                'roast_level': 'light',
                'description': 'Delicate flavor with floral notes and bright acidity.',
                'price_per_kg': Decimal('45.00'),
                'min_price': Decimal('35.00'),
                'max_price': Decimal('55.00'),
                'texture_notes': 'Smooth, bright, with hints of citrus and jasmine.',
                'stock_kg': Decimal('150.00'),
            },
            {
                'name': 'Organic Arabica - Medium Roast',
                'coffee_type': 'arabica',
                'roast_level': 'medium',
                'description': 'Balanced flavor with chocolate and caramel notes.',
                'price_per_kg': Decimal('42.00'),
                'min_price': Decimal('35.00'),
                'max_price': Decimal('55.00'),
                'texture_notes': 'Rich, balanced, with chocolate and nutty undertones.',
                'stock_kg': Decimal('200.00'),
            },
            {
                'name': 'Bold Arabica - Dark Roast',
                'coffee_type': 'arabica',
                'roast_level': 'dark',
                'description': 'Strong, full-bodied with smoky finish.',
                'price_per_kg': Decimal('40.00'),
                'min_price': Decimal('35.00'),
                'max_price': Decimal('55.00'),
                'texture_notes': 'Bold, smoky, with deep cocoa notes.',
                'stock_kg': Decimal('180.00'),
            },
        ]
        
        for coffee_data in coffee_products:
            CoffeeProduct.objects.get_or_create(
                name=coffee_data['name'],
                defaults=coffee_data
            )
        
        self.stdout.write('  ✓ Coffee data created')

    def create_forex_data(self):
        self.stdout.write('Creating forex currency pairs...')
        
        pairs = [
            {'base': 'USD', 'quote': 'CAD', 'rate': '1.3650'},
            {'base': 'USD', 'quote': 'UGX', 'rate': '3750.00'},
            {'base': 'EUR', 'quote': 'USD', 'rate': '1.0850'},
            {'base': 'GBP', 'quote': 'USD', 'rate': '1.2650'},
        ]
        
        for pair_data in pairs:
            CurrencyPair.objects.get_or_create(
                base_currency=pair_data['base'],
                quote_currency=pair_data['quote'],
                defaults={'current_rate': Decimal(pair_data['rate'])}
            )
        
        self.stdout.write('  ✓ Forex data created')

    def create_training_data(self):
        self.stdout.write('Creating training courses...')
        
        instructor = User.objects.get(username='michael')
        
        courses = [
            {
                'title': 'Import/Export Business Fundamentals',
                'slug': 'import-export-fundamentals',
                'instructor': instructor,
                'description': 'Learn the basics of international trade.',
                'price': Decimal('299.00'),
                'duration_hours': 20,
                'level': 'beginner',
            },
            {
                'title': 'Forex Trading Masterclass',
                'slug': 'forex-trading-masterclass',
                'instructor': instructor,
                'description': 'Master currency trading strategies.',
                'price': Decimal('499.00'),
                'duration_hours': 40,
                'level': 'intermediate',
            },
        ]
        
        for course_data in courses:
            Course.objects.get_or_create(
                slug=course_data['slug'],
                defaults=course_data
            )
        
        self.stdout.write('  ✓ Training courses created')

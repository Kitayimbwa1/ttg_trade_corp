"""
Management command: python manage.py seed_data

Seeds the database with:
  - Product categories
  - Exchange rates
  - Training programs
  - A demo superuser (admin / admin1234)
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Seed T&TG Trade Corp with initial data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--flush', action='store_true',
            help='Clear existing seed data before seeding'
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING('\n🌱  T&TG Trade Corp — Seeding database...\n'))

        if options['flush']:
            self._flush()

        self._seed_categories()
        self._seed_rates()
        self._seed_programs()
        self._seed_superuser()

        self.stdout.write(self.style.SUCCESS('\n✅  Seeding complete!\n'))
        self.stdout.write('    Run: python manage.py runserver\n')
        self.stdout.write('    Admin: http://127.0.0.1:8000/admin/\n')
        self.stdout.write('    Login: admin / admin1234\n\n')

    # ── FLUSH ────────────────────────────────────────────────────────────────
    def _flush(self):
        from ecommerce.models import Category
        from forex.models import ExchangeRate
        from training.models import TrainingProgram
        Category.objects.all().delete()
        ExchangeRate.objects.all().delete()
        TrainingProgram.objects.all().delete()
        self.stdout.write('  Flushed existing seed data.')

    # ── CATEGORIES ───────────────────────────────────────────────────────────
    def _seed_categories(self):
        from ecommerce.models import Category
        cats = [
            ('Agriculture & Food',         'agriculture-food',       'fa-seedling'),
            ('Electronics & Technology',   'electronics-tech',       'fa-microchip'),
            ('Textiles & Fashion',         'textiles-fashion',       'fa-tshirt'),
            ('Construction & Materials',   'construction-materials', 'fa-hard-hat'),
            ('Pharmaceuticals & Health',   'pharmaceuticals',        'fa-pills'),
            ('Automotive & Parts',         'automotive-parts',       'fa-car'),
            ('Financial Instruments',      'financial-instruments',  'fa-chart-line'),
            ('Services & Consulting',      'services-consulting',    'fa-briefcase'),
            ('Beverages & FMCG',           'beverages-fmcg',         'fa-box'),
            ('Energy & Utilities',         'energy-utilities',       'fa-bolt'),
        ]
        created = 0
        for name, slug, icon in cats:
            _, was_created = Category.objects.get_or_create(
                slug=slug, defaults={'name': name, 'icon': icon}
            )
            if was_created:
                created += 1
        self.stdout.write(f'  Categories: {created} created, {len(cats) - created} already exist.')

    # ── EXCHANGE RATES ────────────────────────────────────────────────────────
    def _seed_rates(self):
        from forex.models import ExchangeRate
        rates = [
            # USD pairs
            ('USD', 'CAD',  1.360),
            ('USD', 'UGX',  3750.000),
            ('USD', 'KES',  130.000),
            ('USD', 'JPY',  149.500),
            ('USD', 'EUR',  0.920),
            ('USD', 'GBP',  0.790),
            # CAD pairs
            ('CAD', 'USD',  0.735),
            ('CAD', 'UGX',  2757.000),
            ('CAD', 'KES',  95.590),
            ('CAD', 'EUR',  0.676),
            # EUR pairs
            ('EUR', 'USD',  1.087),
            ('EUR', 'UGX',  4076.000),
            ('EUR', 'KES',  141.300),
            # GBP pairs
            ('GBP', 'USD',  1.265),
            ('GBP', 'UGX',  4743.000),
            # KES / UGX cross
            ('KES', 'UGX',  28.850),
            ('UGX', 'KES',  0.0347),
            # JPY
            ('JPY', 'USD',  0.00669),
            ('JPY', 'CAD',  0.00910),
        ]
        updated = 0
        for fc, tc, r in rates:
            _, created = ExchangeRate.objects.update_or_create(
                from_currency=fc, to_currency=tc,
                defaults={'rate': r}
            )
            updated += 1
        self.stdout.write(f'  Exchange rates: {updated} set.')

    # ── TRAINING PROGRAMS ─────────────────────────────────────────────────────
    def _seed_programs(self):
        from training.models import TrainingProgram
        programs = [
            # ── FARMING ──
            dict(
                title='Introduction to Precision & Tech Farming',
                slug='intro-precision-farming',
                category='farming',
                description=(
                    'Master drone-assisted crop monitoring, IoT soil sensors, satellite imagery '
                    'analysis, and data-driven yield optimisation. Designed for farmers and '
                    'agri-entrepreneurs across East Africa and the global T&TG network.'
                ),
                duration_hours=12,
                certificate_fee_usd=500,
            ),
            dict(
                title='Agri-Business & Export Marketing',
                slug='agri-business-export',
                category='farming',
                description=(
                    'From farm gate to global market — learn how to position, certify, and '
                    'export agricultural commodities through T&TG international trade channels. '
                    'Covers branding, logistics, phytosanitary compliance, and buyer negotiation.'
                ),
                duration_hours=8,
                certificate_fee_usd=750,
            ),
            dict(
                title='Climate-Smart Agriculture',
                slug='climate-smart-agriculture',
                category='farming',
                description=(
                    'Sustainable farming in the face of climate change. Covers water-efficient '
                    'irrigation, carbon sequestration, resilient crop varieties, and accessing '
                    'climate finance for smallholder farmers in Uganda and Kenya.'
                ),
                duration_hours=10,
                certificate_fee_usd=600,
            ),
            # ── ENTERPRISE ──
            dict(
                title='Mid-Market Enterprise Management',
                slug='enterprise-management',
                category='enterprise',
                description=(
                    'Corporate strategy, operational leadership, cross-border team management, '
                    'and mid-market enterprise growth frameworks. A comprehensive programme for '
                    'managers and directors ready to scale their businesses internationally.'
                ),
                duration_hours=20,
                certificate_fee_usd=2000,
            ),
            dict(
                title='International Trade & Import/Export Operations',
                slug='international-trade-import-export',
                category='enterprise',
                description=(
                    'End-to-end guide to international trade: Incoterms 2020, customs '
                    'documentation, HS codes, partner negotiation, and logistics coordination '
                    'across T&TG corridors — Canada, Uganda, Netherlands, Japan, Kenya.'
                ),
                duration_hours=15,
                certificate_fee_usd=1500,
            ),
            dict(
                title='Digital Marketing for Global Trade',
                slug='digital-marketing-global-trade',
                category='enterprise',
                description=(
                    'Build a digital presence and customer acquisition engine for B2B and '
                    'B2C trade. Covers SEO, social media, e-commerce storefronts, and '
                    'cross-border digital advertising strategies.'
                ),
                duration_hours=8,
                certificate_fee_usd=800,
            ),
            # ── FINANCE ──
            dict(
                title='Foreign Exchange & Currency Risk Management',
                slug='forex-currency-management',
                category='finance',
                description=(
                    'Multi-currency trading, hedging strategies, forward contracts, and forex '
                    'risk management fundamentals. Practical module covering USD, CAD, UGX, '
                    'KES, EUR, and JPY cross-rate management for business transactions.'
                ),
                duration_hours=10,
                certificate_fee_usd=1000,
            ),
            dict(
                title='Investment Strategy & Portfolio Management',
                slug='investment-strategy-portfolio',
                category='finance',
                description=(
                    'Equity, fixed income, alternative assets, and portfolio construction '
                    'strategies applicable to emerging market and developed-market investments. '
                    'The flagship T&TG finance programme. Graduates eligible for secondary '
                    'shareholding in the corporation.'
                ),
                duration_hours=18,
                certificate_fee_usd=5000,
            ),
            dict(
                title='Financial Inclusion & Mobile Money',
                slug='financial-inclusion-mobile-money',
                category='finance',
                description=(
                    'Understanding Africa\'s mobile money ecosystem — MTN MoMo, M-Pesa, '
                    'Airtel Money, and Orange Money. Covers fintech integration, cross-border '
                    'remittances, and leveraging mobile finance for trade and investment.'
                ),
                duration_hours=6,
                certificate_fee_usd=500,
            ),
        ]
        created = 0
        for p in programs:
            _, was_created = TrainingProgram.objects.get_or_create(slug=p['slug'], defaults=p)
            if was_created:
                created += 1
        self.stdout.write(f'  Training programs: {created} created, {len(programs) - created} already exist.')

    # ── SUPERUSER ─────────────────────────────────────────────────────────────
    def _seed_superuser(self):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@ttgtrade.ca',
                password='admin1234',
                first_name='T&TG',
                last_name='Admin',
            )
            self.stdout.write('  Superuser created: admin / admin1234')
        else:
            self.stdout.write('  Superuser "admin" already exists.')

# T&TG Trade Corp — Django Web Application

**Tom & The Group Trade Corp** · Toronto, ON, Canada · Founded October 14, 2026

---

## Quick Setup (5 Steps)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run migrations
python manage.py makemigrations
python manage.py migrate

# 3. Seed all data (categories, rates, programs, admin user)
python manage.py seed_data

# 4. Collect static files
python manage.py collectstatic --noinput

# 5. Start the server
python manage.py runserver
```

**Visit:** http://127.0.0.1:8000  
**Admin:** http://127.0.0.1:8000/admin  
**Login:** `admin` / `admin1234`

---

## Project Structure

```
ttg_trade/
├── ttg_trade/               # Project config
│   ├── settings.py          # All Django settings
│   ├── urls.py              # Root URL routing
│   ├── wsgi.py
│   └── admin_site.py        # Branded admin site
│
├── core/                    # Main app
│   ├── models.py            # TraderProfile, ContactMessage
│   ├── views.py             # Home, About, Register, Dashboard, Profile, TV, Invest
│   ├── forms.py             # Registration, Contact, Profile update
│   ├── signals.py           # Auto-notifications on key events
│   ├── context_processors.py# Site-wide template variables
│   └── management/commands/
│       └── seed_data.py     # python manage.py seed_data
│
├── ecommerce/               # Trading portal
│   ├── models.py            # Category, Product, RFQ, Order
│   ├── views.py             # Marketplace, Product detail, Orders, RFQ
│   └── forms.py
│
├── forex/                   # Foreign exchange
│   ├── models.py            # ExchangeRate, ForexTransaction
│   ├── views.py             # Forex home, Exchange, History
│   └── forms.py
│
├── training/                # Online programs
│   ├── models.py            # TrainingProgram, Subscription
│   └── views.py             # Programs list, Detail, Subscribe, My Programs
│
├── notifications/           # User notifications
│   ├── models.py            # Notification (with .send() helper)
│   ├── views.py             # List, Mark read, Unread count API
│   └── apps.py              # Uses label 'site_notifications'
│
├── templates/
│   ├── base.html            # Master layout (navbar, footer, notifications bell)
│   ├── core/
│   │   ├── home.html        # Homepage with hero, ticker, countries, services
│   │   ├── about.html       # About, leadership, mission
│   │   ├── services.html    # Four business lines
│   │   ├── operations.html  # Global offices, portal architecture
│   │   ├── tv_program.html  # TV program & media, subscribe plans
│   │   ├── invest.html      # Investment & partnership tiers
│   │   ├── contact.html     # Contact form
│   │   ├── register.html    # KYC trader registration
│   │   ├── dashboard.html   # User dashboard
│   │   ├── profile.html     # Public trader profile
│   │   └── edit_profile.html
│   ├── ecommerce/           # Marketplace, product, orders, RFQ
│   ├── forex/               # Forex home, exchange, history
│   ├── training/            # Programs, detail, my programs
│   ├── notifications/       # Notification inbox
│   ├── registration/        # Login
│   └── errors/              # 404, 500
│
├── static/
│   ├── css/main.css         # Full design system (400 lines)
│   └── js/main.js           # Navbar, animations, form helpers, clipboard
│
├── manage.py
├── requirements.txt
├── seed.py                  # Legacy seeder (use manage.py seed_data instead)
├── .env.example
├── .gitignore
└── README.md
```

---

## Pages & URLs

| URL | Page |
|-----|------|
| `/` | Homepage |
| `/about/` | About T&TG Trade Corp |
| `/services/` | Four business lines |
| `/operations/` | Global offices & platform architecture |
| `/tv/` | TV Program & Media |
| `/invest/` | Investment & partnership |
| `/contact/` | Contact form |
| `/register/` | Trader registration (KYC) |
| `/dashboard/` | User dashboard |
| `/profile/<slug>/` | Public trader profile |
| `/trade/` | Marketplace |
| `/trade/product/<slug>/` | Product detail |
| `/trade/product/new/` | List a product |
| `/trade/rfq/new/` | Submit RFQ |
| `/trade/orders/` | My orders |
| `/forex/` | Forex home & rates |
| `/forex/exchange/` | Currency exchange |
| `/forex/history/` | Transaction history |
| `/training/` | Training programs |
| `/training/program/<slug>/` | Program detail |
| `/training/my-programs/` | My enrolled programs |
| `/notifications/` | Notification inbox |
| `/accounts/login/` | Sign in |
| `/admin/` | Django admin |

---

## Key Features

### Trading Portal
- **Local Market**: Country-specific — Canada, Uganda, Netherlands, Japan, Kenya
- **International Market**: For certified traders with Certificate of Completion
- Product listings with images, categories, currencies, stock management
- RFQ (Request for Quotation) system
- Order management with Mobile Money / E-Transfer / Bank Transfer

### Trader Registration & KYC
- 4-section registration: personal info → market type → business description → identity verification
- National ID upload (front & back), selfie, signed declaration
- Admin approval workflow: Pending → Approved / Rejected
- Auto-notifications on status change
- Shareable profile pages at `/profile/<slug>/`

### Notifications
- Bell icon in navbar with unread badge (polls every 60s via JS)
- Auto-triggered on: registration update, order placed/updated, forex transaction, training enrollment, certificate issued
- `Notification.send(user, title, message)` helper for programmatic use

### Forex Bureau
- Admin-managed exchange rates (19 pre-seeded pairs)
- Currencies: USD, CAD, UGX, KES, EUR, JPY, GBP
- Unique reference numbers per transaction
- Payment via Mobile Money, E-Transfer, Bank Transfer

### Training & Certification
- 3 tracks: Modern Farming, Enterprise Management, Financial Services
- 9 programs pre-seeded with `manage.py seed_data`
- Free to watch, paid Certificate of Completion ($500–$5,000)
- Certificate benefits: priority employment, international market access, secondary shareholding

### TV Program & Media
- 3 broadcast tracks matching training programmes
- 6 sample episodes with thumbnails
- Advertising slot showcase
- 4-tier subscription plan display

---

## Design System

| Token | Value |
|-------|-------|
| Primary Dark | `#0a0f1e` (Deep Navy) |
| Accent | `#c9a84c` (Corporate Gold) |
| Text Muted | `#8a9ab5` |
| Heading Font | Cormorant Garamond |
| Body Font | DM Sans |
| Card Background | `rgba(26,37,64,0.75)` with blur |

Global styles in `static/css/main.css`. Per-page overrides in `{% block extra_css %}`.

---

## Corporation Details

| Field | Value |
|-------|-------|
| Full Name | Tom & The Group Trade Corp |
| Founded | October 14, 2026 |
| HQ | M1G 1L8, Toronto, ON, Canada |
| Phone | +1 (416) 832 3512 |
| Email | tom.grouptradecorp.ca |
| Founder & Ops Manager | Tom Ssembiito |
| Shareholder & Software Engineer | Edgar Kitayimbwa |
| Shareholder | Musana Francis |
| Operations | Canada · Uganda · Netherlands · USA · Japan · Kenya |

---

## Production Deployment Checklist

- [ ] Set `DJANGO_SECRET_KEY` environment variable
- [ ] Set `DJANGO_DEBUG=False`
- [ ] Set `ALLOWED_HOSTS` to your domain
- [ ] Switch to PostgreSQL (uncomment in settings.py)
- [ ] Run `python manage.py collectstatic`
- [ ] Configure Nginx + Gunicorn
- [ ] Install SSL certificate (Let's Encrypt)
- [ ] Uncomment HTTPS security headers in settings.py
- [ ] Set up S3 or similar for media file storage
- [ ] Configure email backend for notifications


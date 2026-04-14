#!/bin/bash

echo "================================================"
echo "  T&TG Trade Corporation - Complete Setup"
echo "  Enhanced with Avon Points, Insurance & Coffee"
echo "================================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

echo "Activating virtual environment..."
source venv/Scripts/activate 2>/dev/null || source venv/bin/activate

echo "Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

echo ""
echo "Creating migrations..."
python manage.py makemigrations ecommerce
python manage.py makemigrations insurance
python manage.py makemigrations coffee
python manage.py makemigrations

echo ""
echo "Applying migrations..."
python manage.py migrate

echo ""
echo "Loading seed data..."
python manage.py seed_data_updated

echo ""
echo "Collecting static files..."
python manage.py collectstatic --noinput

echo ""
echo "================================================"
echo "  Setup Complete!"
echo "================================================"
echo ""
echo "Default Users Created:"
echo "  Admin: admin / admin123"
echo "  Leadership: tom, edgar, michael, francis / demo123"
echo "  Buyers: buyer1, buyer2 / demo123"
echo ""
echo "Features Enabled:"
echo "  ✓ Avon Points System (5.5% end user, 8.5% referral)"
echo "  ✓ Insurance Module"
echo "  ✓ Coffee Roasting Business"
echo "  ✓ Partner Company System"
echo "  ✓ Enhanced Order Flow with Delivery Options"
echo ""
echo "To start the development server:"
echo "  python manage.py runserver"
echo ""
echo "Then visit: http://127.0.0.1:8000"
echo "Admin panel: http://127.0.0.1:8000/admin"
echo ""

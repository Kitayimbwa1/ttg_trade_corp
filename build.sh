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

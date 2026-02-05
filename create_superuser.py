"""
Script to create superuser for MFU Portal
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from apps.core.models import User

# Create superuser
email = 'admin@mfu.com'
password = 'admin123'
first_name = 'Admin'
last_name = 'User'

if not User.objects.filter(email=email).exists():
    user = User.objects.create_superuser(
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name
    )
    print(f'Superuser created successfully!')
    print(f'Email: {email}')
    print(f'Password: {password}')
else:
    print(f'Superuser with email {email} already exists.')

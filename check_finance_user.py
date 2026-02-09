import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from apps.core.models import User

u = User.objects.get(email='finance@mfu.com')
print(f'User: {u.email}')
print(f'Active: {u.is_active}')
print(f'Email Confirmed: {u.email_confirmed}')
roles = u.roles.all()
print(f'Total Roles: {roles.count()}')
for role in roles:
    print(f'  - {role.code} (active: {role.is_active})')

active_roles = u.roles.filter(is_active=True)
print(f'Active Roles: {list(active_roles.values_list("code", flat=True))}')

#!/usr/bin/env python
import os
import sys
import pathlib
import django

# Ensure project root on sys.path
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.development")
django.setup()

from apps.core.models import User, Role, UserRole
from apps.coach_portal.models import CoachProfile

EMAIL = 'coach1@gmail.com'
ROLE_CODE = 'coach'
PASSWORD = 'ChangeMe123!'
FIRST_NAME = 'Coach'
LAST_NAME = 'One'


def main():
    # Ensure role exists
    role, role_created = Role.objects.get_or_create(
        code=ROLE_CODE,
        defaults={
            'name': 'Coach',
            'description': 'Coach role',
            'dashboard_url': '/coach-portal/dashboard/',
            'dashboard_icon': 'bi-person-badge',
        }
    )
    if role_created:
        print('Created Role: coach')
    else:
        print('Role exists: coach')

    # Create user if missing
    u = User.objects.filter(email__iexact=EMAIL).first()
    if not u:
        u = User.objects.create_user(email=EMAIL, password=PASSWORD, first_name=FIRST_NAME, last_name=LAST_NAME)
        print(f'Created user {EMAIL} with password "{PASSWORD}"')
    else:
        print(f'User exists: {EMAIL}')

    # Ensure user active and email confirmed
    changed = False
    if not u.is_active:
        u.is_active = True
        changed = True
    if not getattr(u, 'email_confirmed', False):
        setattr(u, 'email_confirmed', True)
        changed = True
    if changed:
        u.save()
        print('Activated user and marked email confirmed')
    else:
        print('User already active and email confirmed')

    # Assign role
    ur, created = UserRole.objects.get_or_create(user=u, role=role, defaults={'assigned_by': None})
    print('UserRole created' if created else 'UserRole already exists')

    # Ensure CoachProfile
    cp, cp_created = CoachProfile.objects.get_or_create(user=u)
    print('CoachProfile created' if cp_created else 'CoachProfile already exists')

    print('Done. Login with:', EMAIL, 'password:', PASSWORD)


if __name__ == '__main__':
    main()

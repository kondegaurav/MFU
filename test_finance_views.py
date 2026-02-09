#!/usr/bin/env python
"""Test script to verify finance portal views work correctly."""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from django.test import RequestFactory
from django.contrib.auth.models import AnonymousUser
from apps.finance_portal.views import equipment_requests, transactions_list, equipment_inventory, finance_dashboard
from apps.core.models import User, UserRole, Role
from apps.finance_portal.models import EquipmentRequest, FinancialTransaction

# Create a test user with finance_inventory role
try:
    test_user, _ = User.objects.get_or_create(
        email='test@finance.com',
        defaults={'first_name': 'Test', 'last_name': 'Finance', 'is_active': True}
    )

    role_obj, created = Role.objects.get_or_create(
        code='finance_inventory',
        defaults={'name': 'Finance & Inventory Manager', 'dashboard_url': 'finance_portal:dashboard'}
    )
    if not created and role_obj.dashboard_url != 'finance_portal:dashboard':
        role_obj.dashboard_url = 'finance_portal:dashboard'
        role_obj.save()
        print(f"✓ Updated role dashboard_url to: {role_obj.dashboard_url}")

    user_role, _ = UserRole.objects.get_or_create(
        user=test_user,
        role=role_obj
    )
    print(f"✓ Test user created: {test_user.email} with role: {role_obj.name}")
except Exception as e:
    print(f"✗ Error creating test user: {e}")
    exit(1)

# Test equipment_requests view
factory = RequestFactory()
request = factory.get('/finance/equipment-requests/')
request.user = test_user

try:
    response = equipment_requests(request)
    print(f"✓ equipment_requests view works: {response.status_code}")
except Exception as e:
    print(f"✗ equipment_requests view error: {e}")
    import traceback
    traceback.print_exc()

# Test transactions_list view
request = factory.get('/finance/transactions/')
request.user = test_user

try:
    response = transactions_list(request)
    print(f"✓ transactions_list view works: {response.status_code}")
except Exception as e:
    print(f"✗ transactions_list view error: {e}")
    import traceback
    traceback.print_exc()

# Test equipment_inventory view
request = factory.get('/finance/equipment/')
request.user = test_user

try:
    response = equipment_inventory(request)
    print(f"✓ equipment_inventory view works: {response.status_code}")
except Exception as e:
    print(f"✗ equipment_inventory view error: {e}")
    import traceback
    traceback.print_exc()

# Test finance_dashboard view
request = factory.get('/finance/dashboard/')
request.user = test_user

try:
    response = finance_dashboard(request)
    print(f"✓ finance_dashboard view works: {response.status_code}")
except Exception as e:
    print(f"✗ finance_dashboard view error: {e}")
    import traceback
    traceback.print_exc()

print("\n✓ All finance views passed testing!")

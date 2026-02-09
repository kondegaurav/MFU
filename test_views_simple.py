#!/usr/bin/env python
"""Quick test of finance portal views."""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.test import RequestFactory
from django.template import TemplateDoesNotExist
from apps.finance_portal.views import equipment_requests, transactions_list

# Create test request
factory = RequestFactory()
from apps.core.models import User, UserRole

# Get test user
test_user, _ = User.objects.get_or_create(
    username='testfinance',
    defaults={'email': 'test@example.com', 'is_active': True}
)

# Get or create role
role, _ = UserRole.objects.get_or_create(user=test_user, role='finance_inventory')

print(f"Test user: {test_user.username}, Role: {role.role}")

# Test equipment_requests
try:
    request = factory.get('/finance/equipment-requests/')
    request.user = test_user
    response = equipment_requests(request)
    print(f"✓ equipment_requests: Status {response.status_code}")
except TemplateDoesNotExist as e:
    print(f"✗ Missing template: {e}")
except Exception as e:
    print(f"✗ equipment_requests error: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()

# Test transactions_list  
try:
    request = factory.get('/finance/transactions/')
    request.user = test_user
    response = transactions_list(request)
    print(f"✓ transactions_list: Status {response.status_code}")
except TemplateDoesNotExist as e:
    print(f"✗ Missing template: {e}")
except Exception as e:
    print(f"✗ transactions_list error: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()

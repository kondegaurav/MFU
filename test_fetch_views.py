#!/usr/bin/env python
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE','config.settings')
django.setup()
from django.test import Client
from apps.core.models import User, UserRole

client = Client()
# create test user
user, created = User.objects.get_or_create(username='test_finance', defaults={'email':'test@local','is_active':True})
UserRole.objects.get_or_create(user=user, role='finance_inventory')
# login
user.set_password('testpass')
user.save()
logged_in = client.login(username='test_finance', password='testpass')
print('logged_in', logged_in)
for url in ['/finance-portal/equipment/','/finance-portal/equipment-requests/','/finance-portal/transactions/']:
    resp = client.get(url)
    print(url, resp.status_code)
    if resp.status_code != 200:
        print(resp.content[:1000])

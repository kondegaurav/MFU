#!/usr/bin/env python
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE','config.settings.development')
django.setup()
from django.test import Client
from django.contrib.auth import get_user_model
User = get_user_model()
print('Test: find coach user')
try:
    u = User.objects.get(email__iexact='coach1@gmail.com')
    print('Found user:', u.email, 'is_active=', u.is_active, 'email_confirmed=', getattr(u,'email_confirmed',None))
except Exception as e:
    print('Error:', e)

c = Client()
logged_in = c.login(email='coach1@gmail.com', password='ChangeMe123!')
print('login ok=', logged_in)
resp = c.get('/coach-portal/dashboard/')
print('GET /coach-portal/dashboard/ status_code=', resp.status_code)
print('response content head:', resp.content[:500])

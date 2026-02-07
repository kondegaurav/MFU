
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from apps.core.models import Role

print("Checking Roles for empty dashboard_url...")
roles = Role.objects.all()
for r in roles:
    print(f"Role: {r.name} ({r.code}) -> URL: '{r.dashboard_url}'")
    if not r.dashboard_url:
        print(f"WARNING: Role {r.name} has empty dashboard_url!")


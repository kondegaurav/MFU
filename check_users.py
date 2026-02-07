
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from apps.core.models import User

users = User.objects.all()
print(f"Total Users: {users.count()}")
print("-" * 60)
print(f"{'Email':<30} | {'Active':<7} | {'Roles'}")
print("-" * 60)

for user in users:
    roles = ", ".join([r.name for r in user.roles.all()])
    print(f"{user.email:<30} | {str(user.is_active):<7} | {roles}")

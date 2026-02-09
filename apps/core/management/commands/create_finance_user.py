"""
Management command to create demo finance user with correct role.
Usage: python manage.py create_finance_user
"""

from django.core.management.base import BaseCommand
from apps.core.models import User, Role, UserRole


class Command(BaseCommand):
    help = 'Create or update demo finance user with finance_inventory role'

    def handle(self, *args, **options):
        email = 'finance@mfu.com'
        password = 'password123'
        first_name = 'Finance'
        last_name = 'Manager'

        # Ensure role exists
        try:
            role = Role.objects.get(code=Role.FINANCE_INVENTORY)
            self.stdout.write(self.style.SUCCESS(f'✓ Role exists: {role.name}'))
        except Role.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'✗ Role does not exist: {Role.FINANCE_INVENTORY}'))
            self.stdout.write('Run: python manage.py seed_roles')
            return

        # Create or get user
        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                'first_name': first_name,
                'last_name': last_name,
                'is_active': True,
                'email_confirmed': True,
            }
        )

        if created:
            user.set_password(password)
            user.save()
            self.stdout.write(self.style.SUCCESS(f'✓ Created user: {email}'))
        else:
            self.stdout.write(f'  User already exists: {email}')
            # Ensure user is active and email confirmed
            changed = False
            if not user.is_active:
                user.is_active = True
                changed = True
            if not user.email_confirmed:
                user.email_confirmed = True
                changed = True
            if changed:
                user.save()
                self.stdout.write('  Activated user and confirmed email')

        # Assign role
        user_role, role_created = UserRole.objects.get_or_create(
            user=user,
            role=role,
            defaults={'assigned_by': None}
        )

        if role_created:
            self.stdout.write(self.style.SUCCESS(f'✓ Assigned role: {role.name}'))
        else:
            self.stdout.write(f'  Role already assigned: {role.name}')

        self.stdout.write(self.style.SUCCESS('\n✓ Finance user is ready!'))
        self.stdout.write(f'  Email: {email}')
        self.stdout.write(f'  Password: {password}')

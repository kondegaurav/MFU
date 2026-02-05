"""
Management command to seed initial roles and role tags.
Usage: python manage.py seed_roles
"""

from django.core.management.base import BaseCommand
from apps.core.models import Role, RoleTag


class Command(BaseCommand):
    help = 'Seed initial roles and role tags for MFU Portal'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting to seed roles and tags...'))

        # Create roles
        roles_data = [
            {
                'code': Role.ADMIN,
                'name': 'Admin',
                'description': 'Administrative privileges for managing centers, coaches, and events',
                'dashboard_url': 'admin_portal:dashboard',
                'dashboard_icon': 'bi-shield-check',
                'display_order': 1
            },
            {
                'code': Role.COACH,
                'name': 'Coach',
                'description': 'Coach privileges for managing certifications, attendance, and evaluations',
                'dashboard_url': 'coach_portal:dashboard',
                'dashboard_icon': 'bi-clipboard-check',
                'display_order': 2
            },
            {
                'code': Role.PARENT,
                'name': 'Parent',
                'description': 'Parent privileges for managing children enrollments and activities',
                'dashboard_url': 'parent_portal:dashboard',
                'dashboard_icon': 'bi-house-heart',
                'display_order': 3
            },
            {
                'code': Role.ATHLETE,
                'name': 'Athlete',
                'description': 'Athlete privileges for viewing scores and rankings',
                'dashboard_url': 'athlete_portal:dashboard',
                'dashboard_icon': 'bi-trophy',
                'display_order': 4
            },
            {
                'code': Role.FINANCE_INVENTORY,
                'name': 'Finance & Inventory Manager',
                'description': 'Finance and inventory management privileges',
                'dashboard_url': 'finance_portal:dashboard',
                'dashboard_icon': 'bi-cash-stack',
                'display_order': 5
            },
        ]

        for role_data in roles_data:
            role, created = Role.objects.get_or_create(
                code=role_data['code'],
                defaults=role_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'+ Created role: {role.name}'))
            else:
                self.stdout.write(f'  Role already exists: {role.name}')

        # Create role tags
        self.stdout.write('\nSeeding role tags...')

        admin_role = Role.objects.get(code=Role.ADMIN)
        coach_role = Role.objects.get(code=Role.COACH)

        tags_data = [
            {
                'code': RoleTag.CENTER_HEAD,
                'name': 'Center Head',
                'description': 'Additional privileges for center heads (event management, volunteering, equipment requests)',
                'applicable_to_role': admin_role
            },
            {
                'code': RoleTag.HEAD_COACH,
                'name': 'Head Coach',
                'description': 'Additional privileges for head coaches (create competition teams)',
                'applicable_to_role': coach_role
            },
        ]

        for tag_data in tags_data:
            tag, created = RoleTag.objects.get_or_create(
                code=tag_data['code'],
                defaults=tag_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'+ Created tag: {tag.name}'))
            else:
                self.stdout.write(f'  Tag already exists: {tag.name}')

        self.stdout.write(self.style.SUCCESS('\nSuccessfully seeded all roles and tags!'))

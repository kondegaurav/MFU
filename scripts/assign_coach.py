from apps.core.models import User, Role, UserRole
from apps.coach_portal.models import CoachProfile

EMAIL = 'coach1@gmail.com'
ROLE_CODE = 'coach'

u = User.objects.filter(email__iexact=EMAIL).first()
if not u:
    print(f"User with email {EMAIL} not found.")
else:
    role = Role.objects.filter(code=ROLE_CODE).first()
    if not role:
        print(f"Role with code '{ROLE_CODE}' not found. Run seed_roles.")
    else:
        ur, created = UserRole.objects.get_or_create(user=u, role=role, defaults={'assigned_by': None})
        print('UserRole created' if created else 'UserRole already exists')

    changed = False
    if not u.is_active:
        u.is_active = True
        changed = True
    if not u.email_confirmed:
        u.email_confirmed = True
        changed = True
    if changed:
        u.save()
        print('User activated and email confirmed')
    else:
        print('User already active and email confirmed')

    cp, cp_created = CoachProfile.objects.get_or_create(user=u)
    print('CoachProfile created' if cp_created else 'CoachProfile already exists')

    print('Done. You can now visit /coach-portal/dashboard/')

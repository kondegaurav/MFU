from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from apps.admin_portal.views import admin_dashboard
from apps.core.models import Role, UserRole

User = get_user_model()

class AdminDashboardViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            email='admin@test.com',
            password='password'
        )
        # Assign admin role
        self.role = Role.objects.create(
            code='admin', 
            name='Admin',
            dashboard_url='admin_portal:dashboard'
        )
        UserRole.objects.create(user=self.user, role=self.role)

    def test_admin_dashboard_field_error(self):
        request = self.factory.get('/admin-portal/dashboard/')
        request.user = self.user
        
        response = admin_dashboard(request)
        self.assertEqual(response.status_code, 200)

from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

from apps.core.services.permission_service import PermissionService
from apps.core.models import Role, RoleTag
from apps.core.decorators.permissions import (
	require_roles,
	require_tags,
	require_role_and_tag,
)
from apps.core.mixins.permissions import RoleRequiredMixin


@login_required
def permission_examples(request):
	"""
	Simple page demonstrating permission checks and available dashboards.
	Used to test and showcase the PermissionService, decorators and mixins.
	"""
	user = request.user
	dashboards = PermissionService.get_user_dashboard_urls(user)

	context = {
		'user': user,
		'dashboards': dashboards,
		'can_manage_events': PermissionService.can_manage_events(user),
		'can_create_teams': PermissionService.can_create_competition_teams(user),
		'can_raise_requests': PermissionService.can_raise_equipment_requests(user),
	}
	return render(request, 'core/permission_examples.html', context)


@require_roles([Role.ADMIN])
def admin_only_view(request):
	return HttpResponse('This is an admin-only view')


@require_role_and_tag(Role.ADMIN, RoleTag.CENTER_HEAD)
def admin_center_head_view(request):
	return HttpResponse('Admin + Center Head required')


class CoachExampleView(RoleRequiredMixin, TemplateView):
	required_roles = [Role.COACH]
	template_name = 'core/permission_examples.html'

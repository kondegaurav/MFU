"""
Template tags for permission checks.

Usage in templates:
    {% load permission_tags %}

    {% if request.user|has_role:'admin' %}
        <p>Admin content here</p>
    {% endif %}

    {% if request.user|has_tag:'center_head' %}
        <p>Center Head content here</p>
    {% endif %}

    {% if request.user|can_manage_events %}
        <a href="...">Manage Events</a>
    {% endif %}
"""
from django import template
from apps.core.services import PermissionService
from apps.core.models import Role, RoleTag

register = template.Library()


@register.filter
def has_role(user, role_code):
    """
    Check if user has a specific role.

    Usage: {% if user|has_role:'admin' %}
    """
    return PermissionService.has_role(user, role_code)


@register.filter
def has_any_role(user, role_codes):
    """
    Check if user has any of the specified roles.

    Usage: {% if user|has_any_role:'admin,coach' %}
    """
    if isinstance(role_codes, str):
        role_codes = [code.strip() for code in role_codes.split(',')]
    return PermissionService.has_any_role(user, role_codes)


@register.filter
def has_tag(user, tag_code):
    """
    Check if user has a specific tag.

    Usage: {% if user|has_tag:'center_head' %}
    """
    return PermissionService.has_tag(user, tag_code)


@register.filter
def has_any_tag(user, tag_codes):
    """
    Check if user has any of the specified tags.

    Usage: {% if user|has_any_tag:'center_head,head_coach' %}
    """
    if isinstance(tag_codes, str):
        tag_codes = [code.strip() for code in tag_codes.split(',')]
    return PermissionService.has_any_tag(user, tag_codes)


@register.filter
def can_manage_events(user):
    """
    Check if user can manage events.

    Usage: {% if user|can_manage_events %}
    """
    return PermissionService.can_manage_events(user)


@register.filter
def can_manage_volunteering(user):
    """
    Check if user can manage volunteering.

    Usage: {% if user|can_manage_volunteering %}
    """
    return PermissionService.can_manage_volunteering(user)


@register.filter
def can_raise_equipment_requests(user):
    """
    Check if user can raise equipment requests.

    Usage: {% if user|can_raise_equipment_requests %}
    """
    return PermissionService.can_raise_equipment_requests(user)


@register.filter
def can_create_competition_teams(user):
    """
    Check if user can create competition teams.

    Usage: {% if user|can_create_competition_teams %}
    """
    return PermissionService.can_create_competition_teams(user)


@register.simple_tag
def get_user_dashboards(user):
    """
    Get all dashboards accessible to the user.

    Usage: {% get_user_dashboards request.user as dashboards %}
    """
    return PermissionService.get_user_dashboard_urls(user)


@register.inclusion_tag('core/tags/role_badge.html')
def show_role_badge(role):
    """
    Display a role badge.

    Usage: {% show_role_badge role %}
    """
    return {'role': role}


@register.inclusion_tag('core/tags/tag_badge.html')
def show_tag_badge(tag):
    """
    Display a tag badge.

    Usage: {% show_tag_badge tag %}
    """
    return {'tag': tag}

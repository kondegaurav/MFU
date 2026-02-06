"""
Permission decorators for view protection.
"""
from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from apps.core.services import PermissionService


def require_roles(role_codes, require_all=False):
    """
    Decorator to require specific roles.

    Usage:
        @require_roles([Role.ADMIN])
        def my_view(request):
            ...

        @require_roles([Role.ADMIN, Role.COACH], require_all=True)
        def my_view(request):
            ...

    Args:
        role_codes: Single role code or list of role codes
        require_all: If True, user must have all roles. If False, any role is sufficient.

    Returns:
        Decorator function
    """
    # Convert single role to list
    if not isinstance(role_codes, (list, tuple)):
        role_codes = [role_codes]

    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def wrapper(request, *args, **kwargs):
            user = request.user

            # Check permissions
            if require_all:
                has_permission = PermissionService.has_all_roles(user, role_codes)
            else:
                has_permission = PermissionService.has_any_role(user, role_codes)

            if not has_permission:
                messages.error(
                    request,
                    'You do not have permission to access this page. '
                    'Required role(s) are missing.'
                )
                raise PermissionDenied('Insufficient role permissions')

            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def require_tags(tag_codes, require_all=False):
    """
    Decorator to require specific role tags.

    Usage:
        @require_tags([RoleTag.CENTER_HEAD])
        def my_view(request):
            ...

    Args:
        tag_codes: Single tag code or list of tag codes
        require_all: If True, user must have all tags. If False, any tag is sufficient.

    Returns:
        Decorator function
    """
    # Convert single tag to list
    if not isinstance(tag_codes, (list, tuple)):
        tag_codes = [tag_codes]

    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def wrapper(request, *args, **kwargs):
            user = request.user

            # Check permissions
            if require_all:
                has_permission = all(
                    PermissionService.has_tag(user, tag_code)
                    for tag_code in tag_codes
                )
            else:
                has_permission = PermissionService.has_any_tag(user, tag_codes)

            if not has_permission:
                messages.error(
                    request,
                    'You do not have permission to access this page. '
                    'Required privilege tag(s) are missing.'
                )
                raise PermissionDenied('Insufficient tag permissions')

            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def require_role_and_tag(role_code, tag_code):
    """
    Decorator to require both a specific role AND a specific tag.

    Usage:
        @require_role_and_tag(Role.ADMIN, RoleTag.CENTER_HEAD)
        def my_view(request):
            ...

    Args:
        role_code: Required role code
        tag_code: Required tag code

    Returns:
        Decorator function
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def wrapper(request, *args, **kwargs):
            user = request.user

            has_role = PermissionService.has_role(user, role_code)
            has_tag = PermissionService.has_tag(user, tag_code)

            if not (has_role and has_tag):
                messages.error(
                    request,
                    'You do not have permission to access this page. '
                    'Both role and privilege tag are required.'
                )
                raise PermissionDenied('Insufficient role and tag permissions')

            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

"""
Permission mixins for class-based views.
"""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from apps.core.services import PermissionService


class RoleRequiredMixin(LoginRequiredMixin):
    """
    Mixin to require specific roles for class-based views.

    Usage:
        class MyView(RoleRequiredMixin, View):
            required_roles = [Role.ADMIN]
            require_all_roles = False  # Optional, default False
            ...
    """
    required_roles = []
    require_all_roles = False

    def dispatch(self, request, *args, **kwargs):
        if not self.required_roles:
            raise ValueError('required_roles must be set')

        user = request.user

        # Check if user is authenticated (LoginRequiredMixin handles this)
        if not user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)

        # Check role permissions
        if self.require_all_roles:
            has_permission = PermissionService.has_all_roles(user, self.required_roles)
        else:
            has_permission = PermissionService.has_any_role(user, self.required_roles)

        if not has_permission:
            messages.error(
                request,
                'You do not have permission to access this page. '
                'Required role(s) are missing.'
            )
            raise PermissionDenied('Insufficient role permissions')

        return super().dispatch(request, *args, **kwargs)


class TagRequiredMixin(LoginRequiredMixin):
    """
    Mixin to require specific role tags for class-based views.

    Usage:
        class MyView(TagRequiredMixin, View):
            required_tags = [RoleTag.CENTER_HEAD]
            require_all_tags = False  # Optional, default False
            ...
    """
    required_tags = []
    require_all_tags = False

    def dispatch(self, request, *args, **kwargs):
        if not self.required_tags:
            raise ValueError('required_tags must be set')

        user = request.user

        # Check if user is authenticated
        if not user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)

        # Check tag permissions
        if self.require_all_tags:
            has_permission = all(
                PermissionService.has_tag(user, tag_code)
                for tag_code in self.required_tags
            )
        else:
            has_permission = PermissionService.has_any_tag(user, self.required_tags)

        if not has_permission:
            messages.error(
                request,
                'You do not have permission to access this page. '
                'Required privilege tag(s) are missing.'
            )
            raise PermissionDenied('Insufficient tag permissions')

        return super().dispatch(request, *args, **kwargs)


class RoleAndTagRequiredMixin(LoginRequiredMixin):
    """
    Mixin to require both a specific role AND tag for class-based views.

    Usage:
        class MyView(RoleAndTagRequiredMixin, View):
            required_role = Role.ADMIN
            required_tag = RoleTag.CENTER_HEAD
            ...
    """
    required_role = None
    required_tag = None

    def dispatch(self, request, *args, **kwargs):
        if not self.required_role or not self.required_tag:
            raise ValueError('Both required_role and required_tag must be set')

        user = request.user

        # Check if user is authenticated
        if not user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)

        # Check both role and tag
        has_role = PermissionService.has_role(user, self.required_role)
        has_tag = PermissionService.has_tag(user, self.required_tag)

        if not (has_role and has_tag):
            messages.error(
                request,
                'You do not have permission to access this page. '
                'Both role and privilege tag are required.'
            )
            raise PermissionDenied('Insufficient role and tag permissions')

        return super().dispatch(request, *args, **kwargs)

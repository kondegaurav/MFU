"""
Centralized Permission Service for MFU Web Portal.
Handles all role-based and tag-based permission checks.
"""
from apps.core.models import Role, RoleTag


class PermissionService:
    """
    Service class for checking user permissions.
    All permission logic should go through this service.
    """

    @staticmethod
    def has_role(user, role_code):
        """
        Check if user has a specific role.

        Args:
            user: User instance
            role_code: Role code (e.g., Role.ADMIN)

        Returns:
            bool: True if user has the role
        """
        if not user or not user.is_authenticated:
            return False
        return user.has_role(role_code)

    @staticmethod
    def has_any_role(user, role_codes):
        """
        Check if user has any of the specified roles.

        Args:
            user: User instance
            role_codes: List of role codes

        Returns:
            bool: True if user has at least one of the roles
        """
        if not user or not user.is_authenticated:
            return False
        return user.has_any_role(role_codes)

    @staticmethod
    def has_all_roles(user, role_codes):
        """
        Check if user has all of the specified roles.

        Args:
            user: User instance
            role_codes: List of role codes

        Returns:
            bool: True if user has all the roles
        """
        if not user or not user.is_authenticated:
            return False
        for role_code in role_codes:
            if not user.has_role(role_code):
                return False
        return True

    @staticmethod
    def has_tag(user, tag_code):
        """
        Check if user has a specific role tag.

        Args:
            user: User instance
            tag_code: Tag code (e.g., RoleTag.CENTER_HEAD)

        Returns:
            bool: True if user has the tag
        """
        if not user or not user.is_authenticated:
            return False
        return user.has_tag(tag_code)

    @staticmethod
    def has_any_tag(user, tag_codes):
        """
        Check if user has any of the specified tags.

        Args:
            user: User instance
            tag_codes: List of tag codes

        Returns:
            bool: True if user has at least one of the tags
        """
        if not user or not user.is_authenticated:
            return False
        for tag_code in tag_codes:
            if user.has_tag(tag_code):
                return True
        return False

    @staticmethod
    def can_manage_events(user):
        """
        Check if user can manage events.
        Only Admins with Center Head tag can manage events.

        Args:
            user: User instance

        Returns:
            bool: True if user can manage events
        """
        return (
            PermissionService.has_role(user, Role.ADMIN) and
            PermissionService.has_tag(user, RoleTag.CENTER_HEAD)
        )

    @staticmethod
    def can_manage_volunteering(user):
        """
        Check if user can manage volunteering opportunities.
        Only Admins with Center Head tag can manage volunteering.

        Args:
            user: User instance

        Returns:
            bool: True if user can manage volunteering
        """
        return (
            PermissionService.has_role(user, Role.ADMIN) and
            PermissionService.has_tag(user, RoleTag.CENTER_HEAD)
        )

    @staticmethod
    def can_raise_equipment_requests(user):
        """
        Check if user can raise equipment requests.
        Only Admins with Center Head tag can raise equipment requests.

        Args:
            user: User instance

        Returns:
            bool: True if user can raise equipment requests
        """
        return (
            PermissionService.has_role(user, Role.ADMIN) and
            PermissionService.has_tag(user, RoleTag.CENTER_HEAD)
        )

    @staticmethod
    def can_create_competition_teams(user):
        """
        Check if user can create competition teams.
        Only Coaches with Head Coach tag can create teams.

        Args:
            user: User instance

        Returns:
            bool: True if user can create competition teams
        """
        return (
            PermissionService.has_role(user, Role.COACH) and
            PermissionService.has_tag(user, RoleTag.HEAD_COACH)
        )

    @staticmethod
    def can_view_child_rankings(user, child_age):
        """
        Check if user can view child rankings.
        Parents can only view rankings for children aged 12 or older.

        Args:
            user: User instance
            child_age: Age of the child

        Returns:
            bool: True if user can view rankings
        """
        return (
            PermissionService.has_role(user, Role.PARENT) and
            child_age >= 12
        )

    @staticmethod
    def can_view_child_scores(user, child_age):
        """
        Check if user can view child scores.
        Parents can only view scores for children aged 12 or older.

        Args:
            user: User instance
            child_age: Age of the child

        Returns:
            bool: True if user can view scores
        """
        return (
            PermissionService.has_role(user, Role.PARENT) and
            child_age >= 12
        )

    @staticmethod
    def can_view_evaluation_certificates(user, child_age):
        """
        Check if user can view evaluation certificates.
        Parents can only view certificates for children aged 12 or older.

        Args:
            user: User instance
            child_age: Age of the child

        Returns:
            bool: True if user can view certificates
        """
        return (
            PermissionService.has_role(user, Role.PARENT) and
            child_age >= 12
        )

    @staticmethod
    def get_user_dashboard_urls(user):
        """
        Get all dashboard URLs that the user has access to.

        Args:
            user: User instance

        Returns:
            list: List of tuples (role_name, dashboard_url, icon)
        """
        if not user or not user.is_authenticated:
            return []

        dashboards = []
        for role in user.get_active_roles():
            dashboards.append({
                'name': role.name,
                'url': role.dashboard_url,
                'icon': role.dashboard_icon,
                'code': role.code,
            })
        return dashboards

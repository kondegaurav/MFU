"""
Core models for MFU Web Portal.
Contains User, Role, and RoleTag models - the foundation of the authentication system.
"""

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone


class UserManager(BaseUserManager):
    """Custom user manager for email-based authentication."""

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular user with the given email and password."""
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a superuser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('email_confirmed', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class Role(models.Model):
    """
    User roles in the system.
    Each role corresponds to a dashboard with specific permissions.
    """

    # Role constants
    ADMIN = 'admin'
    COACH = 'coach'
    PARENT = 'parent'
    ATHLETE = 'athlete'
    FINANCE_INVENTORY = 'finance_inventory'

    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (COACH, 'Coach'),
        (PARENT, 'Parent'),
        (ATHLETE, 'Athlete'),
        (FINANCE_INVENTORY, 'Finance & Inventory Manager'),
    ]

    code = models.CharField(
        max_length=50,
        unique=True,
        choices=ROLE_CHOICES,
        db_index=True
    )
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    dashboard_url = models.CharField(max_length=200, help_text="URL name for this role's dashboard")
    dashboard_icon = models.CharField(max_length=50, default='bi-dashboard', help_text="Bootstrap icon class")
    display_order = models.PositiveIntegerField(default=0, help_text="Order in which tabs appear")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'roles'
        ordering = ['display_order', 'name']
        verbose_name = 'Role'
        verbose_name_plural = 'Roles'

    def __str__(self):
        return self.name


class RoleTag(models.Model):
    """
    Conditional privileges that extend role permissions.
    Example: 'Center Head' tag gives additional permissions to Admin role.
    """

    # Tag constants
    CENTER_HEAD = 'center_head'
    HEAD_COACH = 'head_coach'

    TAG_CHOICES = [
        (CENTER_HEAD, 'Center Head'),
        (HEAD_COACH, 'Head Coach'),
    ]

    code = models.CharField(
        max_length=50,
        unique=True,
        choices=TAG_CHOICES,
        db_index=True
    )
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    applicable_to_role = models.ForeignKey(
        Role,
        on_delete=models.CASCADE,
        related_name='tags',
        help_text="Which role can have this tag"
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'role_tags'
        ordering = ['name']
        verbose_name = 'Role Tag'
        verbose_name_plural = 'Role Tags'

    def __str__(self):
        return f"{self.name} ({self.applicable_to_role.name})"


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model for MFU Web Portal.
    Uses email as the unique identifier instead of username.
    Supports multiple roles and role tags.
    """

    email = models.EmailField(
        unique=True,
        db_index=True,
        error_messages={
            'unique': 'A user with that email already exists.',
        }
    )
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)

    # Many-to-many relationships
    roles = models.ManyToManyField(
        Role,
        through='UserRole',
        through_fields=('user', 'role'),
        related_name='users',
        blank=True
    )
    role_tags = models.ManyToManyField(
        RoleTag,
        through='UserRoleTag',
        through_fields=('user', 'role_tag'),
        related_name='users',
        blank=True
    )

    # Account status
    is_active = models.BooleanField(
        default=False,
        help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.'
    )
    is_staff = models.BooleanField(
        default=False,
        help_text='Designates whether the user can log into the admin site.'
    )
    email_confirmed = models.BooleanField(
        default=False,
        help_text='Designates whether the user has confirmed their email address.'
    )

    # Timestamps
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Soft delete
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        db_table = 'users'
        ordering = ['-date_joined']
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['email', 'is_active']),
            models.Index(fields=['email', 'email_confirmed']),
        ]

    def __str__(self):
        return self.email

    def get_full_name(self):
        """Return the first_name plus the last_name, with a space in between."""
        full_name = f'{self.first_name} {self.last_name}'.strip()
        return full_name or self.email

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name or self.email.split('@')[0]

    def has_role(self, role_code):
        """Check if user has a specific role."""
        return self.roles.filter(code=role_code, is_active=True).exists()

    def has_any_role(self, role_codes):
        """Check if user has any of the specified roles."""
        return self.roles.filter(code__in=role_codes, is_active=True).exists()

    def has_tag(self, tag_code):
        """Check if user has a specific role tag."""
        return self.role_tags.filter(code=tag_code, is_active=True).exists()

    def get_active_roles(self):
        """Get all active roles for this user."""
        return self.roles.filter(is_active=True).order_by('display_order')

    def get_active_tags(self):
        """Get all active role tags for this user."""
        return self.role_tags.filter(is_active=True)


class UserRole(models.Model):
    """Through table for User-Role many-to-many relationship."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    assigned_at = models.DateTimeField(auto_now_add=True)
    assigned_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='roles_assigned'
    )

    class Meta:
        db_table = 'user_roles'
        unique_together = ['user', 'role']
        verbose_name = 'User Role'
        verbose_name_plural = 'User Roles'

    def __str__(self):
        return f"{self.user.email} - {self.role.name}"


class UserRoleTag(models.Model):
    """Through table for User-RoleTag many-to-many relationship."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role_tag = models.ForeignKey(RoleTag, on_delete=models.CASCADE)
    assigned_at = models.DateTimeField(auto_now_add=True)
    assigned_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tags_assigned'
    )

    class Meta:
        db_table = 'user_role_tags'
        unique_together = ['user', 'role_tag']
        verbose_name = 'User Role Tag'
        verbose_name_plural = 'User Role Tags'

    def __str__(self):
        return f"{self.user.email} - {self.role_tag.name}"

"""
Parent models for MFU Web Portal.
Manages parent/guardian relationships and child data access.
"""
from django.db import models
from django.utils import timezone
from apps.core.models import User
from apps.athlete_portal.models import AthletePerson


class Parent(models.Model):
    """
    Parent/Guardian profile linked to a user.
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='parent_profile'
    )
    
    occupation = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    alternate_phone = models.CharField(max_length=20, blank=True)
    
    is_primary_contact = models.BooleanField(
        default=True,
        help_text="Is this the primary emergency contact?"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'parents'
        verbose_name = 'Parent'
        verbose_name_plural = 'Parents'
    
    def __str__(self):
        return f"Parent: {self.user.get_full_name()}"
    
    def get_children(self):
        """Get all children linked to this parent."""
        return self.children.filter(is_active=True)


class ParentChildRelation(models.Model):
    """
    Relationship between a parent and their child (athlete).
    Defines what data parent can access.
    """
    RELATIONSHIP_CHOICES = [
        ('mother', 'Mother'),
        ('father', 'Father'),
        ('guardian', 'Guardian'),
        ('grandparent', 'Grandparent'),
        ('other', 'Other'),
    ]
    
    parent = models.ForeignKey(
        Parent,
        on_delete=models.CASCADE,
        related_name='children'
    )
    
    child = models.ForeignKey(
        AthletePerson,
        on_delete=models.CASCADE,
        related_name='parents'
    )
    
    relationship = models.CharField(
        max_length=50,
        choices=RELATIONSHIP_CHOICES,
        default='parent'
    )
    
    # What can this parent view?
    can_view_scores = models.BooleanField(
        default=True,
        help_text="Can view child's scores and results"
    )
    can_view_rankings = models.BooleanField(
        default=True,
        help_text="Can view child's rankings (only for 12+)"
    )
    can_view_certificates = models.BooleanField(
        default=True,
        help_text="Can view child's certificates"
    )
    can_view_attendance = models.BooleanField(
        default=True,
        help_text="Can view training session attendance"
    )
    can_view_fees = models.BooleanField(
        default=False,
        help_text="Can view fee and payment information"
    )
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'parent_child_relations'
        unique_together = ['parent', 'child']
        ordering = ['child__last_name', 'child__first_name']
        verbose_name = 'Parent Child Relation'
        verbose_name_plural = 'Parent Child Relations'
    
    def __str__(self):
        return f"{self.parent.user.get_full_name()} → {self.child.get_full_name()}"
    
    def can_view_child_rankings(self):
        """Check if parent can view child's rankings."""
        # Parents can only view rankings for children 12+
        return self.can_view_rankings and self.child.age >= 12

"""
Volunteering models for MFU Web Portal.
Manages volunteering opportunities and volunteer management.
"""
from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from apps.core.models import User
from apps.centers.models import Center


class VolunteeringOpportunity(models.Model):
    """
    A volunteering opportunity available at a center.
    """
    STATUS_CHOICES = [
        ('open', 'Open for Volunteers'),
        ('closed', 'Closed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    title = models.CharField(max_length=255, db_index=True)
    description = models.TextField()
    center = models.ForeignKey(
        Center,
        on_delete=models.PROTECT,
        related_name='volunteering_opportunities'
    )
    
    opportunity_type = models.CharField(
        max_length=50,
        choices=[
            ('event_support', 'Event Support'),
            ('coaching', 'Coaching Assistant'),
            ('admin', 'Administrative'),
            ('maintenance', 'Maintenance'),
            ('coaching_mentorship', 'Coaching Mentorship'),
        ],
        default='event_support'
    )
    
    # Timing
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    required_hours = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=4,
        help_text="Expected hours for this opportunity"
    )
    
    # Requirements
    required_skills = models.CharField(max_length=500, blank=True, help_text="Comma-separated list")
    min_age = models.PositiveIntegerField(default=16)
    max_volunteers = models.PositiveIntegerField(
        default=10,
        validators=[MinValueValidator(1)]
    )
    current_volunteers = models.PositiveIntegerField(default=0)
    
    # Management
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_opportunities'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='open',
        db_index=True
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'volunteering_opportunities'
        ordering = ['-start_date']
        verbose_name = 'Volunteering Opportunity'
        verbose_name_plural = 'Volunteering Opportunities'
        indexes = [
            models.Index(fields=['center', 'status']),
        ]
    
    def __str__(self):
        return f"{self.title} at {self.center.name}"
    
    def is_full(self):
        """Check if opportunity has reached max volunteers."""
        return self.current_volunteers >= self.max_volunteers
    
    def can_volunteer(self):
        """Check if new volunteers can sign up."""
        now = timezone.now()
        return self.status == 'open' and now < self.start_date and not self.is_full()


class VolunteerApplication(models.Model):
    """
    A volunteer's application/signup for an opportunity.
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    opportunity = models.ForeignKey(
        VolunteeringOpportunity,
        on_delete=models.CASCADE,
        related_name='applications'
    )
    volunteer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='volunteer_applications'
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    
    # Application details
    motivation = models.TextField(blank=True, help_text="Why volunteer is interested")
    experience = models.TextField(blank=True, help_text="Relevant experience")
    hours_completed = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        help_text="Hours actually volunteered"
    )
    
    # Approval
    approved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_volunteer_applications'
    )
    approval_notes = models.TextField(blank=True)
    
    applied_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'volunteer_applications'
        unique_together = ['opportunity', 'volunteer']
        ordering = ['-applied_at']
        verbose_name = 'Volunteer Application'
        verbose_name_plural = 'Volunteer Applications'
    
    def __str__(self):
        return f"{self.volunteer.get_full_name()} - {self.opportunity.title}"

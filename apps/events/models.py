"""
Event models for MFU Web Portal.
Manages sports events and competitions.
"""
from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from apps.core.models import User
from apps.centers.models import Center


class Event(models.Model):
    """
    A sports event or competition held at a center.
    """
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    name = models.CharField(max_length=255, db_index=True)
    description = models.TextField()
    center = models.ForeignKey(
        Center,
        on_delete=models.PROTECT,
        related_name='events'
    )
    event_type = models.CharField(
        max_length=50,
        choices=[
            ('competition', 'Competition'),
            ('training', 'Training'),
            ('seminar', 'Seminar'),
            ('tournament', 'Tournament'),
        ],
        default='competition'
    )
    
    # Dates
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    registration_start = models.DateTimeField()
    registration_end = models.DateTimeField()
    
    # Capacity
    max_participants = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        help_text="Maximum number of participants"
    )
    current_participants = models.PositiveIntegerField(default=0)
    
    # Management
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_events'
    )
    organizers = models.ManyToManyField(
        User,
        related_name='organized_events',
        blank=True,
        help_text="Users who can manage this event"
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft',
        db_index=True
    )
    
    # Additional info
    entry_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)]
    )
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'events'
        ordering = ['-start_date']
        verbose_name = 'Event'
        verbose_name_plural = 'Events'
        indexes = [
            models.Index(fields=['center', 'status']),
            models.Index(fields=['start_date', 'status']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.get_status_display()})"
    
    def is_registration_open(self):
        """Check if registration is currently open."""
        now = timezone.now()
        return self.registration_start <= now <= self.registration_end
    
    def is_full(self):
        """Check if event has reached max capacity."""
        return self.current_participants >= self.max_participants
    
    def can_register(self):
        """Check if new registrations are allowed."""
        return self.is_registration_open() and not self.is_full()


class EventRegistration(models.Model):
    """
    Participant registration for an event.
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='registrations'
    )
    participant = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='event_registrations'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    
    # Registration details
    bib_number = models.CharField(max_length=50, blank=True, help_text="Participant bib/race number")
    team_name = models.CharField(max_length=255, blank=True)
    category = models.CharField(max_length=100, blank=True, help_text="Age group or skill category")
    notes = models.TextField(blank=True)
    
    # Payment
    amount_paid = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)]
    )
    payment_status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('completed', 'Completed'),
            ('refunded', 'Refunded'),
        ],
        default='pending'
    )
    
    registered_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'event_registrations'
        unique_together = ['event', 'participant']
        ordering = ['-registered_at']
        verbose_name = 'Event Registration'
        verbose_name_plural = 'Event Registrations'
    
    def __str__(self):
        return f"{self.participant.get_full_name()} - {self.event.name}"

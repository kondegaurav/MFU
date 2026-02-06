"""
Center models for MFU Web Portal.
Manages sports facilities and center information.
"""
from django.db import models
from django.core.validators import MinValueValidator, URLValidator
from django.utils import timezone
from apps.core.models import User


class Center(models.Model):
    """
    A sports center or facility where events, training, and volunteering happen.
    """
    name = models.CharField(max_length=200, unique=True, db_index=True)
    description = models.TextField(blank=True)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, default='India')
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    website = models.URLField(blank=True, validators=[URLValidator()])
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
    # Center management
    center_head = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='managed_centers',
        help_text="Admin user assigned as Center Head"
    )
    
    # Capacity and facilities
    total_capacity = models.PositiveIntegerField(
        default=100,
        validators=[MinValueValidator(1)],
        help_text="Total capacity of the center"
    )
    has_indoor_facility = models.BooleanField(default=True)
    has_outdoor_facility = models.BooleanField(default=False)
    has_parking = models.BooleanField(default=False)
    has_food_court = models.BooleanField(default=False)
    
    # Status
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'centers'
        ordering = ['name']
        verbose_name = 'Center'
        verbose_name_plural = 'Centers'
        indexes = [
            models.Index(fields=['city', 'is_active']),
        ]
    
    def __str__(self):
        return self.name


class CenterFacility(models.Model):
    """
    Specific facilities available at a center.
    """
    FACILITY_CHOICES = [
        ('gym', 'Gymnasium'),
        ('pool', 'Swimming Pool'),
        ('track', 'Running Track'),
        ('court', 'Sports Court'),
        ('field', 'Athletic Field'),
        ('dojo', 'Dojo/Martial Arts'),
        ('classroom', 'Classroom'),
        ('cafeteria', 'Cafeteria'),
    ]
    
    center = models.ForeignKey(
        Center,
        on_delete=models.CASCADE,
        related_name='facilities'
    )
    facility_type = models.CharField(
        max_length=50,
        choices=FACILITY_CHOICES,
        db_index=True
    )
    description = models.TextField(blank=True)
    capacity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'center_facilities'
        unique_together = ['center', 'facility_type']
        verbose_name = 'Center Facility'
        verbose_name_plural = 'Center Facilities'
    
    def __str__(self):
        return f"{self.center.name} - {self.get_facility_type_display()}"

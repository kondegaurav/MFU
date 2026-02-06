"""
Athlete models for MFU Web Portal.
Manages athlete data, rankings, and evaluation certificates.
"""
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from apps.core.models import User
from apps.centers.models import Center
from apps.events.models import Event


class AthletePerson(models.Model):
    """
    An athlete registered in the system.
    Links to a User account (or can exist without one for minors).
    """
    user = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='athlete_profile',
        help_text="Optional: link to user account if athlete has login"
    )
    
    # Personal info
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    date_of_birth = models.DateField()
    gender = models.CharField(
        max_length=20,
        choices=[
            ('male', 'Male'),
            ('female', 'Female'),
            ('other', 'Other'),
        ]
    )
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    
    # Affiliation
    center = models.ForeignKey(
        Center,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='athletes'
    )
    
    # Medical/Health
    blood_type = models.CharField(
        max_length=5,
        choices=[
            ('A+', 'A+'), ('A-', 'A-'),
            ('B+', 'B+'), ('B-', 'B-'),
            ('AB+', 'AB+'), ('AB-', 'AB-'),
            ('O+', 'O+'), ('O-', 'O-'),
        ],
        blank=True
    )
    allergies = models.TextField(blank=True, help_text="Any known allergies")
    medical_conditions = models.TextField(blank=True, help_text="Any relevant medical conditions")
    emergency_contact_name = models.CharField(max_length=150, blank=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    registration_date = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'athlete_persons'
        ordering = ['last_name', 'first_name']
        verbose_name = 'Athlete'
        verbose_name_plural = 'Athletes'
        indexes = [
            models.Index(fields=['center', 'is_active']),
        ]
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def age(self):
        """Calculate age from date of birth."""
        today = timezone.now().date()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )


class AthleteScore(models.Model):
    """
    Stores scores/results for an athlete in an event.
    """
    athlete = models.ForeignKey(
        AthletePerson,
        on_delete=models.CASCADE,
        related_name='scores'
    )
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='athlete_scores'
    )
    
    # Score details
    score = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text="The score achieved"
    )
    score_type = models.CharField(
        max_length=50,
        choices=[
            ('points', 'Points'),
            ('time', 'Time (seconds)'),
            ('distance', 'Distance (meters)'),
            ('rank', 'Rank/Position'),
        ],
        default='points'
    )
    
    rank = models.PositiveIntegerField(blank=True, null=True, help_text="Placement/rank in event")
    notes = models.TextField(blank=True)
    
    recorded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'athlete_scores'
        unique_together = ['athlete', 'event']
        ordering = ['-recorded_at']
        verbose_name = 'Athlete Score'
        verbose_name_plural = 'Athlete Scores'
    
    def __str__(self):
        return f"{self.athlete.get_full_name()} - {self.event.name}: {self.score}"


class AthleteRanking(models.Model):
    """
    Overall ranking of an athlete based on accumulated scores.
    """
    athlete = models.OneToOneField(
        AthletePerson,
        on_delete=models.CASCADE,
        related_name='ranking'
    )
    
    category = models.CharField(
        max_length=100,
        help_text="Age group or skill category (e.g., U-12, Intermediate)"
    )
    
    total_score = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)]
    )
    rank = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        help_text="Overall rank in category"
    )
    
    events_participated = models.PositiveIntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'athlete_rankings'
        verbose_name = 'Athlete Ranking'
        verbose_name_plural = 'Athlete Rankings'
    
    def __str__(self):
        return f"{self.athlete.get_full_name()} - Rank #{self.rank} ({self.category})"


class EvaluationCertificate(models.Model):
    """
    Certificate issued to an athlete for evaluation/achievement.
    """
    athlete = models.ForeignKey(
        AthletePerson,
        on_delete=models.CASCADE,
        related_name='certificates'
    )
    event = models.ForeignKey(
        Event,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='certificates'
    )
    
    title = models.CharField(max_length=255, help_text="Certificate title (e.g., Gold Medal)")
    description = models.TextField()
    certificate_number = models.CharField(max_length=100, unique=True)
    
    issued_date = models.DateField(auto_now_add=True)
    valid_from = models.DateField(auto_now_add=True)
    valid_until = models.DateField(null=True, blank=True)
    
    issued_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='issued_certificates'
    )
    
    is_viewable_by_parents = models.BooleanField(
        default=True,
        help_text="Can parents/guardians view this certificate?"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'evaluation_certificates'
        ordering = ['-issued_date']
        verbose_name = 'Evaluation Certificate'
        verbose_name_plural = 'Evaluation Certificates'
    
    def __str__(self):
        return f"{self.athlete.get_full_name()} - {self.title}"
    
    def is_valid(self):
        """Check if certificate is currently valid."""
        today = timezone.now().date()
        if self.valid_until and today > self.valid_until:
            return False
        return today >= self.valid_from

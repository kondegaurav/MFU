"""
Coach models for MFU Web Portal.
Manages coaching, training sessions, and team management.
"""
from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from apps.core.models import User
from apps.centers.models import Center
from apps.athlete_portal.models import AthletePerson


class CoachProfile(models.Model):
    """
    Extended profile for coaches.
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='coach_profile'
    )
    
    specializations = models.CharField(
        max_length=500,
        blank=True,
        help_text="Comma-separated list (e.g., Sprint, Long Jump, Relay)"
    )
    certifications = models.TextField(blank=True, help_text="Coaching certifications")
    experience_years = models.PositiveIntegerField(
        default=0,
        help_text="Years of coaching experience"
    )
    
    center = models.ForeignKey(
        Center,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='coaches'
    )
    
    is_head_coach = models.BooleanField(
        default=False,
        help_text="Is this a head coach for the center?"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'coach_profiles'
        verbose_name = 'Coach Profile'
        verbose_name_plural = 'Coach Profiles'
    
    @property
    def has_head_coach_privileges(self):
        """Check if coach has head coach privileges via DB field OR Role Tag."""
        return self.is_head_coach or self.user.has_tag('head_coach')

    def __str__(self):
        return f"Coach: {self.user.get_full_name()}"


class TrainingSession(models.Model):
    """
    A training session conducted by a coach.
    """
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    coach = models.ForeignKey(
        CoachProfile,
        on_delete=models.SET_NULL,
        null=True,
        related_name='training_sessions'
    )
    
    center = models.ForeignKey(
        Center,
        on_delete=models.PROTECT,
        related_name='training_sessions'
    )
    
    title = models.CharField(max_length=255)
    description = models.TextField()
    
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    
    athletes = models.ManyToManyField(
        AthletePerson,
        related_name='training_sessions',
        blank=True
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='scheduled',
        db_index=True
    )
    
    notes = models.TextField(blank=True, help_text="Session notes/feedback")
    attendance = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Number of athletes who attended"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'training_sessions'
        ordering = ['-start_time']
        verbose_name = 'Training Session'
        verbose_name_plural = 'Training Sessions'
        indexes = [
            models.Index(fields=['coach', 'status']),
            models.Index(fields=['start_time', 'status']),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.start_time.strftime('%b %d, %Y')}"


class CompetitionTeam(models.Model):
    """
    A team created by a coach for competitions.
    """
    STATUS_CHOICES = [
        ('forming', 'Forming'),
        ('active', 'Active'),
        ('competing', 'Competing'),
        ('inactive', 'Inactive'),
    ]
    
    coach = models.ForeignKey(
        CoachProfile,
        on_delete=models.CASCADE,
        related_name='competition_teams'
    )
    
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    
    category = models.CharField(
        max_length=100,
        help_text="Team category (e.g., U-14, U-18)"
    )
    
    athletes = models.ManyToManyField(
        AthletePerson,
        through='TeamMember',
        related_name='teams'
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='forming',
        db_index=True
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'competition_teams'
        ordering = ['name']
        verbose_name = 'Competition Team'
        verbose_name_plural = 'Competition Teams'
    
    def __str__(self):
        return f"{self.name} ({self.category})"


class TeamMember(models.Model):
    """
    Through table for tracking team membership and roles.
    """
    ROLE_CHOICES = [
        ('athlete', 'Athlete'),
        ('alternate', 'Alternate'),
        ('reserve', 'Reserve'),
    ]
    
    team = models.ForeignKey(
        CompetitionTeam,
        on_delete=models.CASCADE
    )
    athlete = models.ForeignKey(
        AthletePerson,
        on_delete=models.CASCADE
    )
    
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='athlete'
    )
    jersey_number = models.PositiveIntegerField(null=True, blank=True)
    
    joined_at = models.DateTimeField(auto_now_add=True)
    removed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'team_members'
        unique_together = ['team', 'athlete']
        verbose_name = 'Team Member'
        verbose_name_plural = 'Team Members'
    
    def __str__(self):
        return f"{self.athlete.get_full_name()} - {self.team.name} ({self.role})"

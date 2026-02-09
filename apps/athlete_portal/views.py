from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from apps.core.decorators.permissions import require_roles
from .models import AthletePerson, AthleteRanking, EvaluationCertificate, AthleteScore
from apps.events.models import EventRegistration, Event
from apps.coach_portal.models import TrainingSession, TeamMember


@login_required
def athlete_detail(request, athlete_id):
    """
    View details of a specific athlete.
    Accessible to: the athlete themselves, coaches, admins.
    """
    user = request.user
    athlete = get_object_or_404(AthletePerson, id=athlete_id)
    
    # Permission check: only athlete themselves, coaches, or admins can view
    has_permission = (
        user == athlete.user or
        user.has_role('coach') or
        user.has_role('admin')
    )
    
    if not has_permission:
        from django.http import HttpResponseForbidden
        return HttpResponseForbidden("You don't have permission to view this profile.")
    
    # Get athlete's rankings
    rankings = AthleteRanking.objects.filter(
        athlete=athlete,
        is_active=True
    ).order_by('-total_score')
    
    # Get athlete's recent scores
    recent_scores = AthleteScore.objects.filter(
        athlete=athlete
    ).select_related('event').order_by('-recorded_at')[:10]
    
    # Get athlete's certificates
    certificates = EvaluationCertificate.objects.filter(
        athlete=athlete
    ).order_by('-issued_date')
    
    # Get athlete's team memberships
    team_memberships = TeamMember.objects.filter(
        athlete=athlete,
        removed_at__isnull=True
    ).select_related('team')
    
    context = {
        'athlete': athlete,
        'rankings': rankings,
        'recent_scores': recent_scores,
        'certificates': certificates,
        'team_memberships': team_memberships,
    }
    
    return render(request, 'athlete_portal/athlete_detail.html', context)


@login_required
@require_roles('athlete')
def athlete_dashboard(request):
    """Athlete dashboard showing personal stats and rankings."""
    user = request.user
    
    try:
        athlete = AthletePerson.objects.get(user=user)
    except AthletePerson.DoesNotExist:
        context = {'error': 'Athlete profile not found'}
        return render(request, 'athlete_portal/dashboard.html', context)
    
    # Get athlete's rankings
    rankings = AthleteRanking.objects.filter(
        athlete=athlete
    ).order_by('-total_score')
    
    # Get athlete's recent scores
    recent_scores = AthleteScore.objects.filter(
        athlete=athlete
    ).select_related('event').order_by('-recorded_at')[:10]
    
    # Get athlete's certificates
    certificates = EvaluationCertificate.objects.filter(
        athlete=athlete
    ).order_by('-issued_date')
    
    # Get athlete's team memberships
    team_memberships = TeamMember.objects.filter(
        athlete=athlete,
        removed_at__isnull=True
    ).select_related('team')
    
    # Get upcoming training sessions
    from django.utils import timezone
    today = timezone.now().date()
    
    training_sessions = TrainingSession.objects.filter(
        athletes=athlete,
        start_time__date__gte=today
    ).order_by('start_time')[:5]
    
    context = {
        'athlete': athlete,
        'rankings': rankings,
        'recent_scores': recent_scores,
        'certificates': certificates,
        'team_memberships': team_memberships,
        'upcoming_training': training_sessions,
    }
    
    return render(request, 'athlete_portal/dashboard.html', context)


@login_required
@require_roles('athlete')
def athlete_rankings(request):
    """Athlete's rankings across all categories."""
    user = request.user
    athlete = get_object_or_404(AthletePerson, user=user)
    
    rankings = AthleteRanking.objects.filter(
        athlete=athlete
    ).order_by('-total_score')
    
    context = {
        'athlete': athlete,
        'rankings': rankings,
    }
    
    return render(request, 'athlete_portal/rankings.html', context)


@login_required
@require_roles('athlete')
def athlete_scores(request):
    """Athlete's event scores."""
    user = request.user
    athlete = get_object_or_404(AthletePerson, user=user)
    
    scores = AthleteScore.objects.filter(
        athlete=athlete
    ).select_related('event').order_by('-recorded_at')
    
    context = {
        'athlete': athlete,
        'scores': scores,
    }
    
    return render(request, 'athlete_portal/scores.html', context)


@login_required
@require_roles('athlete')
def athlete_certificates(request):
    """Athlete's evaluation certificates."""
    user = request.user
    athlete = get_object_or_404(AthletePerson, user=user)
    
    certificates = EvaluationCertificate.objects.filter(
        athlete=athlete
    ).order_by('-issued_date')
    
    context = {
        'athlete': athlete,
        'certificates': certificates,
    }
    
    return render(request, 'athlete_portal/certificates.html', context)


@login_required
@require_roles('athlete')
def athlete_teams(request):
    """Athlete's team memberships."""
    user = request.user
    athlete = get_object_or_404(AthletePerson, user=user)
    
    team_memberships = TeamMember.objects.filter(
        athlete=athlete,
        removed_at__isnull=True
    ).select_related('team', 'team__coach')
    
    context = {
        'athlete': athlete,
        'team_memberships': team_memberships,
    }
    
    return render(request, 'athlete_portal/teams.html', context)


@login_required
@require_roles('athlete')
def athlete_events(request):
    """Athlete's event registrations."""
    user = request.user
    
    event_registrations = EventRegistration.objects.filter(
        participant=user
    ).select_related('event').order_by('-registered_at')
    
    context = {
        'event_registrations': event_registrations,
    }
    
    return render(request, 'athlete_portal/events.html', context)


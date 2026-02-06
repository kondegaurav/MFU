from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta

from apps.core.decorators.permissions import require_roles
from .models import CoachProfile, TrainingSession, CompetitionTeam, TeamMember
from apps.athlete_portal.models import AthletePerson, AthleteScore, AthleteRanking


@login_required
@require_roles('coach')
def coach_dashboard(request):
    """Coach dashboard showing training sessions and teams."""
    user = request.user
    
    try:
        coach = CoachProfile.objects.get(user=user)
    except CoachProfile.DoesNotExist:
        context = {'error': 'Coach profile not found'}
        return render(request, 'coach_portal/dashboard.html', context)
    
    # Get coach's teams
    if coach.is_head_coach:
        teams = CompetitionTeam.objects.filter(head_coach=coach)
    else:
        teams = CompetitionTeam.objects.filter(members__athlete__user=user).distinct()
    
    # Get coach's training sessions
    today = timezone.now().date()
    upcoming_sessions = TrainingSession.objects.filter(
        coach=coach,
        date__gte=today
    ).order_by('date', 'time')[:10]
    
    past_sessions = TrainingSession.objects.filter(
        coach=coach,
        date__lt=today
    ).order_by('-date')[:5]
    
    # Get athlete performance data
    team_ids = teams.values_list('id', flat=True)
    team_athletes = TeamMember.objects.filter(
        team_id__in=team_ids,
        is_active=True
    ).select_related('athlete').values_list('athlete_id', flat=True)
    
    athlete_rankings = AthleteRanking.objects.filter(
        athlete_id__in=team_athletes,
        is_active=True
    ).select_related('athlete').order_by('-total_score')[:10]
    
    context = {
        'coach': coach,
        'teams': teams,
        'upcoming_sessions': upcoming_sessions,
        'past_sessions': past_sessions,
        'athlete_rankings': athlete_rankings,
        'total_teams': teams.count(),
        'total_athletes': TeamMember.objects.filter(
            team__in=teams,
            is_active=True
        ).distinct('athlete').count(),
    }
    
    return render(request, 'coach_portal/dashboard.html', context)


@login_required
@require_roles('coach')
def teams_dashboard(request):
    """Coach's teams management."""
    user = request.user
    coach = get_object_or_404(CoachProfile, user=user)
    
    if coach.is_head_coach:
        teams = CompetitionTeam.objects.filter(head_coach=coach)
    else:
        teams = CompetitionTeam.objects.filter(members__athlete__user=user).distinct()
    
    context = {
        'teams': teams,
        'coach': coach,
    }
    
    return render(request, 'coach_portal/teams.html', context)


@login_required
@require_roles('coach')
def training_sessions_dashboard(request):
    """Coach's training sessions."""
    user = request.user
    coach = get_object_or_404(CoachProfile, user=user)
    
    today = timezone.now().date()
    
    # Filter by date range if provided
    date_filter = request.GET.get('filter', 'upcoming')  # upcoming, past, all
    
    if date_filter == 'upcoming':
        sessions = TrainingSession.objects.filter(
            coach=coach,
            date__gte=today
        )
    elif date_filter == 'past':
        sessions = TrainingSession.objects.filter(
            coach=coach,
            date__lt=today
        )
    else:
        sessions = TrainingSession.objects.filter(coach=coach)
    
    sessions = sessions.order_by('-date', '-time')
    
    context = {
        'sessions': sessions,
        'coach': coach,
        'selected_filter': date_filter,
    }
    
    return render(request, 'coach_portal/training_sessions.html', context)


@login_required
@require_roles('coach')
def athletes_dashboard(request):
    """Coach's athletes and their performance."""
    user = request.user
    coach = get_object_or_404(CoachProfile, user=user)
    
    # Get coach's teams
    if coach.is_head_coach:
        teams = CompetitionTeam.objects.filter(head_coach=coach)
    else:
        teams = CompetitionTeam.objects.filter(members__athlete__user=user).distinct()
    
    # Get team members
    team_ids = teams.values_list('id', flat=True)
    team_members = TeamMember.objects.filter(
        team_id__in=team_ids,
        is_active=True
    ).select_related('athlete', 'team').order_by('team', 'athlete__user__first_name')
    
    context = {
        'team_members': team_members,
        'teams': teams,
        'coach': coach,
    }
    
    return render(request, 'coach_portal/athletes.html', context)


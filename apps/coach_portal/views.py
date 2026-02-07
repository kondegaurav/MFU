from django.shortcuts import render, get_object_or_404, redirect
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
    if coach.is_head_coach and coach.center:
        teams = CompetitionTeam.objects.filter(coach__center=coach.center)
    else:
        teams = CompetitionTeam.objects.filter(coach=coach)
    
    # Get coach's training sessions
    today = timezone.now().date()
    upcoming_sessions = TrainingSession.objects.filter(
        coach=coach,
        start_time__gte=today
    ).order_by('start_time')[:10]

    past_sessions = TrainingSession.objects.filter(
        coach=coach,
        start_time__lt=today
    ).order_by('-start_time')[:5]
    
    # Get athlete performance data
    team_ids = teams.values_list('id', flat=True)
    team_athletes = TeamMember.objects.filter(
        team_id__in=team_ids,
        removed_at__isnull=True
    ).select_related('athlete').values_list('athlete_id', flat=True)
    
    athlete_rankings = AthleteRanking.objects.filter(
        athlete_id__in=team_athletes,
        athlete__is_active=True
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
            removed_at__isnull=True
        ).values_list('athlete', flat=True).distinct().count(),
    }
    
    return render(request, 'coach_portal/dashboard.html', context)


@login_required
@require_roles('coach')
def teams_dashboard(request):
    """Coach's teams management."""
    user = request.user
    coach = get_object_or_404(CoachProfile, user=user)
    
    if coach.is_head_coach and coach.center:
        teams = CompetitionTeam.objects.filter(coach__center=coach.center)
    else:
        teams = CompetitionTeam.objects.filter(coach=coach)
    
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
            start_time__gte=today
        )
    elif date_filter == 'past':
        sessions = TrainingSession.objects.filter(
            coach=coach,
            start_time__lt=today
        )
    else:
        sessions = TrainingSession.objects.filter(coach=coach)

    sessions = sessions.order_by('-start_time')
    
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
    if coach.is_head_coach and coach.center:
        teams = CompetitionTeam.objects.filter(coach__center=coach.center)
    else:
        teams = CompetitionTeam.objects.filter(coach=coach)
    
    # Get team members
    team_ids = teams.values_list('id', flat=True)
    team_members = TeamMember.objects.filter(
        team_id__in=team_ids,
        removed_at__isnull=True
    ).select_related('athlete', 'team').order_by('team', 'athlete__user__first_name')
    
    context = {
        'team_members': team_members,
        'teams': teams,
        'coach': coach,
    }
    
    return render(request, 'coach_portal/athletes.html', context)

@login_required
@require_roles('coach')
def create_training_session(request):
    """Create a new training session."""
    user = request.user
    coach = get_object_or_404(CoachProfile, user=user)
    
    from .forms import TrainingSessionForm

    if request.method == 'POST':
        form = TrainingSessionForm(request.POST)
        if form.is_valid():
            session = form.save(commit=False)
            session.coach = coach
            if not session.center:
                session.center = coach.center
            session.save()
            return redirect('coach_portal:training_sessions')
    else:
        # Default to coach's center
        initial_data = {}
        if coach.center:
            initial_data['center'] = coach.center
        form = TrainingSessionForm(initial=initial_data)

    context = {
        'form': form,
        'coach': coach,
        'title': 'Create Training Session'
    }
    return render(request, 'coach_portal/training_session_form.html', context)
@login_required
@require_roles('coach')
def team_detail(request, team_id):
    """View team details and members."""
    user = request.user
    coach = get_object_or_404(CoachProfile, user=user)
    
    # Get team, ensuring coach has access
    if coach.is_head_coach and coach.center:
        team = get_object_or_404(CompetitionTeam, id=team_id, coach__center=coach.center)
    else:
        team = get_object_or_404(CompetitionTeam, id=team_id, coach=coach)
    
    # Get active team members
    members = TeamMember.objects.filter(
        team=team,
        removed_at__isnull=True
    ).select_related('athlete', 'athlete__user')
    
    context = {
        'team': team,
        'members': members,
        'coach': coach,
    }
    return render(request, 'coach_portal/team_detail.html', context)

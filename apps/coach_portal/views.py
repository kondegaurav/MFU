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
    # Get coach's teams
    if coach.has_head_coach_privileges and coach.center:
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
    
    if coach.has_head_coach_privileges and coach.center:
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
    if coach.has_head_coach_privileges and coach.center:
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
    if coach.has_head_coach_privileges and coach.center:
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


@login_required
@require_roles('coach')
def create_team(request):
    """Create a new competition team (Head Coach only)."""
    user = request.user
    coach = get_object_or_404(CoachProfile, user=user)
    
    # Check head coach status
    if not coach.has_head_coach_privileges:
        # Ideally handle this better, but for now redirect
        return redirect('coach_portal:teams')

    from .forms import CompetitionTeamForm

    if request.method == 'POST':
        form = CompetitionTeamForm(request.POST)
        if form.is_valid():
            team = form.save(commit=False)
            team.coach = coach
            team.save()
            return redirect('coach_portal:teams')
    else:
        form = CompetitionTeamForm()

    context = {
        'form': form,
        'coach': coach,
        'title': 'Create Competition Team'
    }
    return render(request, 'coach_portal/team_form.html', context)


@login_required
@require_roles('coach')
def add_team_member(request, team_id):
    """Add an athlete to the team (Head Coach only)."""
    user = request.user
    coach = get_object_or_404(CoachProfile, user=user)
    
    if not coach.has_head_coach_privileges:
        return redirect('coach_portal:team_detail', team_id=team_id)

    # Get team, ensuring coach has access
    if coach.center:
        team = get_object_or_404(CompetitionTeam, id=team_id, coach__center=coach.center)
    else:
        team = get_object_or_404(CompetitionTeam, id=team_id, coach=coach)

    # Get available athletes (in center, not currently active in team)
    # We want athletes who are NOT currently in the team (removed_at is null)
    current_member_ids = TeamMember.objects.filter(
        team=team, 
        removed_at__isnull=True
    ).values_list('athlete_id', flat=True)
    
    if coach.center:
        available_athletes = AthletePerson.objects.filter(
            center=coach.center,
            is_active=True
        ).exclude(id__in=current_member_ids).order_by('last_name', 'first_name')
    else:
        available_athletes = []

    context = {
        'team': team,
        'available_athletes': available_athletes,
        'coach': coach
    }

    if request.method == 'POST':
        athlete_id = request.POST.get('athlete')
        if athlete_id:
            try:
                athlete = AthletePerson.objects.get(id=athlete_id)
            except AthletePerson.DoesNotExist:
                context['error'] = 'Selected athlete not found.'
                return render(request, 'coach_portal/add_team_member.html', context)
            
            # Verify athlete belongs to same center
            if coach.center and athlete.center != coach.center:
                # Should not happen if filtered correctly, but good for security
                context['error'] = 'Selected athlete does not belong to your center.'
                return render(request, 'coach_portal/add_team_member.html', context)
            
            # Check if already a member (including removed ones?)
            # If previously removed, we might want to un-remove them
            existing_member = TeamMember.objects.filter(team=team, athlete=athlete).first()
            if existing_member:
                existing_member.removed_at = None
                existing_member.save()
            else:
                TeamMember.objects.create(team=team, athlete=athlete)
            return redirect('coach_portal:team_detail', team_id=team_id)
        else:
            context['error'] = 'Please select an athlete to add.'

    return render(request, 'coach_portal/add_team_member.html', context)


@login_required
@require_roles('coach')
def remove_team_member(request, team_id, member_id):
    """Remove an athlete from the team (Head Coach only)."""
    user = request.user
    coach = get_object_or_404(CoachProfile, user=user)
    
    if not coach.has_head_coach_privileges:
        return redirect('coach_portal:team_detail', team_id=team_id)

    if coach.center:
        team = get_object_or_404(CompetitionTeam, id=team_id, coach__center=coach.center)
    else:
        team = get_object_or_404(CompetitionTeam, id=team_id, coach=coach)

    member = get_object_or_404(TeamMember, id=member_id, team=team)
    member.removed_at = timezone.now()
    member.save()
    
    return redirect('coach_portal:team_detail', team_id=team_id)

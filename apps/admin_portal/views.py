from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta

from apps.core.services.permission_service import PermissionService
from apps.core.decorators.permissions import require_roles
from apps.centers.models import Center
from apps.events.models import Event, EventRegistration
from apps.athlete_portal.models import AthletePerson, AthleteRanking
from apps.coach_portal.models import CoachProfile, TrainingSession
from apps.parent_portal.models import Parent
from apps.volunteering.models import VolunteeringOpportunity, VolunteerApplication
from apps.finance_portal.models import FinancialTransaction


@login_required
@require_roles(['admin'])
def admin_dashboard(request):
    """Admin dashboard with overall statistics and recent activity."""
    user = request.user
    
    # Statistics
    stats = {
        'total_centers': Center.objects.count(),
        'active_centers': Center.objects.filter(is_active=True).count(),
        'total_events': Event.objects.count(),
        'ongoing_events': Event.objects.filter(status='ongoing').count(),
        'total_athletes': AthletePerson.objects.count(),
        'active_athletes': AthletePerson.objects.filter(is_active=True).count(),
        'total_coaches': CoachProfile.objects.count(),
        'total_parents': Parent.objects.count(),
        'pending_volunteers': VolunteerApplication.objects.filter(status='pending').count(),
    }
    
    # Recent Events
    recent_events = Event.objects.select_related('center').order_by('-created_at')[:5]
    
    # Recent Registrations
    recent_registrations = EventRegistration.objects.select_related(
        'event', 'participant'
    ).order_by('-registered_at')[:5]
    
    # Recent Financial Transactions
    recent_transactions = FinancialTransaction.objects.order_by('-transaction_date')[:5]
    
    # Upcoming Events (next 7 days)
    today = timezone.now().date()
    upcoming_events = Event.objects.filter(
        start_date__gte=today,
        start_date__lte=today + timedelta(days=7)
    ).order_by('start_date')
    
    # Pending Volunteer Applications
    pending_volunteers = VolunteerApplication.objects.filter(
        status='pending'
    ).select_related('opportunity', 'volunteer')[:5]
    
    context = {
        'stats': stats,
        'recent_events': recent_events,
        'recent_registrations': recent_registrations,
        'recent_transactions': recent_transactions,
        'upcoming_events': upcoming_events,
        'pending_volunteers': pending_volunteers,
    }
    
    return render(request, 'admin_portal/dashboard.html', context)


@login_required
@require_roles(['admin'])
def centers_dashboard(request):
    """Centers management dashboard."""
    centers = Center.objects.annotate(
        facility_count=Count('centerfacility'),
        event_count=Count('event')
    ).order_by('-created_at')
    
    context = {
        'centers': centers,
        'total_centers': centers.count(),
        'active_centers': centers.filter(is_active=True).count(),
    }
    
    return render(request, 'admin_portal/centers_dashboard.html', context)


@login_required
@require_roles(['admin'])
def events_dashboard(request):
    """Events management dashboard."""
    events = Event.objects.select_related('center').annotate(
        registration_count=Count('eventregistration')
    ).order_by('-created_at')
    
    status_filter = request.GET.get('status')
    if status_filter:
        events = events.filter(status=status_filter)
    
    context = {
        'events': events,
        'total_events': Event.objects.count(),
        'status_counts': {
            'draft': Event.objects.filter(status='draft').count(),
            'published': Event.objects.filter(status='published').count(),
            'ongoing': Event.objects.filter(status='ongoing').count(),
            'completed': Event.objects.filter(status='completed').count(),
        },
        'selected_status': status_filter,
    }
    
    return render(request, 'admin_portal/events_dashboard.html', context)


@login_required
@require_roles(['admin'])
def users_dashboard(request):
    """User management dashboard."""
    athletes = AthletePerson.objects.select_related('user').order_by('-user__date_joined')
    coaches = CoachProfile.objects.select_related('user').order_by('-user__date_joined')
    parents = Parent.objects.select_related('user').order_by('-user__date_joined')
    
    context = {
        'athletes': athletes[:10],
        'coaches': coaches[:10],
        'parents': parents[:10],
        'total_athletes': athletes.count(),
        'total_coaches': coaches.count(),
        'total_parents': parents.count(),
    }
    
    return render(request, 'admin_portal/users_dashboard.html', context)


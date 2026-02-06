from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from apps.core.decorators.permissions import require_roles
from .models import Parent, ParentChildRelation
from apps.athlete_portal.models import AthletePerson, AthleteRanking, EvaluationCertificate, AthleteScore
from apps.events.models import EventRegistration


@login_required
@require_roles('parent')
def parent_dashboard(request):
    """Parent dashboard showing children and their information."""
    user = request.user
    
    try:
        parent = Parent.objects.get(user=user)
    except Parent.DoesNotExist:
        context = {'error': 'Parent profile not found'}
        return render(request, 'parent_portal/dashboard.html', context)
    
    # Get parent's children with permissions
    children_relations = ParentChildRelation.objects.filter(
        parent=parent
    ).select_related('child')
    
    children_data = []
    for relation in children_relations:
        child = relation.child
        child_info = {
            'relation': relation,
            'child': child,
            'age': child.age,
            'can_view_scores': relation.can_view_scores,
            'can_view_rankings': relation.can_view_rankings and child.age >= 12,
            'can_view_certificates': relation.can_view_certificates,
        }
        children_data.append(child_info)
    
    context = {
        'parent': parent,
        'children_data': children_data,
        'total_children': len(children_data),
    }
    
    return render(request, 'parent_portal/dashboard.html', context)


@login_required
@require_roles('parent')
def child_details(request, child_id):
    """View details of a specific child."""
    user = request.user
    parent = get_object_or_404(Parent, user=user)
    
    # Verify parent-child relationship
    relation = get_object_or_404(ParentChildRelation, parent=parent, child_id=child_id)
    child = relation.child
    
    # Get child's rankings (if parent has permission and child is 12+)
    rankings = None
    if relation.can_view_rankings and child.age >= 12:
        rankings = AthleteRanking.objects.filter(
            athlete=child,
            is_active=True
        ).order_by('-total_score')
    
    # Get child's certificates (if parent has permission)
    certificates = None
    if relation.can_view_certificates:
        certificates = EvaluationCertificate.objects.filter(
            athlete=child,
            is_viewable_by_parents=True
        ).order_by('-issued_date')
    
    # Get child's recent scores (if parent has permission)
    recent_scores = None
    if relation.can_view_scores:
        recent_scores = AthleteScore.objects.filter(
            athlete=child
        ).select_related('event').order_by('-scored_date')[:10]
    
    # Get child's event registrations (if parent has permission)
    event_registrations = None
    if relation.can_view_events:
        event_registrations = EventRegistration.objects.filter(
            participant=child.user
        ).select_related('event').order_by('-registration_date')[:10]
    
    context = {
        'parent': parent,
        'child': child,
        'relation': relation,
        'rankings': rankings,
        'certificates': certificates,
        'recent_scores': recent_scores,
        'event_registrations': event_registrations,
    }
    
    return render(request, 'parent_portal/child_details.html', context)


@login_required
@require_roles('parent')
def child_rankings(request, child_id):
    """View child's rankings."""
    user = request.user
    parent = get_object_or_404(Parent, user=user)
    
    relation = get_object_or_404(ParentChildRelation, parent=parent, child_id=child_id)
    
    # Check permissions
    if not relation.can_view_rankings or relation.child.age < 12:
        context = {'error': 'You do not have permission to view this child\'s rankings'}
        return render(request, 'parent_portal/child_rankings.html', context)
    
    child = relation.child
    rankings = AthleteRanking.objects.filter(
        athlete=child
    ).order_by('-total_score')
    
    context = {
        'parent': parent,
        'child': child,
        'rankings': rankings,
    }
    
    return render(request, 'parent_portal/child_rankings.html', context)


@login_required
@require_roles('parent')
def child_certificates(request, child_id):
    """View child's certificates."""
    user = request.user
    parent = get_object_or_404(Parent, user=user)
    
    relation = get_object_or_404(ParentChildRelation, parent=parent, child_id=child_id)
    
    if not relation.can_view_certificates:
        context = {'error': 'You do not have permission to view this child\'s certificates'}
        return render(request, 'parent_portal/child_certificates.html', context)
    
    child = relation.child
    certificates = EvaluationCertificate.objects.filter(
        athlete=child,
        is_viewable_by_parents=True
    ).order_by('-issued_date')
    
    context = {
        'parent': parent,
        'child': child,
        'certificates': certificates,
    }
    
    return render(request, 'parent_portal/child_certificates.html', context)


"""
Views for user profiles.
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def profile_dashboard(request):
    """
    User profile dashboard - always visible to all logged-in users.
    """
    user = request.user
    roles = user.get_active_roles()
    tags = user.get_active_tags()

    context = {
        'user': user,
        'roles': roles,
        'tags': tags,
    }
    return render(request, 'profiles/dashboard.html', context)

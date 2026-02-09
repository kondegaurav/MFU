"""URLs for coach portal app."""
from django.urls import path
from . import views

app_name = 'coach_portal'

urlpatterns = [
    path('dashboard/', views.coach_dashboard, name='dashboard'),
    path('teams/', views.teams_dashboard, name='teams'),
    path('teams/create/', views.create_team, name='create_team'),
    path('teams/<int:team_id>/', views.team_detail, name='team_detail'),
    path('teams/<int:team_id>/add-member/', views.add_team_member, name='add_team_member'),
    path('teams/<int:team_id>/remove-member/<int:member_id>/', views.remove_team_member, name='remove_team_member'),
    path('training-sessions/', views.training_sessions_dashboard, name='training_sessions'),
    path('training-sessions/create/', views.create_training_session, name='create_training_session'),
    path('athletes/', views.athletes_dashboard, name='athletes'),
]

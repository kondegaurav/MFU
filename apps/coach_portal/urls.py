"""URLs for coach portal app."""
from django.urls import path
from . import views

app_name = 'coach_portal'

urlpatterns = [
    path('dashboard/', views.coach_dashboard, name='dashboard'),
    path('teams/', views.teams_dashboard, name='teams'),
    path('training-sessions/', views.training_sessions_dashboard, name='training_sessions'),
    path('athletes/', views.athletes_dashboard, name='athletes'),
]

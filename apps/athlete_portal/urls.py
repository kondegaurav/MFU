"""URLs for athlete portal app."""
from django.urls import path
from . import views

app_name = 'athlete_portal'

urlpatterns = [
    path('dashboard/', views.athlete_dashboard, name='dashboard'),
    path('rankings/', views.athlete_rankings, name='rankings'),
    path('scores/', views.athlete_scores, name='scores'),
    path('certificates/', views.athlete_certificates, name='certificates'),
    path('teams/', views.athlete_teams, name='teams'),
    path('events/', views.athlete_events, name='events'),
]

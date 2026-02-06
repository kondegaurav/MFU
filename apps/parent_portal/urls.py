"""URLs for parent portal app."""
from django.urls import path
from . import views

app_name = 'parent_portal'

urlpatterns = [
    path('dashboard/', views.parent_dashboard, name='dashboard'),
    path('child/<int:child_id>/', views.child_details, name='child_details'),
    path('child/<int:child_id>/rankings/', views.child_rankings, name='child_rankings'),
    path('child/<int:child_id>/certificates/', views.child_certificates, name='child_certificates'),
]

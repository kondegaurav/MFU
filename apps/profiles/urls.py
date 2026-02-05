"""
URLs for profiles app.
"""
from django.urls import path
from . import views

app_name = 'profiles'

urlpatterns = [
    # User Profile Dashboard (always visible)
    path('dashboard/', views.profile_dashboard, name='dashboard'),
]

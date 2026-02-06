"""URLs for admin portal app."""
from django.urls import path
from . import views

app_name = 'admin_portal'

urlpatterns = [
    path('dashboard/', views.admin_dashboard, name='dashboard'),
    path('centers/', views.centers_dashboard, name='centers'),
    path('events/', views.events_dashboard, name='events'),
    path('users/', views.users_dashboard, name='users'),
]

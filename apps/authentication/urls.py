"""
URLs for authentication app.
"""
from django.urls import path
from . import views

app_name = 'authentication'

urlpatterns = [
    # Home page redirects to login
    path('', views.home_redirect, name='home'),

    # Custom login page (combines manual + OAuth)
    path('login/', views.custom_login, name='login'),

    # Registration
    path('register/', views.custom_register, name='register'),

    # Password reset
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset-password/<uidb64>/<token>/', views.reset_password, name='reset_password'),

    # Email confirmation success
    path('email-confirmation-sent/', views.email_confirmation_sent, name='email_confirmation_sent'),

    # Custom logout
    path('logout/', views.custom_logout, name='logout'),
]

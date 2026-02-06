"""URLs for finance portal app."""
from django.urls import path
from . import views

app_name = 'finance_portal'

urlpatterns = [
    path('dashboard/', views.finance_dashboard, name='dashboard'),
    path('equipment/', views.equipment_inventory, name='equipment_inventory'),
    path('equipment-requests/', views.equipment_requests, name='equipment_requests'),
    path('transactions/', views.transactions_list, name='transactions_list'),
]

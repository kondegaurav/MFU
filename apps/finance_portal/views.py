from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Q, Count, IntegerField, Value
from django.db.models.functions import Cast
from decimal import Decimal

from apps.core.decorators.permissions import require_roles
from .models import Equipment, EquipmentRequest, FinancialTransaction


@login_required
@require_roles('admin', 'finance_officer')
def finance_dashboard(request):
    """Finance dashboard with financial statistics and transactions."""
    
    # Financial statistics
    all_transactions = FinancialTransaction.objects.all()
    
    income_transactions = all_transactions.filter(
        Q(transaction_type='event_fee') |
        Q(transaction_type='registration_fee') |
        Q(transaction_type='donation')
    )
    
    expense_transactions = all_transactions.filter(
        Q(transaction_type='salary') |
        Q(transaction_type='equipment_purchase') |
        Q(transaction_type='maintenance') |
        Q(transaction_type='utility') |
        Q(transaction_type='other')
    )
    
    total_income = income_transactions.aggregate(Sum('amount'))['amount__sum'] or Decimal('0')
    total_expenses = expense_transactions.aggregate(Sum('amount'))['amount__sum'] or Decimal('0')
    net_balance = total_income - total_expenses
    
    # Recent transactions
    recent_transactions = FinancialTransaction.objects.order_by('-transaction_date')[:10]
    
    # Transaction breakdown by type
    transaction_types = FinancialTransaction.objects.values('transaction_type').annotate(
        count=Sum('amount')
    )
    
    # Pending transactions
    pending_transactions = FinancialTransaction.objects.filter(
        status='pending'
    ).order_by('-transaction_date')
    
    context = {
        'total_income': total_income,
        'total_expenses': total_expenses,
        'net_balance': net_balance,
        'recent_transactions': recent_transactions,
        'transaction_types': transaction_types,
        'pending_transactions': pending_transactions,
        'total_transactions': all_transactions.count(),
        'completed_transactions': all_transactions.filter(status='completed').count(),
    }
    
    return render(request, 'finance_portal/dashboard.html', context)


@login_required
@require_roles('admin', 'finance_officer')
def equipment_inventory(request):
    """Equipment inventory management."""
    equipment_list = Equipment.objects.all()
    
    # Filter by status if provided
    status_filter = request.GET.get('status')
    if status_filter:
        equipment_list = equipment_list.filter(status=status_filter)
    
    # Filter by condition if provided
    condition_filter = request.GET.get('condition')
    if condition_filter:
        equipment_list = equipment_list.filter(condition=condition_filter)
    
    # Get equipment statistics
    stats = {
        'total_equipment': Equipment.objects.count(),
        'available': Equipment.objects.filter(status='available').count(),
        'in_use': Equipment.objects.filter(status='in_use').count(),
        'maintenance': Equipment.objects.filter(status='maintenance').count(),
        'damaged': Equipment.objects.filter(condition='damaged').count(),
        'excellent': Equipment.objects.filter(condition='excellent').count(),
        'good': Equipment.objects.filter(condition='good').count(),
        'fair': Equipment.objects.filter(condition='fair').count(),
    }
    
    context = {
        'equipment_list': equipment_list,
        'stats': stats,
        'selected_status': status_filter,
        'selected_condition': condition_filter,
    }
    
    return render(request, 'finance_portal/equipment_inventory.html', context)


@login_required
@require_roles('admin', 'finance_officer')
def equipment_requests(request):
    """Equipment request tracking."""
    requests_list = EquipmentRequest.objects.select_related('equipment', 'requested_by')
    
    # Filter by status if provided
    status_filter = request.GET.get('status')
    if status_filter:
        requests_list = requests_list.filter(status=status_filter)
    
    # Filter by type if provided
    type_filter = request.GET.get('type')
    if type_filter:
        requests_list = requests_list.filter(request_type=type_filter)
    
    requests_list = requests_list.order_by('-requested_date')
    
    context = {
        'requests_list': requests_list,
        'total_requests': EquipmentRequest.objects.count(),
        'pending_requests': EquipmentRequest.objects.filter(status='pending').count(),
        'selected_status': status_filter,
        'selected_type': type_filter,
    }
    
    return render(request, 'finance_portal/equipment_requests.html', context)


@login_required
@require_roles('admin', 'finance_officer')
def transactions_list(request):
    """Financial transactions list."""
    transactions = FinancialTransaction.objects.all()
    
    # Filter by status if provided
    status_filter = request.GET.get('status')
    if status_filter:
        transactions = transactions.filter(status=status_filter)
    
    # Filter by type if provided
    type_filter = request.GET.get('type')
    if type_filter:
        transactions = transactions.filter(transaction_type=type_filter)
    
    # Filter by payment method if provided
    method_filter = request.GET.get('method')
    if method_filter:
        transactions = transactions.filter(payment_method=method_filter)
    
    transactions = transactions.order_by('-transaction_date')
    
    # Statistics by type
    type_stats = FinancialTransaction.objects.values('transaction_type').annotate(
        total=Sum('amount'),
        count=Count('id'),
    )
    
    context = {
        'transactions': transactions,
        'total_transactions': FinancialTransaction.objects.count(),
        'selected_status': status_filter,
        'selected_type': type_filter,
        'selected_method': method_filter,
        'type_stats': type_stats,
    }
    
    return render(request, 'finance_portal/transactions_list.html', context)



"""
Finance & Inventory models for MFU Web Portal.
Manages financial transactions, inventory, and equipment.
"""
from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from apps.core.models import User
from apps.centers.models import Center
from apps.events.models import Event


class Equipment(models.Model):
    """
    Sports equipment inventory item.
    """
    CONDITION_CHOICES = [
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('damaged', 'Damaged'),
        ('unusable', 'Unusable'),
    ]
    
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('in_use', 'In Use'),
        ('maintenance', 'Under Maintenance'),
        ('retired', 'Retired'),
    ]
    
    center = models.ForeignKey(
        Center,
        on_delete=models.CASCADE,
        related_name='equipment'
    )
    
    equipment_type = models.CharField(
        max_length=100,
        help_text="Type of equipment (e.g., Javelin, Shot Put, Stopwatch)",
        db_index=True
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    
    # Inventory details
    equipment_code = models.CharField(
        max_length=50,
        unique=True,
        help_text="Unique identifier for this item"
    )
    quantity = models.PositiveIntegerField(default=1)
    purchase_date = models.DateField()
    purchase_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    
    # Condition and Status
    condition = models.CharField(
        max_length=20,
        choices=CONDITION_CHOICES,
        default='good'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='available',
        db_index=True
    )
    
    last_maintenance_date = models.DateField(null=True, blank=True)
    next_maintenance_date = models.DateField(null=True, blank=True)
    
    # Additional info
    supplier = models.CharField(max_length=255, blank=True)
    warranty_expires = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'equipment'
        ordering = ['equipment_type', 'name']
        verbose_name = 'Equipment'
        verbose_name_plural = 'Equipment'
        indexes = [
            models.Index(fields=['center', 'status']),
            models.Index(fields=['equipment_type', 'status']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.equipment_code})"
    
    def needs_maintenance(self):
        """Check if equipment needs maintenance."""
        if self.next_maintenance_date is None:
            return False
        return timezone.now().date() >= self.next_maintenance_date


class EquipmentRequest(models.Model):
    """
    Request to use or maintain equipment.
    """
    REQUEST_TYPE_CHOICES = [
        ('use', 'Usage Request'),
        ('maintenance', 'Maintenance Request'),
        ('repair', 'Repair Request'),
        ('return', 'Return Request'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    
    equipment = models.ForeignKey(
        Equipment,
        on_delete=models.CASCADE,
        related_name='requests'
    )
    
    request_type = models.CharField(
        max_length=20,
        choices=REQUEST_TYPE_CHOICES,
        default='use'
    )
    
    requested_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='equipment_requests'
    )
    
    request_date = models.DateTimeField(auto_now_add=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    
    purpose = models.TextField(help_text="Purpose of the request")
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        db_index=True
    )
    
    approved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_equipment_requests'
    )
    approval_notes = models.TextField(blank=True)
    
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'equipment_requests'
        ordering = ['-request_date']
        verbose_name = 'Equipment Request'
        verbose_name_plural = 'Equipment Requests'
    
    def __str__(self):
        return f"{self.requested_by.get_full_name()} - {self.equipment.name}"


class FinancialTransaction(models.Model):
    """
    Financial transactions (fees, payments, expenses).
    """
    TRANSACTION_TYPE_CHOICES = [
        ('event_fee', 'Event Registration Fee'),
        ('membership_fee', 'Membership Fee'),
        ('training_fee', 'Training Fee'),
        ('other_income', 'Other Income'),
        ('equipment_purchase', 'Equipment Purchase'),
        ('maintenance', 'Maintenance Expense'),
        ('staff_salary', 'Staff Salary'),
        ('utility', 'Utility Expense'),
        ('other_expense', 'Other Expense'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    transaction_id = models.CharField(
        max_length=50,
        unique=True,
        help_text="Unique transaction reference"
    )
    
    center = models.ForeignKey(
        Center,
        on_delete=models.PROTECT,
        related_name='financial_transactions'
    )
    
    transaction_type = models.CharField(
        max_length=50,
        choices=TRANSACTION_TYPE_CHOICES,
        db_index=True
    )
    
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    
    # For income transactions
    payer = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='paid_transactions'
    )
    event = models.ForeignKey(
        Event,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='financial_transactions'
    )
    
    # For expense transactions
    payee = models.CharField(max_length=255, blank=True, help_text="Who/what was paid")
    
    description = models.TextField()
    payment_method = models.CharField(
        max_length=50,
        choices=[
            ('cash', 'Cash'),
            ('check', 'Check'),
            ('card', 'Credit/Debit Card'),
            ('bank_transfer', 'Bank Transfer'),
            ('online', 'Online Payment'),
            ('other', 'Other'),
        ],
        default='online'
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    
    recorded_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='recorded_transactions'
    )
    
    transaction_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'financial_transactions'
        ordering = ['-transaction_date']
        verbose_name = 'Financial Transaction'
        verbose_name_plural = 'Financial Transactions'
        indexes = [
            models.Index(fields=['center', 'transaction_date']),
            models.Index(fields=['transaction_type', 'status']),
        ]
    
    def __str__(self):
        return f"{self.transaction_id} - {self.get_transaction_type_display()}: {self.amount}"

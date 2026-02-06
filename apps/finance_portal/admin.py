from django.contrib import admin
from .models import Equipment, EquipmentRequest, FinancialTransaction


class EquipmentRequestInline(admin.TabularInline):
    model = EquipmentRequest
    extra = 0
    fields = ('equipment', 'request_date', 'request_type', 'status')
    readonly_fields = ('request_date',)


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('equipment_code', 'name', 'condition', 'status', 'center')
    list_filter = ('condition', 'status', 'center')
    search_fields = ('equipment_code', 'name', 'center__name')
    inlines = [EquipmentRequestInline]
    fieldsets = (
        ('Basic Information', {
            'fields': ('equipment_code', 'name', 'description', 'equipment_type')
        }),
        ('Specifications', {
            'fields': ('brand', 'model', 'serial_number')
        }),
        ('Location', {
            'fields': ('center',)
        }),
        ('Condition & Maintenance', {
            'fields': ('condition', 'status')
        }),
    )
    readonly_fields = ('equipment_code',)


@admin.register(EquipmentRequest)
class EquipmentRequestAdmin(admin.ModelAdmin):
    list_display = ('equipment', 'request_date', 'request_type', 'status')
    list_filter = ('request_type', 'status')
    search_fields = ('equipment__name', 'created_by__first_name')
    readonly_fields = ('request_date',)


@admin.register(FinancialTransaction)
class FinancialTransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'amount', 'transaction_type', 'transaction_date', 'status')
    list_filter = ('transaction_type', 'status', 'transaction_date', 'payment_method')
    search_fields = ('transaction_id', 'description', 'related_to')
    readonly_fields = ('transaction_id', 'transaction_date')
    fieldsets = (
        ('Basic Information', {
            'fields': ('transaction_id', 'transaction_type', 'amount', 'transaction_date')
        }),
        ('Details', {
            'fields': ('description', 'related_to', 'reference_number')
        }),
        ('Payment Information', {
            'fields': ('payment_method', 'payment_status', 'paid_by')
        }),
        ('Status', {
            'fields': ('status', 'notes')
        }),
    )


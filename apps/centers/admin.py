from django.contrib import admin
from .models import Center, CenterFacility


@admin.register(Center)
class CenterAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'center_head', 'total_capacity', 'is_active', 'created_at')
    list_filter = ('city', 'is_active', 'created_at')
    search_fields = ('name', 'city', 'email')
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'center_head')
        }),
        ('Address', {
            'fields': ('address', 'city', 'state', 'postal_code', 'country')
        }),
        ('Contact & Web', {
            'fields': ('phone', 'email', 'website')
        }),
        ('Facilities', {
            'fields': ('total_capacity', 'has_indoor_facility', 'has_outdoor_facility', 'has_parking', 'has_food_court')
        }),
        ('Location', {
            'fields': ('latitude', 'longitude'),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )
    readonly_fields = ('created_at', 'updated_at')


@admin.register(CenterFacility)
class CenterFacilityAdmin(admin.ModelAdmin):
    list_display = ('center', 'facility_type', 'capacity', 'is_available')
    list_filter = ('facility_type', 'is_available', 'center')
    search_fields = ('center__name', 'facility_type')

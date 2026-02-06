from django.contrib import admin
from .models import Event, EventRegistration


class EventRegistrationInline(admin.TabularInline):
    model = EventRegistration
    extra = 0
    readonly_fields = ('registered_at',)
    fields = ('participant', 'registered_at', 'status', 'payment_status')


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'center', 'start_date', 'status', 'current_participants', 'max_participants')
    list_filter = ('status', 'start_date', 'center', 'event_type')
    search_fields = ('name', 'description', 'center__name')
    readonly_fields = ('created_at', 'updated_at', 'current_participants')
    inlines = [EventRegistrationInline]
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'center', 'event_type')
        }),
        ('Dates & Times', {
            'fields': ('start_date', 'end_date', 'registration_start', 'registration_end')
        }),
        ('Details', {
            'fields': ('status', 'max_participants', 'current_participants')
        }),
        ('Management', {
            'fields': ('created_by', 'organizers', 'entry_fee', 'is_featured')
        }),
        ('Created', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ('participant', 'event', 'registered_at', 'status', 'payment_status')
    list_filter = ('status', 'payment_status', 'event')
    search_fields = ('participant__first_name', 'event__name')
    readonly_fields = ('registered_at', 'updated_at')

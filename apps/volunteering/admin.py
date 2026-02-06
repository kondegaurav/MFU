from django.contrib import admin
from .models import VolunteeringOpportunity, VolunteerApplication


class VolunteerApplicationInline(admin.TabularInline):
    model = VolunteerApplication
    extra = 0
    fields = ('volunteer', 'applied_at', 'status')
    readonly_fields = ('applied_at',)


@admin.register(VolunteeringOpportunity)
class VolunteeringOpportunityAdmin(admin.ModelAdmin):
    list_display = ('title', 'center', 'required_hours', 'status', 'total_volunteers')
    list_filter = ('status', 'center')
    search_fields = ('title', 'description', 'center__name')
    inlines = [VolunteerApplicationInline]
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'center', 'opportunity_type')
        }),
        ('Requirements', {
            'fields': ('required_hours', 'required_skills', 'max_volunteers', 'min_age')
        }),
        ('Dates & Times', {
            'fields': ('start_date', 'end_date')
        }),
        ('Status', {
            'fields': ('status',)
        }),
    )
    
    def total_volunteers(self, obj):
        return obj.applications.filter(status='approved').count()
    total_volunteers.short_description = 'Approved Volunteers'


@admin.register(VolunteerApplication)
class VolunteerApplicationAdmin(admin.ModelAdmin):
    list_display = ('volunteer', 'opportunity', 'applied_at', 'status')
    list_filter = ('status', 'opportunity')
    search_fields = ('volunteer__first_name', 'opportunity__title')
    readonly_fields = ('applied_at',)
    fieldsets = (
        ('Application Information', {
            'fields': ('volunteer', 'opportunity', 'applied_at')
        }),
        ('Status', {
            'fields': ('status',)
        }),
    )


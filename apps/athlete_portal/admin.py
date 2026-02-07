from django.contrib import admin
from .models import AthletePerson, AthleteScore, AthleteRanking, EvaluationCertificate


class AthleteScoreInline(admin.TabularInline):
    model = AthleteScore
    extra = 0
    fields = ('event', 'score', 'rank', 'recorded_at')
    readonly_fields = ('recorded_at',)


class AthleteRankingInline(admin.TabularInline):
    model = AthleteRanking
    extra = 0
    readonly_fields = ('last_updated',)


class EvaluationCertificateInline(admin.TabularInline):
    model = EvaluationCertificate
    extra = 0
    fields = ('title', 'issued_by', 'is_viewable_by_parents', 'valid_until')
    readonly_fields = ('issued_date', 'valid_from')


@admin.register(AthletePerson)
class AthletePersonAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'email', 'date_of_birth', 'blood_type', 'is_active')
    list_filter = ('is_active', 'date_of_birth', 'blood_type', 'center')
    search_fields = ('first_name', 'last_name', 'email')
    inlines = [AthleteScoreInline, AthleteRankingInline, EvaluationCertificateInline]
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'first_name', 'last_name', 'email', 'phone')
        }),
        ('Personal Information', {
            'fields': ('date_of_birth', 'gender')
        }),
        ('Medical Information', {
            'fields': ('blood_type', 'allergies', 'medical_conditions')
        }),
        ('Contact Information', {
            'fields': ('emergency_contact_name', 'emergency_contact_phone')
        }),
        ('Affiliation', {
            'fields': ('center',)
        }),
        ('Status', {
            'fields': ('is_active', 'registration_date'),
        }),
    )
    readonly_fields = ('registration_date', 'created_at', 'updated_at')
    
    def get_full_name(self, obj):
        return obj.get_full_name()
    get_full_name.short_description = 'Athlete'


@admin.register(AthleteScore)
class AthleteScoreAdmin(admin.ModelAdmin):
    list_display = ('athlete', 'event', 'score', 'rank', 'recorded_at')
    list_filter = ('event', 'recorded_at', 'score_type')
    search_fields = ('athlete__first_name', 'event__name')
    readonly_fields = ('recorded_at', 'updated_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('athlete', 'event', 'score', 'score_type')
        }),
        ('Details', {
            'fields': ('rank', 'notes')
        }),
        ('Timestamps', {
            'fields': ('recorded_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(AthleteRanking)
class AthleteRankingAdmin(admin.ModelAdmin):
    list_display = ('athlete', 'category', 'total_score', 'rank')
    list_filter = ('category', 'last_updated')
    search_fields = ('athlete__first_name', 'category')
    readonly_fields = ('last_updated',)
    fieldsets = (
        ('Ranking Information', {
            'fields': ('athlete', 'category', 'total_score', 'rank', 'events_participated')
        }),
        ('Updated', {
            'fields': ('last_updated',),
            'classes': ('collapse',)
        }),
    )


@admin.register(EvaluationCertificate)
class EvaluationCertificateAdmin(admin.ModelAdmin):
    list_display = ('title', 'athlete', 'issued_by', 'issued_date', 'is_viewable_by_parents')
    list_filter = ('is_viewable_by_parents', 'issued_date', 'valid_until', 'event')
    search_fields = ('title', 'athlete__first_name', 'issued_by__first_name')
    readonly_fields = ('issued_date', 'valid_from', 'created_at')
    fieldsets = (
        ('Certificate Information', {
            'fields': ('athlete', 'title', 'description', 'certificate_number', 'event')
        }),
        ('Issued Information', {
            'fields': ('issued_by', 'issued_date')
        }),
        ('Validity', {
            'fields': ('valid_from', 'valid_until')
        }),
        ('Visibility', {
            'fields': ('is_viewable_by_parents',)
        }),
    )



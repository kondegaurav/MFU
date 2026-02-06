from django.contrib import admin
from .models import CoachProfile, TrainingSession, CompetitionTeam, TeamMember


class TrainingSessionInline(admin.TabularInline):
    model = TrainingSession
    extra = 0
    fields = ('title', 'start_time', 'status')
    readonly_fields = ()


class TeamMemberInline(admin.TabularInline):
    model = TeamMember
    extra = 0
    fields = ('athlete', 'role', 'jersey_number', 'joined_at')
    readonly_fields = ('joined_at',)


@admin.register(CoachProfile)
class CoachProfileAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'specializations', 'is_head_coach', 'experience_years')
    list_filter = ('is_head_coach', 'experience_years', 'center')
    search_fields = ('user__first_name', 'user__last_name', 'specializations')
    inlines = [TrainingSessionInline]
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Professional Information', {
            'fields': ('specializations', 'certifications', 'experience_years', 'is_head_coach')
        }),
        ('Center Assignment', {
            'fields': ('center',)
        }),
    )
    
    def get_full_name(self, obj):
        return obj.user.get_full_name() or obj.user.email
    get_full_name.short_description = 'Coach'


@admin.register(TrainingSession)
class TrainingSessionAdmin(admin.ModelAdmin):
    list_display = ('title', 'coach', 'center', 'start_time', 'status')
    list_filter = ('status', 'start_time', 'coach', 'center')
    search_fields = ('title', 'coach__user__first_name', 'center__name')
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'coach', 'center')
        }),
        ('Time & Status', {
            'fields': ('start_time', 'end_time', 'status')
        }),
        ('Details', {
            'fields': ('notes', 'attendance', 'athletes')
        }),
    )


@admin.register(CompetitionTeam)
class CompetitionTeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'coach', 'category', 'member_count', 'status')
    list_filter = ('category', 'status', 'coach')
    search_fields = ('name', 'coach__user__first_name', 'category')
    inlines = [TeamMemberInline]
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'coach')
        }),
        ('Category & Status', {
            'fields': ('category', 'status')
        }),
    )
    
    def member_count(self, obj):
        return obj.athletes.count()
    member_count.short_description = 'Members'


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('athlete', 'team', 'role', 'jersey_number', 'joined_at')
    list_filter = ('role', 'team', 'joined_at')
    search_fields = ('athlete__first_name', 'team__name')
    readonly_fields = ('joined_at',)
    fieldsets = (
        ('Assignment', {
            'fields': ('athlete', 'team', 'role', 'jersey_number')
        }),
        ('Status', {
            'fields': ('joined_at', 'removed_at')
        }),
    )



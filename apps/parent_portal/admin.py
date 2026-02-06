from django.contrib import admin
from .models import Parent, ParentChildRelation


class ParentChildRelationInline(admin.TabularInline):
    model = ParentChildRelation
    extra = 0
    fields = ('child', 'relationship_type', 'can_view_scores', 'can_view_rankings', 'can_view_certificates')


@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'phone', 'is_primary_contact', 'children_count')
    list_filter = ('is_primary_contact', 'user__date_joined')
    search_fields = ('user__first_name', 'user__last_name', 'phone')
    inlines = [ParentChildRelationInline]
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Contact Information', {
            'fields': ('phone', 'alternate_phone')
        }),
        ('Professional Information', {
            'fields': ('occupation',)
        }),
        ('Status', {
            'fields': ('is_primary_contact',)
        }),
    )
    
    def get_full_name(self, obj):
        return obj.user.get_full_name() or obj.user.email
    get_full_name.short_description = 'Parent'
    
    def children_count(self, obj):
        return obj.children.count()
    children_count.short_description = 'Children'


@admin.register(ParentChildRelation)
class ParentChildRelationAdmin(admin.ModelAdmin):
    list_display = ('parent_name', 'child_name')
    list_filter = ('can_view_scores', 'can_view_rankings')
    search_fields = ('parent__user__first_name', 'child__first_name')
    fieldsets = (
        ('Relationship', {
            'fields': ('parent', 'child', 'relationship_type')
        }),
        ('Permissions - View Scores & Results', {
            'fields': ('can_view_scores', 'can_view_competition_results', 'can_view_events')
        }),
        ('Permissions - Rankings & Certifications', {
            'fields': ('can_view_rankings', 'can_view_certificates', 'can_view_training_schedule')
        }),
        ('Permissions - Financial & Medical', {
            'fields': ('can_view_fees', 'can_view_medical_info', 'can_view_contact_info')
        }),
    )
    
    def parent_name(self, obj):
        return obj.parent.user.get_full_name()
    parent_name.short_description = 'Parent'
    
    def child_name(self, obj):
        return obj.child.get_full_name()
    child_name.short_description = 'Child'



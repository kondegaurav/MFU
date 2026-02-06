"""
URL Configuration for MFU Web Portal.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Authentication (django-allauth)
    path('accounts/', include('allauth.urls')),

    # Custom authentication views
    path('auth/', include('apps.authentication.urls')),

    # User profiles
    path('profiles/', include('apps.profiles.urls')),

    # Core permission examples
    path('core/', include('apps.core.urls')),

    # Portal dashboards
    path('admin-portal/', include('apps.admin_portal.urls')),
    path('coach-portal/', include('apps.coach_portal.urls')),
    path('parent-portal/', include('apps.parent_portal.urls')),
    path('athlete-portal/', include('apps.athlete_portal.urls')),
    path('finance-portal/', include('apps.finance_portal.urls')),

    # Home page - redirect to login
    path('', include('apps.authentication.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    # Debug toolbar
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

# Customize admin site
admin.site.site_header = "MFU Web Portal Administration"
admin.site.site_title = "MFU Portal Admin"
admin.site.index_title = "Welcome to MFU Web Portal"

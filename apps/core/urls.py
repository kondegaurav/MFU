from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('examples/', views.permission_examples, name='permission_examples'),
    path('examples/admin-only/', views.admin_only_view, name='admin_only'),
    path('examples/admin-center/', views.admin_center_head_view, name='admin_center_head'),
    path('examples/coach/', views.CoachExampleView.as_view(), name='coach_example'),
]

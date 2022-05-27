"""Define URL patterns for performance_reports"""

from django.urls import path

from . import views

app_name = 'performance_reports'

urlpatterns = [
    path('', views.index, name="index"),
    path('export_notes', views.export_notes, name="export_notes"),
    path('export_notes/get_str', views.get_random_string, name="get_str"),
]
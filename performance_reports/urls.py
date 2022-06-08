"""Define URL patterns for performance_reports"""

from django.urls import path

from . import views

app_name = 'performance_reports'

urlpatterns = [
    path('', views.index, name="index"),
    path('export-notes', views.export_notes, name="export-notes"),
    path('export-notes/get-str', views.get_random_string, name="get-str"),
    path('add_user', views.add_user, name="add_user"),
    path('login', views.user_login, name="login"),
]
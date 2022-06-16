"""Define URL patterns for performance_reports"""

from django.urls import path
from . import views

app_name = 'performance_reports'

urlpatterns = [
    path('', views.index, name="index"),
    path('export-notes', views.export_notes, name="export-notes"),
    path('export-notes/get-str', views.get_random_string, name="get-str"),
    path('add-user', views.add_user, name="add-user"),
    path('login', views.user_login, name="login"),
    path('logout', views.user_logout, name="logout"),
    path('change-pwd', views.user_update_pwd, name="change-pwd"),
    path('user-admin', views.user_admin, name="user-admin"),
    path('admin-only', views.admin_only, name="admin-only"),
    path('user-admin/delete-user/<str:username>', views.user_admin_delete_user, name="delete-user"),
    path('user-admin/update-user', views.user_admin_update_user_pwd, name="update-user"),
]
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),

    # Auth
    path("", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("logout/", views.logout_view, name="logout"),

    # Password Reset
    path("password-reset/",
         auth_views.PasswordResetView.as_view(template_name="password_reset.html"),
         name="password_reset"),
    path("password-reset/done/",
         auth_views.PasswordResetDoneView.as_view(template_name="password_reset_done.html"),
         name="password_reset_done"),
    path("password-reset-confirm/<uidb64>/<token>/",
         auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_confirm.html"),
         name="password_reset_confirm"),
    path("password-reset-complete/",
         auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_complete.html"),
         name="password_reset_complete"),

    # Dashboard
    path("dashboard/", views.dashboard, name="dashboard"),
    path("calendar/", views.calendar_view, name="calendar"),
    path("activity/", views.activity_view, name="activity"),

    # Profile & Settings
    path("profile/", views.profile_view, name="profile"),
    path("settings/", views.settings_view, name="settings"),

    # Notifications
    path("notifications/", views.notifications_view, name="notifications"),
    path("api/notifications/", views.notifications_json, name="notifications_json"),

    # Export
    path("export/csv/", views.export_csv, name="export_csv"),
    path("export/pdf/", views.export_pdf, name="export_pdf"),

    # Task Operations
    path("task/<int:task_id>/edit/", views.update_task, name="update_task"),
    path("task/<int:task_id>/delete/", views.delete_task, name="delete_task"),
    path("task/<int:task_id>/toggle/", views.toggle_task_status, name="toggle_task_status"),
]
from django.contrib import admin
from .models import Task, UserProfile, ActivityLog


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "task_name", "owner", "priority", "due_date", "is_completed", "created_at")
    list_filter = ("is_completed", "priority", "created_at")
    search_fields = ("task_name", "owner__username")
    ordering = ("-created_at",)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "theme", "default_priority", "sort_order")


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ("user", "task_name", "action", "timestamp")
    list_filter = ("action", "timestamp")
    ordering = ("-timestamp",)
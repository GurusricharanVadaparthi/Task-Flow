from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Task(models.Model):
    PRIORITY_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
    ]

    task_name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)

    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default="medium",
    )

    due_date = models.DateField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="tasks"
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Task"
        verbose_name_plural = "Tasks"

    def __str__(self):
        return self.task_name

    @property
    def is_overdue(self):
        if self.due_date and not self.is_completed:
            return self.due_date < timezone.now().date()
        return False

    @property
    def is_due_today(self):
        if self.due_date and not self.is_completed:
            return self.due_date == timezone.now().date()
        return False


class UserProfile(models.Model):
    THEME_CHOICES = [
        ("light", "Light"),
        ("dark", "Dark"),
        ("system", "System"),
    ]

    SORT_CHOICES = [
        ("-created_at", "Newest First"),
        ("created_at", "Oldest First"),
        ("due_date", "Due Date"),
        ("priority", "Priority"),
        ("task_name", "Name (A-Z)"),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile"
    )
    bio = models.TextField(blank=True, null=True, max_length=300)
    theme = models.CharField(max_length=10, choices=THEME_CHOICES, default="light")
    default_priority = models.CharField(
        max_length=10,
        choices=Task.PRIORITY_CHOICES,
        default="medium"
    )
    sort_order = models.CharField(
        max_length=20,
        choices=SORT_CHOICES,
        default="-created_at"
    )
    email_notifications = models.BooleanField(default=True)
    browser_notifications = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"


class ActivityLog(models.Model):
    ACTION_CHOICES = [
        ("created", "Created"),
        ("edited", "Edited"),
        ("completed", "Completed"),
        ("uncompleted", "Marked Incomplete"),
        ("deleted", "Deleted"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="activities"
    )
    task_name = models.CharField(max_length=100)
    action = models.CharField(max_length=15, choices=ACTION_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return f"{self.user.username} {self.action} '{self.task_name}'"
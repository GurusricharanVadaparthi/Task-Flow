import csv
import calendar as cal
from datetime import timedelta, date
from io import BytesIO

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .models import Task, UserProfile, ActivityLog


def get_or_create_profile(user):
    profile, _ = UserProfile.objects.get_or_create(user=user)
    return profile


def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("register")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
            return redirect("register")

        user = User.objects.create_user(username=username, email=email, password=password)
        UserProfile.objects.create(user=user)

        messages.success(request, "Account created successfully.")
        return redirect("login")

    return render(request, "signup.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("dashboard")

        messages.error(request, "Invalid username or password.")
        return redirect("login")

    return render(request, "login.html")


@login_required(login_url="login")
def dashboard(request):
    profile = get_or_create_profile(request.user)

    if request.method == "POST":
        task_name = request.POST.get("task_name", "").strip()
        description = request.POST.get("description", "").strip()
        priority = request.POST.get("priority", profile.default_priority)
        due_date = request.POST.get("due_date") or None

        if task_name:
            task = Task.objects.create(
                task_name=task_name,
                description=description,
                priority=priority,
                due_date=due_date,
                owner=request.user
            )
            ActivityLog.objects.create(
                user=request.user,
                task_name=task.task_name,
                action="created"
            )
            messages.success(request, "Task added successfully.")

        return redirect("dashboard")

    all_tasks = Task.objects.filter(owner=request.user)

    search_query = request.GET.get("search", "").strip()
    status_filter = request.GET.get("status", "all")
    priority_filter = request.GET.get("priority", "all")

    tasks = all_tasks.order_by(profile.sort_order)

    if search_query:
        tasks = tasks.filter(task_name__icontains=search_query)

    if status_filter == "completed":
        tasks = tasks.filter(is_completed=True)
    elif status_filter == "pending":
        tasks = tasks.filter(is_completed=False)
    elif status_filter == "overdue":
        tasks = tasks.filter(is_completed=False, due_date__lt=timezone.now().date())

    if priority_filter in ["low", "medium", "high"]:
        tasks = tasks.filter(priority=priority_filter)

    total = all_tasks.count()
    completed = all_tasks.filter(is_completed=True).count()
    pending = all_tasks.filter(is_completed=False).count()
    overdue = all_tasks.filter(is_completed=False, due_date__lt=timezone.now().date()).count()
    due_today = all_tasks.filter(is_completed=False, due_date=timezone.now().date()).count()

    progress = int((completed / total) * 100) if total > 0 else 0

    today = timezone.now().date()
    chart_labels, chart_created, chart_completed = [], [], []
    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        chart_labels.append(day.strftime("%b %d"))
        chart_created.append(all_tasks.filter(created_at__date=day).count())
        chart_completed.append(all_tasks.filter(is_completed=True, completed_at__date=day).count())

    priority_data = [
        all_tasks.filter(priority="high").count(),
        all_tasks.filter(priority="medium").count(),
        all_tasks.filter(priority="low").count(),
    ]

    notif_count = overdue + due_today

    context = {
        "tasks": tasks,
        "total_tasks": total,
        "completed_tasks": completed,
        "pending_tasks": pending,
        "overdue_tasks": overdue,
        "due_today_tasks": due_today,
        "progress": progress,
        "search_query": search_query,
        "status_filter": status_filter,
        "priority_filter": priority_filter,
        "chart_labels": chart_labels,
        "chart_created": chart_created,
        "chart_completed": chart_completed,
        "priority_data": priority_data,
        "profile": profile,
        "notif_count": notif_count,
    }

    return render(request, "dashboard.html", context)


@login_required(login_url="login")
def update_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, owner=request.user)

    if request.method == "POST":
        task.task_name = request.POST.get("task_name", "").strip()
        task.description = request.POST.get("description", "").strip()
        task.priority = request.POST.get("priority", "medium")
        due_date = request.POST.get("due_date")
        task.due_date = due_date if due_date else None
        task.save()

        ActivityLog.objects.create(
            user=request.user,
            task_name=task.task_name,
            action="edited"
        )
        messages.success(request, "Task updated successfully.")
        return redirect("dashboard")

    profile = get_or_create_profile(request.user)
    return render(request, "edit_task.html", {"task": task, "profile": profile})


@login_required(login_url="login")
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, owner=request.user)
    task_name = task.task_name
    task.delete()

    ActivityLog.objects.create(
        user=request.user,
        task_name=task_name,
        action="deleted"
    )
    messages.success(request, "Task deleted successfully.")
    return redirect("dashboard")


@login_required(login_url="login")
def toggle_task_status(request, task_id):
    task = get_object_or_404(Task, id=task_id, owner=request.user)
    task.is_completed = not task.is_completed
    task.completed_at = timezone.now() if task.is_completed else None
    task.save()

    ActivityLog.objects.create(
        user=request.user,
        task_name=task.task_name,
        action="completed" if task.is_completed else "uncompleted"
    )
    return redirect("dashboard")


def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("login")


@login_required(login_url="login")
def profile_view(request):
    profile = get_or_create_profile(request.user)

    if request.method == "POST":
        request.user.first_name = request.POST.get("first_name", "").strip()
        request.user.last_name = request.POST.get("last_name", "").strip()
        request.user.email = request.POST.get("email", "").strip()
        request.user.save()

        profile.bio = request.POST.get("bio", "").strip()
        profile.save()

        messages.success(request, "Profile updated successfully.")
        return redirect("profile")

    total = Task.objects.filter(owner=request.user).count()
    completed = Task.objects.filter(owner=request.user, is_completed=True).count()

    return render(request, "profile.html", {
        "profile": profile,
        "total_tasks": total,
        "completed_tasks": completed,
    })


@login_required(login_url="login")
def settings_view(request):
    profile = get_or_create_profile(request.user)

    if request.method == "POST":
        profile.theme = request.POST.get("theme", "light")
        profile.default_priority = request.POST.get("default_priority", "medium")
        profile.sort_order = request.POST.get("sort_order", "-created_at")
        profile.email_notifications = request.POST.get("email_notifications") == "on"
        profile.browser_notifications = request.POST.get("browser_notifications") == "on"
        profile.save()

        messages.success(request, "Settings saved successfully.")
        return redirect("settings")

    return render(request, "settings.html", {"profile": profile})


@login_required(login_url="login")
def notifications_view(request):
    today = timezone.now().date()
    overdue = Task.objects.filter(owner=request.user, is_completed=False, due_date__lt=today)
    due_today = Task.objects.filter(owner=request.user, is_completed=False, due_date=today)
    recent_completed = Task.objects.filter(
        owner=request.user, is_completed=True
    ).order_by("-completed_at")[:5]

    profile = get_or_create_profile(request.user)

    return render(request, "notifications.html", {
        "overdue": overdue,
        "due_today": due_today,
        "recent_completed": recent_completed,
        "profile": profile,
    })


@login_required(login_url="login")
def calendar_view(request):
    profile = get_or_create_profile(request.user)
    today = timezone.now().date()

    try:
        year = int(request.GET.get("year", today.year))
        month = int(request.GET.get("month", today.month))
    except (ValueError, TypeError):
        year, month = today.year, today.month

    if month < 1:
        month, year = 12, year - 1
    elif month > 12:
        month, year = 1, year + 1

    cal_obj = cal.Calendar(firstweekday=6)
    month_days = cal_obj.monthdayscalendar(year, month)

    tasks = Task.objects.filter(
        owner=request.user,
        due_date__year=year,
        due_date__month=month
    )

    tasks_by_day = {}
    for task in tasks:
        day = task.due_date.day
        tasks_by_day.setdefault(day, []).append(task)

    weeks = []
    for week in month_days:
        week_data = []
        for day in week:
            week_data.append({
                "day": day,
                "tasks": tasks_by_day.get(day, []),
                "is_today": (day == today.day and month == today.month and year == today.year),
            })
        weeks.append(week_data)

    prev_month = month - 1 if month > 1 else 12
    prev_year = year if month > 1 else year - 1
    next_month = month + 1 if month < 12 else 1
    next_year = year if month < 12 else year + 1

    # Build months list (1-12 with names)
    months_list = [(i, cal.month_name[i]) for i in range(1, 13)]

    # Build years list (5 years back, 5 years forward from today)
    current_year = today.year
    years_list = list(range(current_year - 5, current_year + 6))

    return render(request, "calendar.html", {
        "weeks": weeks,
        "month_name": cal.month_name[month],
        "year": year,
        "month": month,
        "prev_month": prev_month,
        "prev_year": prev_year,
        "next_month": next_month,
        "next_year": next_year,
        "profile": profile,
        "months_list": months_list,
        "years_list": years_list,
        "today_year": today.year,
        "today_month": today.month,
    })


@login_required(login_url="login")
def activity_view(request):
    profile = get_or_create_profile(request.user)
    activities = ActivityLog.objects.filter(user=request.user)[:100]
    return render(request, "activity.html", {"activities": activities, "profile": profile})


@login_required(login_url="login")
def export_csv(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="my_tasks.csv"'

    writer = csv.writer(response)
    writer.writerow(["Task Name", "Description", "Priority", "Due Date", "Status", "Created At"])

    tasks = Task.objects.filter(owner=request.user)
    for task in tasks:
        writer.writerow([
            task.task_name,
            task.description or "",
            task.get_priority_display(),
            task.due_date.strftime("%Y-%m-%d") if task.due_date else "",
            "Completed" if task.is_completed else "Pending",
            task.created_at.strftime("%Y-%m-%d %H:%M"),
        ])

    return response


@login_required(login_url="login")
def export_pdf(request):
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
        from reportlab.lib import colors
    except ImportError:
        messages.error(request, "Please install reportlab: pip install reportlab")
        return redirect("dashboard")

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph(f"Tasks Report - {request.user.username}", styles["Title"]))
    elements.append(Spacer(1, 20))

    data = [["Task", "Priority", "Due Date", "Status"]]
    tasks = Task.objects.filter(owner=request.user)
    for task in tasks:
        data.append([
            task.task_name[:40],
            task.get_priority_display(),
            task.due_date.strftime("%Y-%m-%d") if task.due_date else "-",
            "Done" if task.is_completed else "Pending",
        ])

    table = Table(data, colWidths=[220, 80, 100, 80])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2563eb")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
        ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#f4f7fb")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    elements.append(table)
    doc.build(elements)

    pdf = buffer.getvalue()
    buffer.close()

    response = HttpResponse(pdf, content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="my_tasks.pdf"'
    return response

from django.http import JsonResponse

@login_required(login_url="login")
def notifications_json(request):
    """Returns JSON list of notifications for browser toast."""
    today = timezone.now().date()
    profile = get_or_create_profile(request.user)

    if not profile.browser_notifications:
        return JsonResponse({"notifications": []})

    overdue = Task.objects.filter(
        owner=request.user,
        is_completed=False,
        due_date__lt=today
    )

    due_today = Task.objects.filter(
        owner=request.user,
        is_completed=False,
        due_date=today
    )

    notifications = []

    for task in overdue:
        notifications.append({
            "id": f"overdue-{task.id}",
            "title": "⚠️ Overdue Task",
            "body": f"'{task.task_name}' was due on {task.due_date.strftime('%d %b %Y')}",
            "type": "overdue",
        })

    for task in due_today:
        notifications.append({
            "id": f"today-{task.id}",
            "title": "📅 Due Today",
            "body": f"'{task.task_name}' is due today!",
            "type": "today",
        })

    return JsonResponse({"notifications": notifications})
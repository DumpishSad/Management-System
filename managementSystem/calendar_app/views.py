from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone
from tasks.models import Task
from datetime import timedelta
from collections import defaultdict

@login_required
def daily_view(request):
    today = timezone.now().date()

    tasks = Task.objects.filter(
        assignee=request.user,
        deadline__date=today
    )

    meetings = request.user.meeting_set.filter(date=today)

    return render(request, 'calendar_app/daily.html', {
        'tasks': tasks,
        'meetings': meetings,
        'date': today,
    })


@login_required
def monthly_view(request):
    today = timezone.now().date()
    start = today.replace(day=1)
    end = (start + timedelta(days=32)).replace(day=1) - timedelta(days=1)

    tasks = Task.objects.filter(
        assignee=request.user,
        deadline__date__range=(start, end)
    )

    meetings = request.user.meeting_set.filter(date__range=(start, end))

    calendar_data = defaultdict(lambda: {'tasks': [], 'meetings': []})

    for task in tasks:
        calendar_data[task.deadline.date()]['tasks'].append(task)

    for meeting in meetings:
        calendar_data[meeting.date]['meetings'].append(meeting)

    return render(request, 'calendar_app/monthly.html', {
        'calendar_data': dict(calendar_data),
        'start': start,
        'end': end,
    })
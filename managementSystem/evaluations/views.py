from datetime import date
from django.utils import timezone

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from django.db.transaction import commit
from django.shortcuts import render, redirect, get_object_or_404

from .forms import EvaluationForm
from .models import Evaluation
from tasks.models import Task


@login_required
def evaluate_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if not (request.user.is_admin() or request.user.is_manager()):
        messages.error(request, "У вас нет прав на оценку.")
        return redirect('task_detail', pk=task_id)

    existing = Evaluation.objects.filter(task=task, reviewer=request.user).first()
    if existing:
        messages.info(request, "Задача уже оценена.")
        return redirect('task_detail', pk=task_id)

    if request.method == 'POST':
        form = EvaluationForm(request.POST)
        if form.is_valid():
            evaluation  = form.save(commit=False)
            evaluation.task = task
            evaluation.reviewer = request.user
            evaluation.target = task.assignee
            evaluation.save()
            messages.success(request, "Оценка сохранена.")
            return redirect('task_detail', pk=task_id)

    else:
        form = EvaluationForm()

    return render(request, 'evaluations/evaluate_task.html', {
        'form': form,
        'task': task
    })


@login_required
def my_evaluations(request):
    evaluations = request.user.received_evaluations.all().order_by('-date')
    today = timezone.now().date()
    month_avg = evaluations.filter(
        date__month=today.month,
        date__year=today.year
    ).aggregate(average=Avg('score'))['average']

    return render(request, 'evaluations/my_evaluations.html', {
        'evaluations': evaluations,
        'month_avg': month_avg
    })

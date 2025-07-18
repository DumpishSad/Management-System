from django.db import models
from django.forms import CharField
from .models import User


class Task(models.Model):
    STATUS_CHOICES = [
        ('open', 'Открыто'),
        ('in_progress', 'В работе'),
        ('done', 'Выполнено'),
    ]

    title = models.CharField(max_length=150)
    description = models.TextField()
    deadline = models.DateTimeField()
    status = models.CharField(choices=STATUS_CHOICES, default='open')
    creator = models.ForeignKey(User, related_name='created_tasks', on_delete=models.CASCADE)
    assignee = models.ForeignKey(User, related_name='assigned_tasks', on_delete=models.SET_NULL, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    task = models.ForeignKey(Task, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

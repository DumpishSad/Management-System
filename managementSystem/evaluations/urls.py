from django.urls import path
from . import views

urlpatterns = [
    path('task/<int:task_id>/evaluate/', views.evaluate_task, name='evaluate_task'),
    path('my/', views.my_evaluations, name='my_evaluations'),
]

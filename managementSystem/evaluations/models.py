from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from tasks.models import Task
from users.models import User


class Evaluation(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='given_evaluations')
    target = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_evaluations')
    score = models.IntegerField(validators=[
        MinValueValidator(1),
        MaxValueValidator(5)])
    date = models.DateField(auto_now_add=True)

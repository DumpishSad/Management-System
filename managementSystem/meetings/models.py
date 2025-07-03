from django.db import models
from django.forms import CharField

from users.models import User


class Meeting(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateField()
    time = models.TimeField()
    participants = models.ManyToManyField(User)

    def __str__(self):
        return f'{self.title} - {self.date} {self.time}'

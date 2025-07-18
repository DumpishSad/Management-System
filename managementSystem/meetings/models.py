from django.db import models
from django.forms import CharField

from users.models import User



class Meeting(models.Model):
    title = models.CharField(max_length=200)
    datetime = models.DateTimeField()  # ✅ заменяем date и time
    participants = models.ManyToManyField(User)

    def __str__(self):
        return f'{self.title} - {self.datetime.strftime("%Y-%m-%d %H:%M")}'

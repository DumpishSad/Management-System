from django.db import models
from django.utils.crypto import get_random_string


class Team(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = get_random_string(length=8)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

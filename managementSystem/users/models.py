from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (
        ('user', 'Обычный пользователь'),
        ('manager', 'Менеджер'),
        ('admin', 'Администратор'),
    )

    email = models.EmailField(unique=True)
    role = models.CharField(choices=ROLE_CHOICES, default='user')
    team = models.ForeignKey('teams.Team', null=True, blank=True, on_delete=models.SET_NULL)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f'{self.email} ({self.role})'

    def is_manager(self):
        return self.role == 'manager'

    def is_admin(self):
        return self.role == 'admin'
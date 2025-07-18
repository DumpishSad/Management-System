from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_team, name='create_team'),
    path('detail/', views.team_detail, name='team_detail'),
    path('manage/', views.manage_team, name='manage_team'),
    path('delete/', views.delete_team, name='delete_team'),
]
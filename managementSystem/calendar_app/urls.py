from django.urls import path
from . import views

urlpatterns = [
    path('daily/', views.daily_view, name='calendar_daily'),
    path('monthly/', views.monthly_view, name='calendar_monthly'),
]

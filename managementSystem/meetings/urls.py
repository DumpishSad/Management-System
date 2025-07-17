from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_meeting, name='create_meeting'),
    path('my/', views.my_meetings, name='my_meetings'),
    path('delete/<int:pk>/', views.delete_meeting, name='delete_meeting'),
]

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from tasks.models import Task
from meetings.models import Meeting


class CalendarViewTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.force_login(self.user)


    def test_daily_view_displays_tasks_and_meetings(self):
        task = Task.objects.create(
            title="Test Task",
            description="Some desc",
            deadline=timezone.now(),
            assignee=self.user,
            creator=self.user,
            status='open'
        )
        meeting = Meeting.objects.create(
            title="Team Sync",
            datetime=timezone.now(),
        )
        meeting.participants.add(self.user)

        response = self.client.get(reverse('calendar_daily'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Task")
        self.assertContains(response, "Team Sync")


    def test_monthly_view_displays_tasks_grouped_by_day(self):
        today = timezone.now()
        task = Task.objects.create(
            title="Monthly Task",
            description="Deadline task",
            deadline=today,
            assignee=self.user,
            creator=self.user,
            status='open'
        )
        meeting = Meeting.objects.create(
            title="Planning",
            datetime=today,
        )
        meeting.participants.add(self.user)

        response = self.client.get(reverse('calendar_monthly'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Monthly Task")
        self.assertContains(response, "Planning")

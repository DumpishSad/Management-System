from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model
from .models import Meeting

User = get_user_model()

class MeetingViewsTest(TestCase):
    def setUp(self):
        timestamp = str(timezone.now().timestamp()).replace('.', '')
        self.user = User.objects.create_user(username=f"user_{timestamp}", email=f"user_{timestamp}@example.com", password="pass")
        self.other_user = User.objects.create_user(username=f"other_{timestamp}", email=f"other_{timestamp}@example.com", password="pass")
        self.client.force_login(self.user)


    def test_create_meeting_success(self):
        response = self.client.post(reverse('create_meeting'), {
            'title': 'Test Meeting',
            'datetime': timezone.now() + timezone.timedelta(days=1),
            'participants': [self.user.id, self.other_user.id]
        })
        self.assertRedirects(response, reverse('my_meetings'))
        self.assertEqual(Meeting.objects.count(), 1)


    def test_create_meeting_conflict(self):
        conflict_time = timezone.now() + timezone.timedelta(days=1)
        meeting = Meeting.objects.create(title='Conflict', datetime=conflict_time)
        meeting.participants.add(self.other_user)

        response = self.client.post(reverse('create_meeting'), {
            'title': 'New Meeting',
            'datetime': conflict_time,
            'participants': [self.other_user.id]
        })

        self.assertContains(response, "уже есть встреча", status_code=200)
        self.assertEqual(Meeting.objects.count(), 1)


    def test_my_meetings_view(self):
        m = Meeting.objects.create(title='My Meeting', datetime=timezone.now() + timezone.timedelta(days=2))
        m.participants.add(self.user)
        response = self.client.get(reverse('my_meetings'))
        self.assertContains(response, 'My Meeting')


    def test_delete_meeting(self):
        m = Meeting.objects.create(title='Delete Me', datetime=timezone.now() + timezone.timedelta(days=2))
        m.participants.add(self.user)
        response = self.client.post(reverse('delete_meeting', args=[m.id]))
        self.assertRedirects(response, reverse('my_meetings'))
        self.assertEqual(Meeting.objects.count(), 0)

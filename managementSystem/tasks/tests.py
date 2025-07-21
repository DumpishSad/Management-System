from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model
from tasks.models import Task
from teams.models import Team
from evaluations.models import Evaluation

User = get_user_model()

class TaskViewsTest(TestCase):
    def setUp(self):
        timestamp = str(timezone.now().timestamp()).replace('.', '')
        self.team = Team.objects.create(name=f"Team{timestamp}")
        self.manager = User.objects.create_user(username=f"manager_{timestamp}", email=f"m_{timestamp}@e.com", password="pass", role="manager", team=self.team)
        self.dev = User.objects.create_user(username=f"dev_{timestamp}", email=f"d_{timestamp}@e.com", password="pass", role="user", team=self.team)
        self.client.force_login(self.manager)


    def test_create_task_success(self):
        future_deadline = timezone.now() + timezone.timedelta(days=1)
        response = self.client.post(reverse('task_create'), {
            'title': 'New Task',
            'description': 'Test desc',
            'assignee': self.dev.id,
            'deadline': future_deadline,
            'status': 'open',
        })

        self.assertEqual(Task.objects.count(), 1)
        self.assertRedirects(response, reverse('task_list'))


    def test_create_task_denied_for_regular_user(self):
        self.client.force_login(self.dev)
        response = self.client.get(reverse('task_create'))
        self.assertRedirects(response, reverse('task_list'))


    def test_task_list_shows_tasks_for_team(self):
        task = Task.objects.create(
            title='Shared Task',
            description='Description',
            creator=self.manager,
            assignee=self.dev,
            deadline=timezone.now()
        )
        response = self.client.get(reverse('task_list'))
        self.assertContains(response, 'Shared Task')


    def test_task_detail_shows_comments_and_evaluation_flag(self):
        task = Task.objects.create(
            title='Detailed Task',
            description='Some info',
            creator=self.manager,
            assignee=self.dev,
            deadline=timezone.now(),
            status='done'
        )
        response = self.client.get(reverse('task_detail', args=[task.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Detailed Task')
        self.assertTrue(response.context['can_evaluate'])


    def test_task_update_works(self):
        task = Task.objects.create(
            title='ToEdit',
            description='Original',
            creator=self.manager,
            assignee=self.dev,
            deadline=timezone.now() + timezone.timedelta(days=1),
            status='open'
        )
        response = self.client.post(reverse('task_update', args=[task.id]), {
            'title': 'Updated',
            'description': 'Updated desc',
            'assignee': self.dev.id,
            'deadline': timezone.now() + timezone.timedelta(days=2),
            'status': 'in_progress'
        })

        task.refresh_from_db()
        self.assertEqual(task.title, 'Updated')


    def test_task_delete_works(self):
        task = Task.objects.create(title='ToDelete', creator=self.manager, assignee=self.dev, deadline=timezone.now())
        response = self.client.post(reverse('task_delete', args=[task.id]))
        self.assertRedirects(response, reverse('task_list'))
        self.assertEqual(Task.objects.count(), 0)

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from tasks.models import Task
from evaluations.models import Evaluation

User = get_user_model()

class EvaluationViewTests(TestCase):
    def setUp(self):
        timestamp = timezone.now().timestamp()

        self.target = User.objects.create_user(
            username=f'dev_{timestamp}',
            email=f'dev_{timestamp}@example.com',
            password='pass',
            role='user'
        )
        self.manager = User.objects.create_user(
            username=f'manager_{timestamp}',
            email=f'manager_{timestamp}@example.com',
            password='pass',
            role='manager'
        )
        self.task = Task.objects.create(
            title='Task Title',
            description='Desc',
            assignee=self.target,
            creator=self.manager,
            deadline=timezone.now(),
            status='done'
        )
        self.client.force_login(self.manager)


    def test_only_manager_can_evaluate(self):
        self.client.logout()
        response = self.client.get(reverse('evaluate_task', args=[self.task.id]))
        login_url = reverse('login')
        expected_url = f"{login_url}?next={reverse('evaluate_task', args=[self.task.id])}"
        self.assertRedirects(response, expected_url)


    def test_evaluation_saved_successfully(self):
        response = self.client.post(
            reverse('evaluate_task', args=[self.task.id]),
            data={'score': 4, 'comment': 'Хорошая работа'}
        )
        self.assertRedirects(response, reverse('task_detail', args=[self.task.id]))
        self.assertEqual(Evaluation.objects.count(), 1)


    def test_cannot_evaluate_twice(self):
        Evaluation.objects.create(
            task=self.task,
            reviewer=self.manager,
            target=self.target,
            score=5
        )
        response = self.client.get(reverse('evaluate_task', args=[self.task.id]))
        self.assertRedirects(response, reverse('task_detail', args=[self.task.id]))


    def test_my_evaluations_view(self):
        Evaluation.objects.create(
            task=self.task,
            reviewer=self.manager,
            target=self.target,
            score=4,
            date=timezone.now().date()
        )
        self.client.logout()
        self.client.force_login(self.target)
        response = self.client.get(reverse('my_evaluations'))
        self.assertContains(response, "4.0")

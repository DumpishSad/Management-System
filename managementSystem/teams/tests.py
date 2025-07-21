from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from teams.models import Team
from django.utils import timezone

User = get_user_model()


class TeamViewsTests(TestCase):
    def setUp(self):
        timestamp = str(timezone.now().timestamp()).replace('.', '')
        self.admin = User.objects.create_user(
            username=f"admin_{timestamp}",
            email=f"a{timestamp}@mail.com",
            password="pass123",
            role="admin"
        )
        self.member = User.objects.create_user(
            username=f"user_{timestamp}",
            email=f"u{timestamp}@mail.com",
            password="pass123",
            role="user",
            team=None
        )
        self.team = Team.objects.create(name=f"Team{timestamp}")
        self.admin.team = self.team
        self.admin.save()
        self.client.force_login(self.admin)


    def test_create_team_view_as_admin(self):
        self.client.force_login(self.admin)
        response = self.client.post(reverse('create_team'), {'name': 'DreamTeam'})
        self.assertRedirects(response, reverse('team_detail'))
        self.assertTrue(Team.objects.filter(name='DreamTeam').exists())


    def test_create_team_denied_for_non_admin(self):
        self.client.logout()
        self.client.force_login(self.member)
        response = self.client.get(reverse('create_team'))
        self.assertRedirects(response, reverse('profile'))


    def test_team_detail_view(self):
        team = Team.objects.create(name='CoolTeam')
        self.admin.team = team
        self.admin.save()
        self.client.force_login(self.admin)
        response = self.client.get(reverse('team_detail'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.admin.username)


    def test_team_detail_redirects_if_no_team(self):
        self.member.team = None
        self.member.save()
        self.client.force_login(self.member)
        response = self.client.get(reverse('team_detail'))
        self.assertRedirects(response, reverse('profile'))


    def test_manage_team_add_user(self):
        team = Team.objects.create(name='TestTeam')
        self.admin.team = team
        self.admin.save()
        available_user = self.member
        available_user.team = None
        available_user.save()

        self.client.force_login(self.admin)
        response = self.client.post(reverse('manage_team'), {
            'action': 'add',
            'user_id': available_user.id
        })

        available_user.refresh_from_db()
        self.assertEqual(available_user.team, team)


    def test_delete_team(self):
        team = Team.objects.create(name='ToDelete')
        self.admin.team = team
        self.admin.save()
        self.client.force_login(self.admin)
        response = self.client.post(reverse('delete_team'))
        self.assertRedirects(response, reverse('profile'))
        self.assertFalse(Team.objects.filter(name='ToDelete').exists())

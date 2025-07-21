from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class UserViewsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )


    def test_register_view(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'new@example.com',
            'password1': 'newpass123!',
            'password2': 'newpass123!'
        })
        self.assertRedirects(response, reverse('login'))
        self.assertTrue(User.objects.filter(username='newuser').exists())


    def test_profile_requires_login(self):
        response = self.client.get(reverse('profile'))
        self.assertRedirects(response, '/users/login/?next=/users/profile/')


    def test_edit_profile(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('edit_profile'), {
            'username': 'updateduser',
            'email': 'updated@example.com',
            'role': self.user.role
        })
        self.assertRedirects(response, reverse('profile'))
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'updateduser')


    def test_delete_account(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('delete_account'))
        self.assertRedirects(response, reverse('login'))
        self.assertFalse(User.objects.filter(username='testuser').exists())


    def test_home_page_accessible(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

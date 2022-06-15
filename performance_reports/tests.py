from django.test import TestCase
from django.urls import reverse

class UserAdminViewTest:
    def test_users_context(self):
        # test user list is returned
        response = self.client.get(reverse('performance_reports:user-admin'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['usernames'], 'user1')

from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse_lazy


class AccountTestCase(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user("jdoe", password="changeme")

    def test_login(self):
        url = reverse_lazy('account:login')
        payload = {'username': 'jdoe', 'password': 'changeme'}
        response = self.client.post(url, payload, follow=True)
        self.assertEqual(reverse_lazy('projects:project-list') in response.redirect_chain[0], True)
        payload = {'username': 'invalid', 'password': 'invalid'}
        response = self.client.post(url, payload, follow=True)
        self.assertEqual(len(response.redirect_chain), 0)

    def test_profile_edit(self):
        # TODO: implement
        pass

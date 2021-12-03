from django.contrib.auth.models import User
from django.conf import settings
from django.urls import reverse_lazy
from apps.projects.models import Project
from ddf import G


class VulnmanTestMixin(object):
    def init_mixin(self):
        self.user1 = self._create_user("dummyuser1", "changeme")
        self.user2 = self._create_user("dummyuser2", "changeme")

    def _create_user(self, username, password, is_staff=False):
        return User.objects.create_user(username, password=password, is_staff=is_staff)

    def _create_project(self, name, customer="testcustomer", creator=None):
        return Project.objects.create(name=name, customer=customer, creator=creator)

    def get_url(self, endpoint, **kwargs):
        return reverse_lazy(endpoint, kwargs=kwargs)

    def _test_unauth_access(self, endpoint):
        url = self.get_url(endpoint)
        response = self.client.get(url, follow=True)
        login_url = self.get_url(settings.LOGIN_URL)
        self.assertEqual(len(response.redirect_chain), 1)
        self.assertEqual(str(login_url) in str(response.redirect_chain[0][0]), True)
        self.client.force_login(self.user1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def _create_instance(self, obj_class, **kwargs):
        return G(obj_class, **kwargs)

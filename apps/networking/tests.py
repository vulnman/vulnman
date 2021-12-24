from django.test import TestCase
from vulnman.tests.mixins import VulnmanTestMixin
from apps.networking import models


class HostTestCase(TestCase, VulnmanTestMixin):
    def setUp(self) -> None:
        self.init_mixin()

    def test_listview(self):
        url = self.get_url("projects:networking:host-list")
        self._test_unauthenticated_aceess(url)
        my_host = self._create_instance(models.Host, project__creator=self.user1)
        self.assign_perm("projects.pentest_project", self.pentester, my_host.project)
        not_my_host = self._create_instance(models.Host, project__creator=self.user2)
        self.assertEqual(models.Host.objects.count(), 2)
        # check without permissions
        self.login_with_project(self.user1, my_host.project)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        # check if i only can see my hosts
        self.login_with_project(self.pentester, my_host.project)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context_data.get('hosts', [])), 1)
        self.assertEqual(response.context_data['hosts'][0], my_host)
        # try to access not_my_host
        self._set_session_variable("project_pk", str(not_my_host.project.pk))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_detailview(self):
        my_host = self._create_instance(models.Host, project__creator=self.manager)
        url = self.get_url("projects:networking:host-detail", pk=my_host.pk)
        self.assign_perm("projects.pentest_project", self.pentester, my_host.project)
        # test unauth access
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        # test auth access
        self.login_with_project(self.pentester, my_host.project)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # test other user access
        self.client.force_login(self.user2)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_createview(self):
        url = self.get_url("projects:networking:host-create")
        self._test_unauthenticated_aceess(url)
        project = self._create_project(creator=self.manager)
        self.assign_perm("projects.pentest_project", self.pentester, project)
        payload = {"ip": "12.12.12.12", "is_online": True, "os": "unknown",
                   "hostname_set-TOTAL_FORMS": "1", "hostname_set-0-uuid": "", "hostname_set-0-host": "",
                   "hostname_set-0-name": "testhost.example.com", "hostname_set-0-DELETE": "",
                   "hostname_set-MAX_NUM_FORMS": "4",
                   "hostname_set-INITIAL_FORMS": "0", "hostname_set-MIN_NUM_FORMS": "0"}
        # test from other user
        self.login_with_project(self.user2, project)
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, 403)
        # test from my user
        self.login_with_project(self.pentester, project)
        response = self.client.post(url, payload, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(models.Host.objects.count(), 1)
        self.assertEqual(models.Host.objects.first().creator, self.pentester)
        self.assertEqual(models.Host.objects.filter(hostname__name="testhost.example.com").count(), 1)

    def test_deleteview(self):
        pass

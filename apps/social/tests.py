from django.test import TestCase
from vulnman.tests.mixins import VulnmanTestMixin
from apps.social import models


class EmployeeTestCase(TestCase, VulnmanTestMixin):
    def setUp(self) -> None:
        self.init_mixin()

    def test_listview(self):
        url = self.get_url("projects:social:employee-list")
        employee = self._create_instance(models.Employee, project__creator=self.user1, email="admin@example.com")
        # test unauthenticated
        self._test_unauthenticated_aceess(url)
        # test logged in
        self.login_with_project(self.user1, employee.project)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context_data['employees']), 1)
        # test other user
        self._test_foreign_access(url, self.user2, employee.project)

    def test_detailview(self):
        employee = self._create_instance(models.Employee, project__creator=self.user1, email="admin@example.com")
        url = self.get_url("projects:social:employee-detail", pk=employee.pk)
        self._test_unauthenticated_aceess(url)
        self._test_foreign_access(url, self.user2, employee.project)
        self.login_with_project(self.user1, employee.project)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class CredentialTestCase(TestCase, VulnmanTestMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.credential = self._create_instance(models.Credential, project__creator=self.user1)

    def test_listview(self):
        url = self.get_url("projects:social:credential-list")
        self._test_unauthenticated_aceess(url)
        # test logged in
        self.login_with_project(self.user1, self.credential.project)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context_data['credentials']), 1)
        # test other user
        self._test_foreign_access(url, self.user2, self.credential.project)

    def test_updateview(self):
        url = self.get_url("projects:social:credential-update", pk=self.credential.pk)
        self._test_unauthenticated_aceess(url)
        self._test_foreign_access(url, self.user2, self.credential.project)
        payload = {"username": "afterupdate", "location_found": "testcase"}
        self.login_with_project(self.user1, self.credential.project)
        response = self.client.post(url, payload, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(models.Credential.objects.filter(username="afterupdate").count(), 1)

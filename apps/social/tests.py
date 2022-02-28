from django.test import TestCase
from vulnman.tests.mixins import VulnmanTestMixin
from apps.social import models


class EmployeeTestCase(TestCase, VulnmanTestMixin):
    def setUp(self) -> None:
        self.init_mixin()

    def test_listview(self):
        url = self.get_url("projects:social:employee-list")
        project = self._create_project(creator=self.manager)
        self.assign_perm("projects.pentest_project", user_or_group=self.pentester, obj=project)
        employee = self._create_instance(models.Employee, project=project, email="admin@example.com")
        # test unauthenticated
        self._test_unauthenticated_aceess(url)
        # test logged in
        self.login_with_project(self.pentester, employee.project)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context_data['employees']), 1)
        # test other user
        self._test_foreign_access(url, self.user2, employee.project)

    def test_detailview(self):
        project = self._create_project(creator=self.manager)
        self.assign_perm("projects.pentest_project", user_or_group=self.pentester, obj=project)
        employee = self._create_instance(models.Employee, project=project, email="admin@example.com")
        url = self.get_url("projects:social:employee-detail", pk=employee.pk)
        self._test_unauthenticated_aceess(url)
        self._test_foreign_access(url, self.user2, employee.project)
        self.login_with_project(self.pentester, employee.project)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class CredentialTestCase(TestCase, VulnmanTestMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.credential = self._create_instance(models.Credential, project__creator=self.user1)
        self.assign_perm("projects.pentest_project", user_or_group=self.pentester, obj=self.credential.project)

    def test_listview(self):
        url = self.get_url("projects:social:credential-list")
        self._test_unauthenticated_aceess(url)
        # test logged in
        self.login_with_project(self.pentester, self.credential.project)
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
        self.login_with_project(self.pentester, self.credential.project)
        response = self.client.post(url, payload, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(models.Credential.objects.filter(username="afterupdate").count(), 1)

from django.test import TestCase
from django.utils import timezone
from vulnman.core.test import VulnmanTestCaseMixin
from apps.projects import models


class ProjectTokenDeleteViewTestCase(TestCase, VulnmanTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.token = self._create_instance(models.ProjectAPIToken, project=self.project1,
                                           user=self.pentester1, date_valid=timezone.now().date())

    def test_delete_valid(self):
        url = self.get_url("projects:token-delete", pk=self.token.pk)
        self.login_with_project(self.pentester1, self.project1)
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(models.ProjectAPIToken.objects.count(), 0)

    def test_delete_broken_access(self):
        url = self.get_url("projects:token-delete", pk=self.token.pk)
        self.login_with_project(self.pentester2, self.project2)
        response = self.client.post(url)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(models.ProjectAPIToken.objects.count(), 1)

    def test_contributor_broken_access(self):
        url = self.get_url("projects:token-delete", pk=self.token.pk)
        models.ProjectContributor.objects.create(role=models.ProjectContributor.ROLE_PENTESTER,
                                                 user=self.pentester2, project=self.project1)
        self.login_with_project(self.pentester2, self.project1)
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)


class ProjectTokenCreateViewTestCase(TestCase, VulnmanTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.data = {"date_valid": timezone.now(). date(), "name": "TestToken"}
        self.url = self.get_url("projects:token-create")

    def test_valid(self):
        self.login_with_project(self.pentester1, self.project1)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(models.ProjectAPIToken.objects.filter(
            user=self.pentester1, name=self.data["name"]).count(), 1)

    def test_vendor(self):
        self.login_with_project(self.vendor, self.project1)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 403)

    def test_readonly(self):
        self.login_with_project(self.read_only1, self.project1)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 403)


class ProjectTokenListViewTestCase(TestCase, VulnmanTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.url = self.get_url("projects:token-list")
        self.token1 = self._create_instance(models.ProjectAPIToken, project=self.project1,
                                            user=self.pentester1, date_valid=timezone.now().date())
        self.token2 = self._create_instance(models.ProjectAPIToken, project=self.project2,
                                            user=self.pentester2, date_valid=timezone.now().date())

    def test_valid(self):
        self.login_with_project(self.pentester1, self.project1)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context.get('tokens', [])), 1)
        self.assertEqual(response.context["tokens"][0], self.token1)
        self.login_with_project(self.pentester2, self.project2)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context.get('tokens', [])), 1)
        self.assertEqual(response.context["tokens"][0], self.token2)

    def test_contributor(self):
        models.ProjectContributor.objects.create(role=models.ProjectContributor.ROLE_PENTESTER, confirmed=True,
                                                 user=self.pentester2, project=self.project1)
        self.login_with_project(self.pentester2, self.project1)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context.get("tokens", [])), 0)

from django.test import TestCase
from vulnman.core.test import VulnmanTestCaseMixin
from apps.projects import models


class ProjectContributorCreateViewTestCase(TestCase, VulnmanTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.url = self.get_url("projects:contributor-create", pk=self.project1.pk)
        self.data = {
            "username": self.pentester2.username, "role": models.ProjectContributor.ROLE_PENTESTER
        }

    def test_valid(self):
        self.login_with_project(self.pentester1, self.project1)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.pentester2.has_perm("projects.change_project", self.project1), True)
        self.assertEqual(self.pentester2.has_perm("projects.add_contributor", self.project1), False)
        # FIXME: this is not working with django_q at the moment
        # self.assertEqual(len(mail.outbox), 1)

    def test_contributor_readonly(self):
        self.login_with_project(self.read_only1, self.project1)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 403)

    def test_pentester2(self):
        self.login_with_project(self.pentester2, self.project2)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(models.ProjectContributor.objects.filter(project=self.project1).count(), 1)
        self.assertEqual(self.pentester2.has_perm("projects.change_project", self.project1), False)

    def test_contributor_pentester(self):
        models.ProjectContributor.objects.create(role=models.ProjectContributor.ROLE_PENTESTER,
                                                 user=self.pentester2, project=self.project1)
        self.login_with_project(self.pentester2, self.project1)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 403)

    def test_contributor_from_other_client(self):
        models.ProjectContributor.objects.create(role=models.ProjectContributor.ROLE_PENTESTER,
                                                 user=self.pentester1, project=self.project1)
        self.login_with_project(self.pentester1, self.project1)
        data = self.data
        data["username"] = self.customer2.username
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["form"].errors), 1)


class ProjectContributorListViewTestCase(TestCase, VulnmanTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.url = self.get_url("projects:contributor-list", pk=self.project1.pk)
        self.contributor1 = models.ProjectContributor.objects.create(role=models.ProjectContributor.ROLE_PENTESTER,
                                                                     user=self.pentester2, project=self.project1)

    def test_valid(self):
        self.login_with_project(self.pentester1, self.project1)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context.get('contributors')), 2)
        self.assertIn(self.contributor1, response.context["contributors"])

    def test_vendor(self):
        self.login_with_project(self.vendor, self.project1)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_readonly(self):
        self.login_with_project(self.read_only1, self.project1)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context.get('contributors')), 2)
        self.assertIn(self.contributor1, response.context["contributors"])


class ProjectContributorDeleteViewTestCase(TestCase, VulnmanTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.contributor = models.ProjectContributor.objects.get(user=self.read_only1, project=self.project1)
        self.url = self.get_url("projects:contributor-delete", pk=self.contributor.pk)

    def test_valid(self):
        self.assertEqual(self.read_only1.has_perm("projects.view_project", self.project1), True)
        self.login_with_project(self.pentester1, self.project1)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.read_only1.has_perm("projects.view_project", self.project1), False)

    def test_contributor_readonly(self):
        self.login_with_project(self.read_only1, self.project1)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 403)

    def test_pentester2(self):
        self.login_with_project(self.pentester2, self.project2)
        response = self.client.post(self.url)
        self.assertEqual(models.ProjectContributor.objects.filter(pk=self.contributor.pk).count(), 1)
        self.assertEqual(response.status_code, 404)

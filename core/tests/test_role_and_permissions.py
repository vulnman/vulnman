from django.test import TestCase
from vulnman.core.test import VulnmanTestCaseMixin
from apps.assets import models
from apps.projects.models import ProjectContributor, ProjectAPIToken


class ProjectUserRolesTestCase(TestCase, VulnmanTestCaseMixin):
    def setUp(self):
        self.init_mixin()

    def test_creator_asset_create(self):
        url = self.get_url("projects:assets:host-create")
        payload = {"ip": "1.2.2.3", "accessibility": 1, "environment": models.Host.ENVIRONMENT_STAGING}
        self.login_with_project(self.pentester1, self.project1)
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(models.Host.objects.count(), 1)

    def test_read_only_asset_create(self):
        url = self.get_url("projects:assets:host-create")
        payload = {"ip": "1.2.3.4", "accessibility": 1, "environment": models.Host.ENVIRONMENT_DEVELOPMENT}
        self.login_with_project(self.pentester2, self.project1)
        self._create_instance(ProjectContributor,
            user=self.pentester2, role=ProjectContributor.ROLE_READ_ONLY, project=self.project1)
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(models.Host.objects.count(), 0)

    def test_pentester_asset_create(self):
        url = self.get_url("projects:assets:host-create")
        payload = {"ip": "1.2.3.4", "accessibility": 1, "environment": models.Host.ENVIRONMENT_UNKNOWN}
        self.login_with_project(self.pentester2, self.project1)
        self.create_instance(ProjectContributor, user=self.pentester2, confirmed=True,
                             role=ProjectContributor.ROLE_PENTESTER, project=self.project1)
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(models.Host.objects.count(), 1)

    def test_api_token_wiped(self):
        contributor = self.add_contributor(self.pentester2, self.project1)
        self._create_instance(ProjectAPIToken, user=self.pentester2, project=self.project1)
        self.assertEqual(ProjectAPIToken.objects.count(), 1)
        contributor.delete()
        self.assertEqual(ProjectAPIToken.objects.count(), 0)

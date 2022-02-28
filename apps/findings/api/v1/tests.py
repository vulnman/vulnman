from rest_framework.test import APITestCase
from vulnman.tests.mixins import VulnmanTestMixin, VulnmanAPITestMixin
from apps.findings import models
from apps.networking.models import Host


class TemplateAPITestCase(APITestCase, VulnmanTestMixin):
    def setUp(self) -> None:
        self.init_mixin()

    def test_list(self):
        url = self.get_url("api:v1:vulnerability-template-list")
        template = self._create_instance(models.Template, creator=self.user1)
        # test unauthenticated
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        # test logged in
        self.client.force_login(self.user1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["results"]), 1)

    def test_detail(self):
        template = self._create_instance(models.Template, creator=self.user1)
        url = self.get_url("api:v1:vulnerability-template-detail", pk=template.pk)
        # test unauthenticated
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        # test logged in
        self.client.force_login(self.user1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["uuid"], str(template.pk))

    def test_update(self):
        template = self._create_instance(models.Template, creator=self.user1, name="before")
        url = self.get_url("api:v1:vulnerability-template-detail", pk=template.pk)
        new_data = {"name": "after"}
        # test unauthenticated
        response = self.client.patch(url, new_data)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(models.Template.objects.filter(name="after").count(), 0)
        # test logged in
        self.client.force_login(self.user1)
        response = self.client.patch(url, new_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(models.Template.objects.filter(name="after").count(), 1)

    def test_delete(self):
        # TODO: implement. should only the creator be allowed to delete a template?
        pass

"""
class VulnerabilityViewSetTestCase(APITestCase, VulnmanAPITestMixin):
    def setUp(self) -> None:
        self.init_mixin()

    def test_listview(self):
        self._test_project_listview("api:v1:vulnerability-list", models.Vulnerability)

    def test_updateview(self):
        payload = {"name": "another vuln"}
        self._test_project_updateview("api:v1:vulnerability-detail", payload, models.Vulnerability)

    def test_createview(self):
        host = self._create_instance(Host, project__creator=self.user1)
        payload = {"name": "my vuln", "host": str(host.pk), "description": "test", "resolution": "resolution",
                   "project": str(self.user1.project_set.first().pk), "cvss_score": "8.0",
                   "ease_of_resolution": "trivial", "details": {"data": "hello"}}
        self._test_project_createview("api:v1:vulnerability-list", payload, models.Vulnerability, format='json')
        self.assertEqual(models.VulnerabilityDetails.objects.count(), 1)

    def test_deleteview(self):
        self._test_project_deleteview("api:v1:vulnerability-detail", models.Vulnerability)
"""
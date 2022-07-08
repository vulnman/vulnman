from django.test import TestCase
from vulnman.core.test import VulnmanTestCaseMixin
from apps.assets import models


class WebApplicationDetailTestCase(TestCase, VulnmanTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.webapp = self._create_instance(models.WebApplication, project=self.project1)
        self.url = self.webapp.get_absolute_url()

    def test_valid(self):
        self.login_with_project(self.pentester1, self.project1)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_pentester2(self):
        self.login_with_project(self.pentester2, self.project2)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 404)

    def test_readonly(self):
        self.login_with_project(self.read_only1, self.project1)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["webapp"], self.webapp)

    def test_vendor(self):
        self.client.force_login(self.vendor)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)


class WebApplicationListViewTestCase(TestCase, VulnmanTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.webapp1 = self._create_instance(models.WebApplication, project=self.project1)
        self.webapp2 = self._create_instance(models.WebApplication, project=self.project2)
        self.url = self.get_url("projects:assets:webapp-list")

    def test_valid(self):
        self.login_with_project(self.pentester1, self.project1)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["webapps"]), 1)
        self.assertIn(self.webapp1, response.context["webapps"])

    def test_readonly(self):
        pass

    def test_vendor(self):
        self.client.force_login(self.vendor)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_pentester2(self):
        self.login_with_project(self.pentester2, self.project2)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["webapps"]), 1)
        self.assertNotIn(self.webapp1, response.context["webapps"])


class WebApplicationCreateViewTestCase(TestCase, VulnmanTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.url = self.get_url("projects:assets:webapp-create")
        self.data = {"base_url": "https://example.com", "name": "My Test Webapp", "description": "hello"}

    def test_valid(self):
        self.login_with_project(self.pentester1, self.project1)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(models.WebApplication.objects.filter(project=self.project1).count(), 1)

    def test_readonly(self):
        self.login_with_project(self.read_only1, self.project1)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 403)

    def test_vendor(self):
        self.client.force_login(self.vendor)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 403)


class WebApplicationUpdateViewTestCase(TestCase, VulnmanTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.webapp = self._create_instance(models.WebApplication, project=self.project1)
        self.url = self.get_url("projects:assets:webapp-update", pk=self.webapp.pk)
        self.data = {"base_url": "https://example.com", "name": "My Test Webapp2"}

    def test_valid(self):
        self.login_with_project(self.pentester1, self.project1)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(models.WebApplication.objects.filter(project=self.project1,
                                                              name=self.data["name"]).count(), 1)

    def test_pentester2(self):
        self.login_with_project(self.pentester2, self.project2)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 404)

    def test_readonly(self):
        self.login_with_project(self.read_only1, self.project1)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 403)

    def test_vendor(self):
        self.client.force_login(self.vendor)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 403)


class WebApplicationDeleteViewTestCase(TestCase, VulnmanTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.webapp = self._create_instance(models.WebApplication, project=self.project1)
        self.url = self.webapp.get_absolute_delete_url()

    def test_valid(self):
        self.login_with_project(self.pentester1, self.project1)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(models.WebApplication.objects.filter(pk=self.webapp.pk).exists(), False)

    def test_pentester2(self):
        self.login_with_project(self.pentester2, self.project2)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 404)

    def test_readonly(self):
        self.login_with_project(self.read_only1, self.project1)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 403)

    def test_vendor(self):
        self.client.force_login(self.vendor)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 403)

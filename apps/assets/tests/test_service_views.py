from django.test import TestCase
from vulnman.core.test import VulnmanTestCaseMixin
from apps.assets import models


class ServiceCreateViewTestCase(TestCase, VulnmanTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.url = self.get_url("projects:assets:service-create")
        self.host1 = self._create_instance(models.Host, project=self.project1)
        self.host2 = self._create_instance(models.Host, project=self.project2)
        self.data = {"host": self.host1.pk, "port": 80, "name": "http", "protocol": "tcp",
                     "state": models.Service.STATE_OPEN}

    def test_valid(self):
        self.login_with_project(self.pentester1, self.project1)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(models.Service.objects.filter(project=self.project1, host=self.host1,
                                                       name=self.data["name"]).count(), 1)

    def test_other_project_host(self):
        self.login_with_project(self.pentester1, self.project1)
        self.data["host"] = self.host2.pk
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(models.Service.objects.filter(project=self.project1, host=self.host2).count(), 0)

    def test_readonly(self):
        self.login_with_project(self.read_only1, self.project1)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 403)

    def test_pentester2(self):
        # same effect as 'test_other_project_host'
        self.login_with_project(self.pentester2, self.project2)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 200)

    def test_vendor(self):
        self.client.force_login(self.vendor)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 403)


class ServiceUpdateViewTestCase(TestCase, VulnmanTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.host1 = self._create_instance(models.Host, project=self.project1)
        self.host2 = self._create_instance(models.Host, project=self.project2)
        self.service = self._create_instance(models.Service, project=self.project1, host=self.host1)
        self.url = self.get_url("projects:assets:service-update", pk=self.service.pk)
        self.data = {"host": self.host1.pk, "port": 80, "name": "http", "protocol": "tcp",
                     "state": models.Service.STATE_OPEN}

    def test_valid(self):
        self.login_with_project(self.pentester1, self.project1)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(models.Service.objects.filter(host=self.host1, project=self.project1,
                                                       name=self.data["name"]).count(), 1)

    def test_pentester2(self):
        self.login_with_project(self.pentester2, self.project2)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 404)

    def test_invalid_host(self):
        self.login_with_project(self.pentester2, self.project2)
        self.data["host"] = self.host2.pk
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


class ServiceDeleteViewTestCase(TestCase, VulnmanTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.host = self._create_instance(models.Host, project=self.project1)
        self.service = self._create_instance(models.Service, project=self.project1, host=self.host)
        self.url = self.service.get_absolute_delete_url()

    def test_valid(self):
        self.login_with_project(self.pentester1, self.project1)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(models.Service.objects.count(), 0)

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


class ServiceDetailViewTestCase(TestCase, VulnmanTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.host = self._create_instance(models.Host, project=self.project1)
        self.service = self._create_instance(models.Service, project=self.project1, host=self.host)
        self.url = self.service.get_absolute_url()

    def test_valid(self):
        self.login_with_project(self.pentester1, self.project1)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_pentester2(self):
        self.login_with_project(self.pentester2, self.project2)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 404)

    def test_vendor(self):
        self.client.force_login(self.vendor)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 403)

    def test_readonly(self):
        self.login_with_project(self.read_only1, self.project1)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

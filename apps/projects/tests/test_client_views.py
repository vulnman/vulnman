from django.test import TestCase
from vulnman.core.test import VulnmanTestCaseMixin
from apps.projects import models


class ClientDetailViewTestCase(TestCase, VulnmanTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.customer = self._create_instance(models.Client)
        self.url = self.get_url("clients:client-detail", pk=self.customer.pk)

    def test_pentester(self):
        self.client.force_login(self.pentester1)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_vendor(self):
        self.client.force_login(self.vendor)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_readonly(self):
        self.client.force_login(self.read_only1)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_customer(self):
        self.client.force_login(self.customer1)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)


class ClientListViewTestCase(TestCase, VulnmanTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.url = self.get_url("clients:client-list")

    def test_pentester(self):
        self.client.force_login(self.pentester1)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["clients"]), 2)
        self.assertIn(self.project1.client, response.context["clients"])

    def test_vendor(self):
        self.client.force_login(self.vendor)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_readonly(self):
        self.client.force_login(self.read_only1)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_customer(self):
        self.client.force_login(self.customer1)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)


class ClientCreateViewTestCase(TestCase, VulnmanTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.url = self.get_url("clients:client-create")
        self.data = {"name": "test", "street": "test", "city": "test", "country": "test_country", "zip": 1234,
                     "homepage": "https://test-homepage.com", "logo": ""}

    def test_pentester(self):
        self.client.force_login(self.pentester1)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(models.Client.objects.count(), 3)

    def test_vendor(self):
        self.client.force_login(self.vendor)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 403)

    def test_customer(self):
        self.client.force_login(self.customer1)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)


class ClientUpdateViewTestCase(TestCase, VulnmanTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        client = self.create_instance(models.Client)
        self.url = self.get_url("clients:client-update", pk=client.pk)
        self.data = {"name": "test", "street": "test", "city": "test", "country": "test_country", "zip": 1234,
                     "homepage": "https://test-homepage.com", "logo": ""}

    def test_pentester(self):
        self.client.force_login(self.pentester1)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(models.Client.objects.filter(homepage=self.data["homepage"]).count(), 1)

    def test_vendor(self):
        self.client.force_login(self.vendor)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 403)

    def test_customer(self):
        self.client.force_login(self.customer1)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)


class ClientDeleteViewTestCase(TestCase, VulnmanTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.project_client = self.create_instance(models.Client)
        self.url = self.get_url("clients:client-delete", pk=self.project_client.pk)

    def test_pentester(self):
        self.client.force_login(self.pentester1)
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(models.Client.objects.filter(pk=self.project_client.pk).count(), 0)

    def test_vendor(self):
        self.client.force_login(self.vendor)
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, 403)

    def test_customer(self):
        self.client.force_login(self.customer1)
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, 403)

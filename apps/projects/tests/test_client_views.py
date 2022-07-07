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
        self.assertEqual(response.status_code, 403)

    def test_vendor(self):
        self.client.force_login(self.vendor)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_readonly(self):
        self.client.force_login(self.pentester1)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_valid(self):
        self.client.force_login(self.manager)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)


class ClientListViewTestCase(TestCase, VulnmanTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.url = self.get_url("clients:client-list")

    def test_valid(self):
        self.client.force_login(self.manager)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["clients"]), 2)
        self.assertIn(self.project1.client, response.context["clients"])

    def test_pentester(self):
        self.client.force_login(self.pentester1)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_vendor(self):
        self.client.force_login(self.vendor)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_readonly(self):
        self.client.force_login(self.read_only1)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

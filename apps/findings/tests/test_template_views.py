from django.test import TestCase
from vulnman.core.test import VulnmanTestCaseMixin
from apps.findings import models


class TemplateListViewTestCase(TestCase, VulnmanTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.url = self.get_url("findings:template-list")

    def test_valid(self):
        template = self._create_instance(models.Template)
        self.client.force_login(self.pentester1)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["templates"][0], template)

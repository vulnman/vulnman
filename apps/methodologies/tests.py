from django.test import TestCase
from vulnman.tests.mixins import VulnmanTestMixin
from apps.methodologies import models


class MethodologyTestCase(TestCase, VulnmanTestMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.methodology1 = self._create_instance(models.Methodology, creator=self.user1)

    def test_methodology_model(self):
        self.assertEqual(models.Methodology.objects.first().pk, self.methodology1.pk)
        self.assertEqual(models.Methodology.objects.first().creator, self.user1)

    def test_methodology_listview(self):
        url = self.get_url("methodology:methodology-list")
        self._test_unauthenticated_aceess(url, expected_status_code=200)

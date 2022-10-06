from django.test import TestCase
from vulnman.core.test import VulnmanTestCaseMixin
from apps.assets import models as asset_models
from apps.findings import models


class CVSSCreateViewTestCase(TestCase, VulnmanTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.asset1 = self._create_instance(asset_models.WebApplication, project=self.project1)
        ct = models.Vulnerability.objects.get_asset_content_type(self.asset1.pk)
        self.vulnerability = self.create_instance(models.Vulnerability, project=self.project1, asset=self.asset1,
                                                  content_type=ct, object_id=self.asset1.pk)
        self.url = self.get_url("projects:findings:cvs-score-create", pk=self.vulnerability.pk)
        self.data = {"attack_vector": "N", "attack_complexity": "L", "scope": "C", "confidentiality": "L",
                     "availability": "L", "integrity": "L", "user_interaction": "N", "privilege_required": "N"}

    def test_valid(self):
        self.login_with_project(self.pentester1, self.project1)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(models.CVSScore.objects.filter(vulnerability=self.vulnerability,
                                                        project=self.project1).count(), 1)
        self.assertEqual(models.CVSScore.objects.filter(**self.data).count(), 1)

    def test_pentester2(self):
        self.login_with_project(self.pentester2, self.project2)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 404)

    def test_readonly(self):
        self.login_with_project(self.read_only1, self.project1)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 403)


class CVSSUpdateTestCase(TestCase, VulnmanTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.asset1 = self._create_instance(asset_models.WebApplication, project=self.project1)
        ct = models.Vulnerability.objects.get_asset_content_type(self.asset1.pk)
        # we need to precise here otherwise DDF fails
        self.vulnerability = self.create_instance(models.Vulnerability, project=self.project1, asset=self.asset1,
                                                  content_type=ct, object_id=self.asset1.pk)
        cvs_score = self.create_instance(models.CVSScore, project=self.project1, vulnerability=self.vulnerability)
        self.url = self.get_url("projects:findings:cvs-score-update", pk=cvs_score.pk)
        self.data = {"attack_vector": "N", "scope": "C"}

    def test_valid(self):
        self.login_with_project(self.pentester1, self.project1)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(models.Vulnerability.objects.filter(
            cvsscore__attack_vector=self.data["attack_vector"], cvsscore__scope=self.data["scope"]).count(), 1)

    def test_pentester2(self):
        self.login_with_project(self.pentester2, self.project2)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 404)

    def test_readonly(self):
        self.login_with_project(self.read_only1, self.project1)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 403)

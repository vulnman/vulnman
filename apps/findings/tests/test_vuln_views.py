from django.test import TestCase
from vulnman.core.test import VulnmanTestCaseMixin
from apps.assets import models as asset_models
from apps.findings import models


class VulnerabilityListViewTestCase(TestCase, VulnmanTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.url = self.get_url("projects:findings:vulnerability-list")
        self.asset1 = self._create_instance(asset_models.WebApplication, project=self.project1)
        ct = models.Vulnerability.objects.get_asset_content_type(self.asset1.pk)
        # we need to precise here otherwise DDF fails
        self.vulnerability = self.create_instance(models.Vulnerability, project=self.project1, asset=self.asset1,
                                                  content_type=ct, object_id=self.asset1.pk)

    def test_pentester1(self):
        self.login_with_project(self.pentester1, self.project1)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["vulnerabilities"]), 1)

    def test_pentester2(self):
        self.login_with_project(self.pentester2, self.project2)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["vulnerabilities"]), 0)

    def test_readonly(self):
        pass


class VulnerabilityCreateViewTestCase(TestCase, VulnmanTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.url = self.get_url("projects:findings:vulnerability-create")
        self.template = self._create_instance(models.Template)
        self.asset1 = self._create_instance(asset_models.WebApplication, project=self.project1)
        self.asset2 = self._create_instance(asset_models.WebApplication, project=self.project2)
        self.data = {"name": "Testvuln", "template_id": self.template.vulnerability_id, "date_found": "2022-12-01",
                     "f_asset": self.asset1.pk, "status": models.Vulnerability.STATUS_OPEN, "auth_required": True,
                     "user_account": "", "asset_type": asset_models.WebApplication.ASSET_TYPE}

    def test_pentester1(self):
        self.login_with_project(self.pentester1, self.project1)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(models.Vulnerability.objects.with_asset(self.asset1).filter(template=self.template).count(), 1)

    def test_pentester2(self):
        self.login_with_project(self.pentester2, self.project2)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(models.Vulnerability.objects.filter(template=self.template).with_asset(self.asset1).count(), 0)

    def test_readonly(self):
        self.login_with_project(self.read_only1, self.project1)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 403)

    def test_asset_other_project(self):
        self.data["f_asset"] = self.asset2.pk
        self.login_with_project(self.pentester1, self.project1)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["form"].errors), 1)
        self.assertEqual(models.Vulnerability.objects.filter(template=self.template,
                                                             project=self.project1).with_asset(self.asset1).count(), 0)


class VulnerabilityDetailViewTestCase(TestCase, VulnmanTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.asset1 = self._create_instance(asset_models.WebApplication, project=self.project1)
        ct = models.Vulnerability.objects.get_asset_content_type(self.asset1.pk)
        # we need to precise here otherwise DDF fails
        self.vulnerability = self.create_instance(models.Vulnerability, project=self.project1, asset=self.asset1,
                                                  content_type=ct, object_id=self.asset1.pk)
        self.url = self.vulnerability.get_absolute_url()

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

    def test_vendor(self):
        self.client.force_login(self.vendor)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)


class VulnerabilityExportViewTestCase(TestCase, VulnmanTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.asset1 = self._create_instance(asset_models.WebApplication, project=self.project1)
        ct = models.Vulnerability.objects.get_asset_content_type(self.asset1.pk)
        # we need to precise here otherwise DDF fails
        self.vulnerability = self.create_instance(models.Vulnerability, project=self.project1, asset=self.asset1,
                                                  content_type=ct, object_id=self.asset1.pk)
        self.url = self.get_url("projects:findings:vulnerability-export", pk=self.vulnerability.pk)

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


class VulnerabilityUpdateViewTestCase(TestCase, VulnmanTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.asset1 = self.create_instance(asset_models.WebApplication, project=self.project1)
        self.asset2 = self.create_instance(asset_models.WebApplication, project=self.project2)
        ct = models.Vulnerability.objects.get_asset_content_type(self.asset1.pk)
        # we need to precise here otherwise DDF fails
        self.vulnerability = self.create_instance(models.Vulnerability, project=self.project1, asset=self.asset1,
                                                  content_type=ct, object_id=self.asset1.pk)
        self.url = self.get_url("projects:findings:vulnerability-update", pk=self.vulnerability.pk)
        self.data = {"name": "Testvuln1234", "template_id": self.vulnerability.template.vulnerability_id, "date_found": "2022-12-01",
                     "f_asset": str(self.asset1.pk), "status": models.Vulnerability.STATUS_OPEN, "auth_required": True,
                     "user_account": "", "asset_type": asset_models.WebApplication.ASSET_TYPE}

    def test_valid(self):
        self.login_with_project(self.pentester1, self.project1)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(models.Vulnerability.objects.filter(pk=self.vulnerability.pk,
                                                             name=self.data["name"]).count(), 1)

    def test_pentester2(self):
        self.login_with_project(self.pentester2, self.project2)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 404)

    def test_invalid_asset(self):
        self.data["f_asset"] = self.asset2.pk
        self.login_with_project(self.pentester1, self.project1)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(models.Vulnerability.objects.with_asset(self.asset2).count(), 0)

    def test_readonly(self):
        self.login_with_project(self.read_only1, self.project1)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 403)


class VulnerabilityDeleteViewTestCase(TestCase, VulnmanTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.asset1 = self._create_instance(asset_models.WebApplication, project=self.project1)
        ct = models.Vulnerability.objects.get_asset_content_type(self.asset1.pk)
        # we need to precise here otherwise DDF fails
        self.vulnerability = self.create_instance(models.Vulnerability, project=self.project1, asset=self.asset1,
                                                  content_type=ct, object_id=self.asset1.pk)
        self.url = self.vulnerability.get_absolute_delete_url()

    def test_valid(self):
        self.login_with_project(self.pentester1, self.project1)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(models.Vulnerability.objects.filter(pk=self.vulnerability.pk).exists(), False)

    def test_readonly(self):
        self.login_with_project(self.read_only1, self.project1)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 403)

    def test_pentester2(self):
        self.login_with_project(self.pentester2, self.project2)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 404)


class VulnerabilityCopyViewTestCase(TestCase, VulnmanTestCaseMixin):
    def setUp(self):
        self.init_mixin()
        self.vulnerability1 = self.create_instance(models.Vulnerability, project=self.project1)
        self.vulnerability2 = self.create_instance(models.Vulnerability, project=self.project2)
        self.url = self.get_url("projects:findings:vulnerability-copy", pk=self.vulnerability1.pk)

    def test_valid(self):
        self.login_with_project(self.pentester1, self.project1)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(models.Vulnerability.objects.filter(
            project=self.project1, name=self.vulnerability1.name).count(), 2)

    def test_pentester2(self):
        self.login_with_project(self.pentester2, self.project2)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 404)

    def test_customer(self):
        self.login_with_project(self.customer1, self.project1)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 403)

    def test_readonly(self):
        self.login_with_project(self.read_only1, self.project1)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 403)

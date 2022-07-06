from rest_framework.test import APITestCase
from django.urls.exceptions import NoReverseMatch
from vulnman.core.test import VulnmanAPITestCaseMixin
from apps.responsible_disc import models


class RespDiscTestProofOrderViewSet(APITestCase, VulnmanAPITestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.vuln1 = self._create_instance(models.Vulnerability, user=self.pentester1)
        self.proof1 = self._create_instance(models.TextProof, vulnerability=self.vuln1)
        self.proof2 = self._create_instance(models.TextProof, vulnerability=self.vuln1)

    def test_methods_not_allowed(self):
        def raise_url_list():
            # this tests create viewset too
            rurl = self.get_url("api:ui:responsible-disclosure:proof-list")
            self.client.get(rurl)

        self.client.force_login(self.pentester1)
        self.assertRaises(NoReverseMatch, raise_url_list)
        url = self.get_url("api:ui:responsible-disclosure:proof-detail", pk=self.proof1.pk)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 405)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 405)

    def test_update_unauthenticated(self):
        url = self.get_url("api:ui:responsible-disclosure:proof-detail", pk=self.proof1.pk)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

    def test_update_allowed(self):
        url = self.get_url("api:ui:responsible-disclosure:proof-detail", pk=self.proof1.pk)
        data = {"order": 5}
        self.client.force_login(self.pentester1)
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(models.TextProof.objects.filter(order=5, pk=self.proof1.pk).count(), 1)

    def test_update_shared_vendor(self):
        url = self.get_url("api:ui:responsible-disclosure:proof-detail", pk=self.proof1.pk)
        data = {"order": 5}
        self.client.force_login(self.vendor)
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(models.TextProof.objects.filter(order=5, pk=self.proof1.pk).count(), 0)

    def test_update_no_permission(self):
        url = self.get_url("api:ui:responsible-disclosure:proof-detail", pk=self.proof1.pk)
        data = {"order": 5}
        self.client.force_login(self.pentester2)
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, 404)

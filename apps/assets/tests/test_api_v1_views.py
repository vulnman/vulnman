from rest_framework.test import APITestCase
from vulnman.core.test import VulnmanAPITestCaseMixin
from apps.assets import models


class HostViewSetTestCase(APITestCase, VulnmanAPITestCaseMixin):
    def setUp(self):
        self.init_mixin()
        self.data = {"ip": "1.2.3.4"}

    def test_createview(self):
        url = self.get_url("api:v1:assets:host-list")
        response = self.client.post(
            url, self.data, HTTP_AUTHORIZATION="Token %s" % self.token1.key
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["project"], str(self.project1.pk))
        self.assertEqual(models.Host.objects.count(), 1)
        # test duplicates
        response = self.client.post(
            url, self.data, HTTP_AUTHORIZATION="Token %s" % self.token1.key
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(models.Host.objects.count(), 1)

    def test_detailview(self):
        host = self.create_instance(models.Host, project=self.project1)
        url = self.get_url("api:v1:assets:host-detail", pk=str(host.pk))
        response = self.client.get(
            url, HTTP_AUTHORIZATION="Token %s" % self.token1.key
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["project"], str(self.project1.pk))

    def test_listview(self):
        host = self.create_instance(models.Host, project=self.project1)
        self.create_instance(models.Host, project=self.project2)
        url = self.get_url("api:v1:assets:host-list")
        response = self.client.get(
            url, HTTP_AUTHORIZATION="Token %s" % self.token1.key)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("count"), 1)
        self.assertEqual(response.json()["results"][0]["uuid"], str(host.pk))

    def test_updateview(self):
        host = self.create_instance(models.Host, project=self.project1)
        data = {"ip": "10.10.1.255"}
        url = self.get_url("api:v1:assets:host-detail", pk=host.pk)
        response = self.client.patch(url, data, HTTP_AUTHORIZATION="Token %s" % self.token1.key)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(models.Host.objects.filter(ip=data["ip"]).count(), 1)

    def test_updateview_forbidden(self):
        host = self.create_instance(models.Host, project=self.project1)
        data = {"ip": "10.10.1.255"}
        url = self.get_url("api:v1:assets:host-detail", pk=host.pk)
        response = self.client.patch(url, data, HTTP_AUTHORIZATION="Token %s" % self.token2.key)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(models.Host.objects.filter(ip=data["ip"]).count(), 0)

    def test_deleteview(self):
        host = self.create_instance(models.Host, project=self.project1)
        url = self.get_url("api:v1:assets:host-detail", pk=host.pk)
        response = self.delete(url, self.token1)
        self.assertEqual(response.status_code, 204)

    def test_deleteview_forbidden(self):
        host = self.create_instance(models.Host, project=self.project1)
        url = self.get_url("api:v1:assets:host-detail", pk=host.pk)
        response = self.delete(url, self.token2)
        self.assertEqual(response.status_code, 404)


class ServiceViewSetTestCase(APITestCase, VulnmanAPITestCaseMixin):
    def setUp(self):
        self.init_mixin()
        self.host = self.create_instance(models.Host, project=self.project1)
        self.data = {
            "name": "Test Service", "host": str(self.host.pk), "port": 443,
            "protocol": "tcp", "banner": "Test", "state": "open"}

    def test_detailview(self):
        service = self.create_instance(models.Service, project=self.project1)
        url = self.get_url("api:v1:assets:service-detail", pk=service.pk)
        response = self.get(url, self.token1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["uuid"], str(service.pk))

    def test_detailview_forbidden(self):
        service = self.create_instance(models.Service, project=self.project2)
        url = self.get_url("api:v1:assets:service-detail", pk=service.pk)
        response = self.get(url, self.token1)
        self.assertEqual(response.status_code, 404)

    def test_createview(self):
        url = self.get_url("api:v1:assets:service-list")
        response = self.post(url, self.data, self.token1)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["project"], str(self.project1.pk))

    def test_createview_forbidden(self):
        url = self.get_url("api:v1:assets:service-list")
        response = self.post(url, self.data, self.token2)
        # returns 400 because the host is not ours
        self.assertEqual(response.status_code, 400)

    def test_updateview(self):
        service = self.create_instance(models.Service, project=self.project1)
        url = self.get_url("api:v1:assets:service-detail", pk=service.pk)
        response = self.patch(url, self.data, self.token1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(models.Service.objects.filter(host=self.host, name=self.data["name"]).count(), 1)

    def test_updateview_forbidden(self):
        service = self.create_instance(models.Service, project=self.project1)
        url = self.get_url("api:v1:assets:service-detail", pk=service.pk)
        response = self.patch(url, self.data, self.token2)
        self.assertEqual(response.status_code, 404)


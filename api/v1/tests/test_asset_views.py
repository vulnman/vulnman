from rest_framework.test import APITestCase
from api.v1.mixins import VulnmanAPITestCaseMixin
from apps.assets import models


class AgentHostViewSetTestCase(APITestCase, VulnmanAPITestCaseMixin):
    def setUp(self):
        self.init_mixin()

    def test_createview(self):
        token = self.create_project_token(self.project1, self.pentester1)
        data = {"ip": "1.2.3.4"}
        url = self.get_url("api:v1:agents:host-list")
        response = self.client.post(
            url, data, HTTP_AUTHORIZATION="Token %s" % token.key
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["project"], str(self.project1.pk))
        self.assertEqual(models.Host.objects.count(), 1)
        response = self.client.post(
            url, data, HTTP_AUTHORIZATION="Token %s" % token.key
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(models.Host.objects.count(), 1)

    def test_detailview(self):
        token = self.create_project_token(self.project1, self.pentester1)
        host = self.create_instance(models.Host, project=self.project1)
        url = self.get_url("api:v1:agents:host-detail", pk=str(host.pk))
        response = self.client.get(
            url, HTTP_AUTHORIZATION="Token %s" % token.key
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["project"], str(self.project1.pk))

    def test_listview(self):
        token = self.create_project_token(self.project1, self.pentester1)
        host = self.create_instance(models.Host, project=self.project1)
        self.create_instance(models.Host, project=self.project2)
        url = self.get_url("api:v1:agents:host-list")
        response = self.client.get(
            url, HTTP_AUTHORIZATION="Token %s" % token.key)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("count"), 1)
        self.assertEqual(response.json()["results"][0]["uuid"], str(host.pk))

    def test_createview_forbidden(self):
        # TODO: implement
        pass

    def test_updateview(self):
        # TODO: implement
        pass

    def test_updateview_forbidden(self):
        # TODO: implement
        # TODO: check if host can be changed after creation
        pass


class AgentServiceViewSetTestCase(APITestCase, VulnmanAPITestCaseMixin):
    def setUp(self):
        self.init_mixin()

    def test_detailview(self):
        """Test detail view for service
        """
        token = self.create_project_token(self.project1, self.pentester1)
        service = self.create_instance(models.Service, project=self.project1)
        url = self.get_url("api:v1:agents:service-detail", pk=service.pk)
        response = self.client.get(
            url, HTTP_AUTHORIZATION="Token %s" % token.key)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["uuid"], str(service.pk))

    def test_detailview_forbidden(self):
        token = self.create_project_token(self.project1, self.pentester1)
        service = self.create_instance(models.Service, project=self.project2)
        url = self.get_url("api:v1:agents:service-detail", pk=service.pk)
        response = self.client.get(
            url, HTTP_AUTHORIZATION="Token %s" % token.key)
        self.assertEqual(response.status_code, 404)

    def test_createview(self):
        token = self.create_project_token(self.project1, self.pentester1)
        host = self.create_instance(models.Host, project=self.project1)
        data = {
            "name": "Test Service", "host": str(host.pk), "port": 443,
            "protocol": "tcp", "banner": "Test", "state": "open"}
        url = self.get_url("api:v1:agents:service-list")
        response = self.client.post(
            url, data, HTTP_AUTHORIZATION="Token %s" % token.key)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["project"], str(self.project1.pk))

    def test_createview_forbidden(self):
        # TODO: implement
        pass

    def test_updateview(self):
        # TODO: implement
        pass

    def test_updateview_forbidden(self):
        # TODO: implement
        # TODO: check if host can be changed after creation
        pass

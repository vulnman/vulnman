from rest_framework.test import APITestCase
from vulnman.tests.mixins import VulnmanAPITestMixin
from apps.networking.models import Host, Service, Hostname


class HostViewSetTestCase(APITestCase, VulnmanAPITestMixin):
    def setUp(self) -> None:
        self.init_mixin()

    def test_listview(self):
        self._test_project_listview("api:v1:host-list", Host)

    def test_updateview(self):
        payload = {"ip": "10.10.100.1"}
        self._test_project_updateview("api:v1:host-detail", payload, Host)

    def test_createview(self):
        payload = {"ip": "10.10.100.1"}
        self._test_project_createview("api:v1:host-list", payload, Host)

    def test_deleteview(self):
        self._test_project_deleteview("api:v1:host-detail", Host)


class ServiceViewSetTestCase(APITestCase, VulnmanAPITestMixin):
    def setUp(self) -> None:
        self.init_mixin()

    def test_listview(self):
        self._test_project_listview("api:v1:service-list", Service)

    def test_updateview(self):
        payload = {"port": "10666"}
        self._test_project_updateview("api:v1:service-detail", payload, Service)

    def test_createview(self):
        host = self._create_instance(Host, project__creator=self.user1)
        payload = {"port": "80", "protocol": "tcp", "name": "http", "host": str(host.pk)}
        self._test_project_createview("api:v1:service-list", payload, Service)

    def test_deleteview(self):
        self._test_project_deleteview("api:v1:service-detail", Service)


class HostnameViewSetTestCase(APITestCase, VulnmanAPITestMixin):
    def setUp(self) -> None:
        self.init_mixin()

    def test_listview(self):
        self._test_project_listview("api:v1:hostname-list", Hostname)

    def test_updateview(self):
        payload = {"name": "test2.example.com"}
        self._test_project_updateview("api:v1:hostname-detail", payload, Hostname)

    def test_createview(self):
        host = self._create_instance(Host, project__creator=self.user1)
        payload = {"name": "test.example.com", "host": str(host.pk)}
        self._test_project_createview("api:v1:hostname-list", payload, Hostname)

    def test_deleteview(self):
        self._test_project_deleteview("api:v1:hostname-detail", Hostname)

from rest_framework.test import APITestCase
from vulnman.tests.mixins import VulnmanAPITestMixin
from apps.social import models


class CredentialViewSetTestCase(APITestCase, VulnmanAPITestMixin):
    def setUp(self) -> None:
        self.init_mixin()

    def test_listview(self):
        self._test_project_listview("api:v1:credential-list", models.Credential)

    def test_updateview(self):
        payload = {"cleartext_password": "test-password"}
        self._test_project_updateview("api:v1:credential-detail", payload, models.Credential)

    def test_createview(self):
        project = self._create_project("testproject", creator=self.user1)
        payload = {"username": "testuser", "cleartext_password": "password", "location_found": "webroot",
                   "project": str(project.pk)}
        self._test_project_createview("api:v1:credential-list", payload, models.Credential, format='json')

    def test_deleteview(self):
        self._test_project_deleteview("api:v1:credential-detail", models.Credential)

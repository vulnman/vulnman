import base64
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from vulnman.core.test import VulnmanTestCaseMixin
from apps.findings import models


class AddTextProofViewTestCase(TestCase, VulnmanTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.vulnerability = self._create_instance(models.Vulnerability, project=self.project1)
        self.vulnerability2 = self._create_instance(models.Vulnerability, project=self.project2)
        self.url = self.get_url("projects:findings:vulnerability-add-text-proof", pk=self.vulnerability.pk)
        self.data = {"name": "lorem", "description": "myproof", "text": "sometext"}

    def test_pentester1(self):
        self.login_with_project(self.pentester1, self.project1)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(models.TextProof.objects.filter(project=self.project1,
                                                         vulnerability=self.vulnerability).count(), 1)

    def test_pentester2(self):
        self.login_with_project(self.pentester2, self.project2)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(models.TextProof.objects.filter(project=self.project1).count(), 0)

    def test_readonly(self):
        self.login_with_project(self.read_only1, self.project1)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 403)

    def test_other_vulnerability(self):
        self.login_with_project(self.pentester1, self.project1)
        self.url = self.get_url("projects:findings:vulnerability-add-text-proof", pk=self.vulnerability2.pk)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(models.TextProof.objects.filter(project=self.project1).count(), 0)


class TextProofUpdateViewTestCase(TestCase, VulnmanTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.vulnerability = self._create_instance(models.Vulnerability, project=self.project1)
        self.vulnerability2 = self._create_instance(models.Vulnerability, project=self.project2)
        self.proof1 = self._create_instance(models.TextProof, vulnerability=self.vulnerability)
        self.proof2 = self._create_instance(models.TextProof, vulnerability=self.vulnerability2)
        self.data = {"name": "lorem", "description": "myproof", "text": "sometext"}
        self.url = self.get_url("projects:findings:text-proof-update", pk=self.proof1.pk)

    def test_valid(self):
        self.login_with_project(self.pentester1, self.project1)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(models.TextProof.objects.filter(vulnerability=self.vulnerability,
                                                         name=self.data["name"]).count(), 1)

    def test_readonly(self):
        self.login_with_project(self.read_only1, self.project1)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 403)

    def test_pentester2(self):
        self.login_with_project(self.pentester2, self.project2)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 404)


class ImageProofDeleteViewTestCase(TestCase, VulnmanTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.vulnerability = self._create_instance(models.Vulnerability, project=self.project1)
        self.proof = self._create_instance(models.ImageProof, vulnerability=self.vulnerability)
        self.url = self.proof.get_absolute_delete_url()

    def test_valid(self):
        self.login_with_project(self.pentester1, self.project1)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(models.ImageProof.objects.count(), 0)

    def test_pentester2(self):
        self.login_with_project(self.pentester2, self.project2)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(models.ImageProof.objects.count(), 1)

    def test_readonly(self):
        self.login_with_project(self.read_only1, self.project1)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 403)


class TextProofDeleteViewTestCase(TestCase, VulnmanTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.vulnerability = self._create_instance(models.Vulnerability, project=self.project1)
        self.proof = self._create_instance(models.TextProof, vulnerability=self.vulnerability)
        self.url = self.proof.get_absolute_delete_url()

    def test_valid(self):
        self.login_with_project(self.pentester1, self.project1)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(models.TextProof.objects.count(), 0)

    def test_pentester2(self):
        self.login_with_project(self.pentester2, self.project2)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 404)

    def test_readonly(self):
        self.login_with_project(self.read_only1, self.project1)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 403)


class ImageCreateViewTestCase(TestCase, VulnmanTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.vulnerability = self._create_instance(models.Vulnerability, project=self.project1)
        image_content = base64.b64decode(b"iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//"
                                         b"8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg==")
        self.url = self.get_url("projects:findings:vulnerability-add-image-proof", pk=self.vulnerability.pk)
        image = SimpleUploadedFile("file.png", image_content, content_type="image/png")
        self.data = {"image": image, "caption": "test", "name": "test", "description": "hello"}

    def test_valid(self):
        self.login_with_project(self.pentester1, self.project1)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(models.ImageProof.objects.filter(vulnerability=self.vulnerability).count(), 1)

    def test_pentester2(self):
        self.login_with_project(self.pentester2, self.project2)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 404)

    def test_readonly(self):
        self.login_with_project(self.read_only1, self.project1)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 403)


class ImageUpdateViewTestCase(TestCase, VulnmanTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.vulnerability = self._create_instance(models.Vulnerability, project=self.project1)
        image_content = base64.b64decode(b"iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//"
                                         b"8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg==")
        image = SimpleUploadedFile("file.png", image_content, content_type="image/png")
        self.data = {"image": image, "caption": "test", "name": "test", "description": "hello"}
        self.proof = self._create_instance(models.ImageProof, vulnerability=self.vulnerability)
        self.url = self.get_url("projects:findings:image-proof-update", pk=self.proof.pk)

    def test_valid(self):
        self.login_with_project(self.pentester1, self.project1)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(models.ImageProof.objects.filter(pk=self.proof.pk, name=self.data["name"],
                                                          vulnerability=self.vulnerability).count(), 1)

    def test_pentester2(self):
        self.login_with_project(self.pentester2, self.project2)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 404)

    def test_readonly(self):
        self.login_with_project(self.read_only1, self.project1)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 403)



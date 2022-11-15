import base64
import io
import zipfile

from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
from vulnman.core.test import VulnmanTestCaseMixin
from apps.responsible_disc import models


class AdvisoryExportViewTestCase(TestCase, VulnmanTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.vulnerability = self.create_instance(models.Vulnerability, user=self.pentester1)
        self.url = self.get_url("responsible_disc:vulnerability-export-advisory", pk=self.vulnerability.pk)

    def test_valid(self):
        self.client.force_login(self.pentester1)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get("Content-Disposition"), 'attachment; filename="advisory.md"')
        self.assertIn(b"# Timeline", response.content)

    def test_pentester2(self):
        self.client.force_login(self.pentester2)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_vendor(self):
        self.client.force_login(self.vendor)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_vendor_unshared(self):
        self.assign_perm("responsible_disc.view_vulnerability", obj=self.vulnerability, user_or_group=self.vendor)
        self.client.force_login(self.vendor)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get("Content-Disposition"), 'attachment; filename="advisory.md"')

    def test_zipfile_export(self):
        self.client.force_login(self.pentester1)
        # upload image proof to disk
        image_content = base64.b64decode(b"iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//"
                                         b"8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg==")
        image = SimpleUploadedFile("file.png", image_content, content_type="image/png")
        data = {"image": image, "caption": "test", "name": "test", "description": "hello"}
        response = self.client.post(self.get_url("responsible_disc:image-proof-create", pk=self.vulnerability.pk), data)
        self.assertEqual(response.status_code, 302)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get("Content-Disposition"), 'attachment; filename="advisory.zip"')
        f = io.BytesIO(response.content)
        zip_file = zipfile.ZipFile(f, "r")
        self.assertIsNone(zip_file.testzip())
        self.assertIn("advisory.md", zip_file.namelist())
        self.assertEqual(len(zip_file.namelist()), 2)

    def test_custom_advisory(self):
        pass

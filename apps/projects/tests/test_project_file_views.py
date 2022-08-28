import base64

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from vulnman.core.test import VulnmanTestCaseMixin
from apps.projects import models


class ProjectFileListViewTestCase(TestCase, VulnmanTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.file1 = self.create_instance(models.ProjectFile, project=self.project1)
        self.file2 = self.create_instance(models.ProjectFile, project=self.project2)
        self.url = self.get_url("projects:file-list")

    def test_status_code(self):
        self.login_with_project(self.pentester1, self.project1)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["object_list"]), 1)
        self.assertEqual(response.context["object_list"][0], self.file1)

    def test_vendor(self):
        self.client.force_login(self.vendor)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)


class ProjectFileCreateViewTestCase(TestCase, VulnmanTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.url = self.get_url("projects:file-create")
        image_content = base64.b64decode(b"iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//"
                                         b"8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg==")
        test_file = SimpleUploadedFile("file.png", image_content, content_type="image/png")
        self.data = {"name": "testfile", "file": test_file}

    def test_status_code(self):
        self.login_with_project(self.pentester1, self.project1)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(models.ProjectFile.objects.filter(project=self.project1).count(), 1)

    def test_vendor(self):
        self.client.force_login(self.vendor)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 403)

    def test_readonly(self):
        self.login_with_project(self.read_only1, self.project1)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 403)


class ProjectFileDetailViewTestCase(TestCase, VulnmanTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.file1 = self.create_instance(models.ProjectFile, project=self.project1)
        self.file2 = self.create_instance(models.ProjectFile, project=self.project2)

    # def test_status_code(self):
    # TODO: implement
    #    self.login_with_project(self.pentester1, self.project1)
    #    response = self.client.get(self.file1.get_absolute_url())
    #    self.assertEqual(response.status_code, 200)

    def test_vendor(self):
        self.client.force_login(self.vendor)
        response = self.client.get(self.file1.get_absolute_url())
        self.assertEqual(response.status_code, 403)

    def test_read_only(self):
        # implement me
        pass

    def test_foreign_project(self):
        self.login_with_project(self.pentester2, self.project2)
        response = self.client.get(self.file1.get_absolute_url())
        self.assertEqual(response.status_code, 404)


class ProjectFileDeleteViewTestCase(TestCase, VulnmanTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.file1 = self.create_instance(models.ProjectFile, project=self.project1)
        self.file2 = self.create_instance(models.ProjectFile, project=self.project2)

    def test_status_code(self):
        self.login_with_project(self.pentester1, self.project1)
        response = self.client.post(self.file1.get_absolute_delete_url(), data={})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("projects:file-list"))
        self.assertEqual(models.ProjectFile.objects.filter(pk=self.file1.pk).count(), 0)

    def test_foreign_project(self):
        self.login_with_project(self.pentester2, self.project2)
        response = self.client.post(self.file1.get_absolute_delete_url(), data={})
        self.assertEqual(response.status_code, 404)

    def test_readonly(self):
        self.login_with_project(self.read_only1, self.project1)
        response = self.client.post(self.file1.get_absolute_delete_url(), data={})
        self.assertEqual(response.status_code, 403)

    def test_vendor(self):
        self.client.force_login(self.vendor)
        response = self.client.post(self.file1.get_absolute_delete_url(), data={})
        self.assertEqual(response.status_code, 403)

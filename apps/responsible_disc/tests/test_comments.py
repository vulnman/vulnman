from django.test import TestCase
from guardian.shortcuts import assign_perm
from vulnman.tests.mixins import VulnmanTestMixin
from apps.responsible_disc import models


class CommentViewTestCase(TestCase, VulnmanTestMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.vuln1 = self._create_instance(models.Vulnerability, user=self.pentester1)

    def test_comment_list(self):
        comment = self._create_instance(models.VulnerabilityComment, vulnerability=self.vuln1, creator=self.pentester1)
        url = self.get_url("responsible_disc:comment-list", pk=self.vuln1.pk)
        # permission denied
        self.client.force_login(self.pentester2)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        # allowed
        self.client.force_login(self.pentester1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["comments"].count(), 1)

    def test_comment_create(self):
        url = self.get_url("responsible_disc:comment-create", pk=self.vuln1.pk)
        data = {"text": "lorem ipsum"}
        # permission denied
        self.client.force_login(self.pentester2)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 403)
        # allowed
        self.client.force_login(self.pentester1)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(models.VulnerabilityComment.objects.filter(
            text=data["text"],
            vulnerability=self.vuln1).count(), 1)

    def test_comment_shared(self):
        url = self.get_url("responsible_disc:comment-create", pk=self.vuln1.pk)
        data = {"text": "lorem ipsum"}
        assign_perm("responsible_disc.add_comment", user_or_group=self.pentester2, obj=self.vuln1)
        self.client.force_login(self.pentester2)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(models.VulnerabilityComment.objects.filter(text=data["text"]).count(), 1)

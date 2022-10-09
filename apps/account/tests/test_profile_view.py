from django.test import TestCase
from django.urls import reverse
from django.conf import settings
from vulnman.core.test import VulnmanTestCaseMixin
from apps.account import models


class ProfileViewTestCase(TestCase, VulnmanTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()

    def test_status_code_pentester(self):
        url = self.get_url("account:user-profile", slug=self.pentester1.username)
        self.client.force_login(self.pentester1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_status_code_vendor(self):
        vendor = self._create_user("testvendor", "changeme", user_role=models.User.USER_ROLE_VENDOR)
        url = self.get_url("account:user-profile", slug=vendor.username)
        self.client.force_login(vendor)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_public_profile_pentester(self):
        url = self.get_url("account:user-profile", slug=self.pentester1.username)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["user"], self.pentester1)

    def test_private_profile_pentester(self):
        url = self.get_url("account:user-profile", slug=self.pentester1.username)
        self.pentester1.profile.is_public = False
        self.pentester1.profile.save()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This profile is not public!")
        self.client.force_login(self.pentester2)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This profile is not public!")

    def test_private_profile_vendor(self):
        vendor = self._create_user("testvendor", "changeme", user_role=models.User.USER_ROLE_VENDOR)
        url = self.get_url("account:user-profile", slug=vendor.username)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


class ProfileUpdateViewTestCase(TestCase, VulnmanTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()

    def test_status_code(self):
        url = self.get_url("account:profile-update")
        data = {"is_public": False, 'first_name': "Testuser", "last_name": "Testlastname"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse(settings.LOGIN_URL) + "?next=" + url)
        self.client.force_login(self.pentester1)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(models.User.objects.filter(
            pentester_profile__is_public=False, pk=self.pentester1.pk, last_name=data["last_name"]).count(), 1)

    def test_vendor_profile_update(self):
        url = self.get_url("account:profile-update")
        data = {"is_public": False, 'first_name': "Testuser", "last_name": "Testlastname"}
        self.client.force_login(self.vendor)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(models.User.objects.filter(
            pk=self.vendor.pk, first_name=data["first_name"]).count(), 0)

    def test_only_active_users(self):
        self.pentester1.is_active = False
        self.pentester1.save()
        url = self.get_url("account:profile-update")
        data = {"is_public": False, 'first_name': "Testuser", "last_name": "Testlastname"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse(settings.LOGIN_URL) + "?next=" + url)
        self.client.force_login(self.pentester1)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(models.User.objects.filter(
            pentester_profile__is_public=False, pk=self.pentester1.pk, last_name=data["last_name"]).count(), 0)


class CustmomerUpdateViewTestCase(TestCase, VulnmanTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.url = self.get_url("account:customer-profile-update")
        self.data = {"last_name": "Test123", "first_name": "FirstTest123"}

    def test_status_code(self):
        self.client.force_login(self.customer1)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(models.User.objects.filter(pk=self.customer1.pk, last_name=self.data["last_name"]).count(), 1)

    def test_other_role(self):
        self.client.force_login(self.pentester1)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 404)


class AccountDeleteViewTestCase(TestCase, VulnmanTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.url = self.get_url("account:delete")
        self.data = {}

    def test_status_code_customer(self):
        self.client.force_login(self.customer1)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(models.User.objects.filter(pk=self.customer1.pk).count(), 0)

    def test_status_code_vendor(self):
        self.client.force_login(self.vendor)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(models.User.objects.filter(pk=self.vendor.pk).count(), 0)

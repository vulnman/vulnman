from django.test import TestCase
from django.urls import reverse
from vulnman.tests.mixins import VulnmanTestMixin
from apps.projects import models


class ProjectTests(TestCase, VulnmanTestMixin):
    def setUp(self):
        self.init_mixin()

    def test_listview(self):
        response = self.client.get(reverse('projects:project-list'))
        self.assertEqual(response.status_code, 302)
        project1 = self._create_project("testproject", creator=self.user1)
        self._create_project("anotherone", creator=self.user2)
        self.client.force_login(self.user1)
        response = self.client.get(reverse('projects:project-list'))
        self.assertEqual(len(response.context['projects']), 1)
        self.assertEqual(response.context['projects'].get(), project1)

    def test_detailview(self):
        project = self._create_project("testproject", creator=self.user1)
        self.client.force_login(self.user2)
        response = self.client.get(reverse('projects:project-detail', kwargs={'pk': project.pk}))
        self.assertEqual(response.status_code, 404)
        self.client.force_login(self.user1)
        response = self.client.get(reverse('projects:project-detail', kwargs={'pk': project.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['project'], project)


class ProjectMemberTests(TestCase, VulnmanTestMixin):
    def setUp(self) -> None:
        self.init_mixin()

    def test_listview(self):
        url = self.get_url("projects:project-member-list")
        self._test_unauthenticated_aceess(url)
        # test as creator
        project = self._create_project("testcaseproject", creator=self.user1)
        new_user = self._create_user("memberuser", "changeme")
        project.projectmember_set.add(self._create_instance(models.ProjectMember, role="read-only", user=new_user))
        self.assertEqual(project.projectmember_set.count(), 1)
        self.login_with_project(self.user1, project)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context_data.get('project_members')), 1)
        # test as not creator
        self.login_with_project(self.user2, project)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_createview(self):
        url = self.get_url("projects:project-add-member")
        project = self._create_project("testcaseproject", creator=self.user1)
        new_user = self._create_user("jdoe", "changeme")
        payload = {"role": "read-only", "email": "jdoe@example.com"}
        # test as creator
        self.login_with_project(self.user1, project)
        response = self.client.post(url, payload, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(models.ProjectMember.objects.count(), 1)
        self.assertEqual(models.Project.objects.filter(projectmember__user=new_user).count(), 1)
        self.assertEqual(models.ProjectMember.objects.first().role, "read-only")
        # test as not creator
        self.login_with_project(self.user2, project)
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, 403)

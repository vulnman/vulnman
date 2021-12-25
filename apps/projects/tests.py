from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from vulnman.tests.mixins import VulnmanTestMixin
from apps.projects import models


class ProjectTests(TestCase, VulnmanTestMixin):
    def setUp(self):
        self.init_mixin()

    def test_listview(self):
        response = self.client.get(reverse('projects:project-list'))
        self.assertEqual(response.status_code, 302)
        project1 = self._create_project(creator=self.user1)
        self.assign_perm("projects.view_project", self.pentester, project1)
        self._create_project(creator=self.user2)
        self.client.force_login(self.pentester)
        response = self.client.get(reverse('projects:project-list'))
        self.assertEqual(len(response.context['projects']), 1)
        self.assertEqual(response.context['projects'].get(), project1)

    def test_detailview(self):
        project = self._create_project(creator=self.manager)
        # test without permission
        self.client.force_login(self.user2)
        response = self.client.get(reverse('projects:project-detail', kwargs={'pk': project.pk}))
        self.assertEqual(response.status_code, 404)
        # test with permission
        self.client.force_login(self.pentester)
        self.assign_perm("projects.view_project", self.pentester, project)
        response = self.client.get(reverse('projects:project-detail', kwargs={'pk': project.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['project'], project)

    def test_createview(self):
        url = self.get_url("projects:project-create")
        client = self._create_instance(models.Client)
        payload = {"client": str(client.pk), "start_date": timezone.now().date(),
                   "end_date": timezone.now().date() + timezone.timedelta(days=1),
                   "scope_set-TOTAL_FORMS": "1", "scope_set-0-uuid": "",
                   "scope_set-0-project": "",
                   "scope_set-0-name": "Test Scope", "scope_set-0-DELETE": "",
                   "scope_set-MAX_NUM_FORMS": "4",
                   "scope_set-INITIAL_FORMS": "0", "scope_set-MIN_NUM_FORMS": "0"
                   }
        # test pentester not allowed to create projects
        self.client.force_login(self.pentester)
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, 403)
        # test as manager
        self.client.force_login(self.manager)
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(models.Project.objects.count(), 1)

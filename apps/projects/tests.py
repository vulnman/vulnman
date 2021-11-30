from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from ddf import G
from apps.projects import models


class ProjectTests(TestCase):
    def setUp(self):
        self.user1 = G(User)
        self.user2 = G(User)

    def test_unauth_project_list(self):
        response = self.client.get(reverse('projects:project-list'))
        self.assertEqual(response.status_code, 302)

    def test_auth_project_list(self):
        project1 = G(models.Project, creator=self.user1)
        G(models.Project, creator=self.user2)
        self.client.force_login(self.user1)
        response = self.client.get(reverse('projects:project-list'))
        self.assertEqual(len(response.context['projects']), 1)
        self.assertEqual(response.context['projects'].get(), project1)

    def test_unauth_project_detail(self):
        project1 = G(models.Project, creator=self.user1)
        self.client.force_login(self.user2)
        response = self.client.get(reverse('projects:project-detail', kwargs={'pk': project1.pk}))
        self.assertEqual(response.status_code, 404)

    def test_auth_project_detail(self):
        project1 = G(models.Project, creator=self.user1)
        self.client.force_login(self.user1)
        response = self.client.get(reverse('projects:project-detail', kwargs={'pk': project1.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['project'], project1)

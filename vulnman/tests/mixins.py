from django.contrib.auth.models import Group
from django.utils import timezone
from django.conf import settings
from django.urls import reverse_lazy
from apps.projects.models import Project, Client, ProjectContributor
from ddf import G
from guardian.shortcuts import assign_perm
from apps.account.models import User
import warnings


class VulnmanTestMixin(object):
    def init_mixin(self):
        warnings.warn("Use `vulnman.core.test.VulnmanTestCaseMixin` instead!")
        self.user1 = self._create_user("dummyuser1", "changeme")
        self.user2 = self._create_user("dummyuser2", "changeme")
        self.pentester1 = self._create_user("pentester", "changeme", is_pentester=True)
        self.pentester2 = self._create_user("pentester2", "changeme", is_pentester=True)
        self.read_only1 = self._create_user("readonly1", "changeme")
        self.manager = self._create_user("manager", "changeme")
        self.manager.groups.add(Group.objects.get(name="Management"))
        # self.pentester1.groups.add(Group.objects.get(name="Pentesters"))
        # self.pentester2.groups.add(Group.objects.get(name="Pentesters"))
        self.project1 = self._create_project(creator=self.pentester1)
        self.project2 = self._create_project(creator=self.pentester2)
        self.add_contributor(self.read_only1, self.project1, role=ProjectContributor.ROLE_READ_ONLY)

    def add_contributor(self, user, project, role=ProjectContributor.ROLE_PENTESTER):
        return ProjectContributor.objects.create(user=user, project=project, role=role)

    def _create_user(self, username, password, is_staff=False, **kwargs):
        email = "%s@example.com" % username
        return User.objects.create_user(username, password=password, is_staff=is_staff, email=email, **kwargs)

    def assign_perm(self, perm, user_or_group, obj=None):
        assign_perm(perm, user_or_group=user_or_group, obj=obj)

    def _create_project(self, client=None, creator=None):
        if not client:
            client = self._create_instance(Client)
        return Project.objects.create(creator=creator, client=client, start_date=timezone.now(),
                                      end_date=timezone.now())

    def get_url(self, endpoint, **kwargs):
        return reverse_lazy(endpoint, kwargs=kwargs)

    def _create_instance(self, obj_class, **kwargs):
        return G(obj_class, **kwargs)

    def _set_session_variable(self, key, value):
        session = self.client.session
        session[key] = value
        session.save()

    def login_with_project(self, user, project):
        self.client.force_login(user)
        self._set_session_variable("project_pk", str(project.pk))

    def _test_unauthenticated_aceess(self, url, expected_status_code=403):
        response = self.client.get(url, follow=True)
        login_url = self.get_url(settings.LOGIN_URL)
        self.assertEqual(len(response.redirect_chain), 1)
        self.assertEqual(str(login_url) in str(response.redirect_chain[0][0]), True)
        self.client.force_login(self.user1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, expected_status_code)

    def _test_foreign_access(self, url, foreign_user, project):
        self.login_with_project(foreign_user, project)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

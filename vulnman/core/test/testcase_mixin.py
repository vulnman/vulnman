from django.contrib.auth.models import Group
from django.utils import timezone
from django.urls import reverse_lazy
from apps.projects.models import Project, Client, ProjectContributor
from ddf import G
from guardian.shortcuts import assign_perm
from apps.account.models import User


class VulnmanTestCaseMixin(object):
    def init_mixin(self):
        self.user1 = self._create_user("dummyuser1", "changeme")
        self.user2 = self._create_user("dummyuser2", "changeme")
        self.pentester1 = self._create_user("pentester", "changeme", is_pentester=True)
        self.pentester2 = self._create_user("pentester2", "changeme", is_pentester=True)
        self.read_only1 = self._create_user("readonly1", "changeme")
        self.manager = self._create_user("manager", "changeme")
        self.manager.groups.add(Group.objects.get(name="Management"))
        self.project1 = self._create_project(creator=self.pentester1)
        self.project2 = self._create_project(creator=self.pentester2)
        self.add_contributor(self.read_only1, self.project1, role=ProjectContributor.ROLE_READ_ONLY)
        self.vendor = self._create_user("testvendor1", "changeme", is_vendor=True)

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

from django.contrib.auth.models import Group
from django.urls import reverse_lazy
from django.utils import timezone
from ddf import G
from apps.projects.models import Project, Client, ProjectContributor
from apps.account.models import User


class CoreObjectsTestCaseMixin(object):
    def init_mixin(self):
        self.pentester1 = self._create_user("pentester", "changeme")
        self.pentester2 = self._create_user("pentester2", "changeme")
        self.pentester1.groups.add(Group.objects.get(name="Pentesters"))
        self.pentester2.groups.add(Group.objects.get(name="Pentesters"))
        self.project1 = self._create_project(creator=self.pentester1)
        self.project2 = self._create_project(creator=self.pentester2)

    def _create_user(self, username, password, is_staff=False):
        """
        create a new user
        """
        email = "%s@example.com" % username
        return User.objects.create_user(username, password=password, is_staff=is_staff, email=email)

    def _create_project(self, client=None, creator=None):
        """
        create a project
        """
        if not client:
            client = self._create_instance(Client)
        return Project.objects.create(creator=creator, client=client, start_date=timezone.now(),
                                      end_date=timezone.now())

    def _create_instance(self, obj_class, **kwargs):
        return G(obj_class, **kwargs)

    def _add_contributor(self, user, project, role=ProjectContributor.ROLE_PENTESTER):
        return ProjectContributor.objects.create(user=user, project=project, role=role)

    def get_url(self, endpoint, **kwargs):
        return reverse_lazy(endpoint, kwargs=kwargs)


class SessionAuthHelperTestCaseMixin(object):
    # helper to allow easy login. set the current active project session
    def _set_session_variable(self, key, value):
        session = self.client.session
        session[key] = value
        session.save()

    def login_with_project(self, user, project):
        self.client.force_login(user)
        self._set_session_variable("project_pk", str(project.pk))

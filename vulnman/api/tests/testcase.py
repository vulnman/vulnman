from uuid import uuid4
from django.contrib.auth.models import User, Group
from django.urls import reverse_lazy
from guardian.shortcuts import assign_perm
from ddf import G
from apps.projects.models import Project


class VulnmanAPITestCaseMixin(object):
    def init_mixin(self):
        self.project_pentester = self.create_user("pentester1", "changeme")
        self.denied_pentester = self.create_user("pentester2", "changeme")
        self.project_pentester.groups.add(Group.objects.get(name="pentester"))
        self.denied_pentester.groups.add(Group.objects.get(name="pentester"))
        self.project = self.create_project(creator=self.project_pentester)
        # self.assign_pentester_permissions(self.project_pentester, self.project)

    def create_user(self, username, password, is_staff=False):
        email = "{username}@example.com".format(username=username)
        return User.objects.create_user(
            username, password=password, is_staff=is_staff, email=email)

    def get_url(self, endpoint, **kwargs):
        return reverse_lazy(endpoint, kwargs=kwargs)

    def create_instance(self, obj_class, **kwargs):
        return G(obj_class, **kwargs)

    def create_project(self, **kwargs):
        return self.create_instance(Project, uuid=uuid4(), **kwargs)

    def assign_permission(self, perm, user_or_group, obj=None):
        assign_perm(perm, user_or_group=user_or_group, obj=obj)

    def assign_pentester_permissions(self, user, project):
        self.assign_permission("projects.view_project", user, project)
        self.assign_permission("projects.change_project", user, project)
        self.assign_permission("projects.delete_project", user, project)

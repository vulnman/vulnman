from django.contrib.auth import PermissionDenied
from django.forms import ModelForm
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from guardian.shortcuts import get_objects_for_user
from apps.projects.models import Project


class ProjectMixin(LoginRequiredMixin, UserPassesTestMixin):

    def get_objects_for_user(self, perm, obj, use_groups=False):
        return get_objects_for_user(self.request.user, perm, obj, use_groups=use_groups, accept_global_perms=False, with_superuser=False)

    def get_project(self):
        if not self.request.session.get('project_pk'):
            return None
        project = Project.objects.get(pk=self.request.session["project_pk"])
        if self.request.user.has_perm("view_project", project):
            return project
        return None

    def test_func(self):
        project = self.get_project()
        if not project:
            raise PermissionDenied
        if not project.is_contributor(self.request.user):
            raise PermissionDenied
        if self.request.method in ["POST"] and self.request.user.has_perm("change_project", project):
            return True
        elif self.request.method in ["GET"] and self.request.user.has_perm("view_project", project):
            return True
        return False
        

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = self.get_project()
        return context

    def form_valid(self, form):
        if not isinstance(form, ModelForm):
            # Not a ModelForm do not save the form
            return super().form_valid(form)
        form.instance.project.save()
        return super().form_valid(form)

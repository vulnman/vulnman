from django.contrib.auth import PermissionDenied
from django.db.models import Q
from django.forms import ModelForm
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from apps.projects.models import Project


class ProjectMixin(LoginRequiredMixin, UserPassesTestMixin):
    allowed_project_roles = []

    def get_project(self):
        if not self.request.session.get('project_pk'):
            return None
        if Project.objects.filter(pk=self.request.session['project_pk']).filter(
                Q(creator=self.request.user) | Q(projectmember__user=self.request.user,
                                                 projectmember__role__in=self.allowed_project_roles)).exists():
            return Project.objects.get(pk=self.request.session['project_pk'])
        return None

    def test_func(self):
        project = self.get_project()
        if project:
            return True
        raise PermissionDenied

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = self.get_project()
        return context

    def form_valid(self, form):
        if not isinstance(form, ModelForm):
            print("no modelform")
            return super().form_valid(form)
        form.instance.project.save()
        return super().form_valid(form)

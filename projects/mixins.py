from django.contrib.auth import PermissionDenied
from django.forms import ModelForm
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from projects.models import Project


class ProjectMixin(LoginRequiredMixin, UserPassesTestMixin):

    def get_project(self):
        if not self.request.session.get('project_pk'):
            return None
        if Project.objects.filter(creator=self.request.user, pk=self.request.session['project_pk']):
            return Project.objects.get(pk=self.request.session['project_pk'])
        return None

    def test_func(self):
        if self.get_project():
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

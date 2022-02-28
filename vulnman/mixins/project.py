from django.contrib.auth import PermissionDenied
from django.forms import ModelForm
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from guardian.shortcuts import get_objects_for_user
from apps.projects.models import Project


class ProjectMixin(LoginRequiredMixin, UserPassesTestMixin):

    def get_objects_for_user(self, perm, obj, use_groups=False):
        return get_objects_for_user(self.request.user, perm, obj, use_groups=use_groups)

    def get_project(self):
        if not self.request.session.get('project_pk'):
            return None
        session_pk = self.request.session["project_pk"]
        projects = get_objects_for_user(self.request.user, "pentest_project", Project.objects.filter(pk=session_pk),
                                        use_groups=False)
        if projects.exists():
            return projects.get()
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
            # Not a ModelForm do not save the form
            return super().form_valid(form)
        form.instance.project.save()
        return super().form_valid(form)

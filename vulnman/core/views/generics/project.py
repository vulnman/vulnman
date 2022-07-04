from django.core.exceptions import ImproperlyConfigured
from vulnman.core.mixins import ObjectPermissionRequiredMixin, ProjectMixin
from vulnman.core.views.generics.vulnman import (
    VulnmanAuthDetailView, VulnmanAuthListView, VulnmanAuthCreateView, VulnmanAuthUpdateView, VulnmanAuthDeleteView,
    VulnmanAuthCreateWithInlinesView, VulnmanAuthTemplateView, VulnmanAuthFormView,
    VulnmanAuthRedirectView
)


class ProjectCreateView(ObjectPermissionRequiredMixin, ProjectMixin, VulnmanAuthCreateView):
    """
    Create an object with relation to a project
    """
    permission_required = ["projects.change_project"]
    return_403 = True
    raise_exception = True

    def get_permission_object(self):
        return self.get_project()

    def form_valid(self, form):
        form.instance.creator = self.request.user
        form.instance.project = self.get_project()
        return super().form_valid(form)


class ProjectDetailView(ObjectPermissionRequiredMixin, ProjectMixin, VulnmanAuthDetailView):
    """
    DetailView for an object that belongs to a project of mine
    """
    permission_required = ["projects.view_project"]
    return_403 = True
    raise_exception = True

    def get_permission_object(self):
        return self.get_project()

    def get_queryset(self):
        if self.queryset is None:
            if self.model:
                return self.model._default_manager.filter(project=self.get_project())
            else:
                raise ImproperlyConfigured(
                    "%(cls)s is missing a QuerySet. Define "
                    "%(cls)s.model, %(cls)s.queryset, or override "
                    "%(cls)s.get_queryset()." % {
                        'cls': self.__class__.__name__
                    }
                )
        return self.queryset.filter(project=self.get_project())


class ProjectListView(ObjectPermissionRequiredMixin, ProjectMixin, VulnmanAuthListView):
    """
    ListView for objects related to a project of mine
    """
    paginate_by = 25
    permission_required = ["projects.view_project"]
    raise_exception = True
    return_403 = True

    def get_permission_object(self):
        return self.get_project()

    def get_queryset(self):
        qs = super().get_queryset()
        # return qs.filter(project=self.get_project())
        return qs


class ProjectDeleteView(ObjectPermissionRequiredMixin, ProjectMixin, VulnmanAuthDeleteView):
    permission_required = ["projects.delete_project"]
    return_403 = True
    raise_exception = True

    def get_permission_object(self):
        return self.get_project()


class ProjectUpdateView(ObjectPermissionRequiredMixin, ProjectMixin, VulnmanAuthUpdateView):
    permission_required = ["projects.change_project"]
    return_403 = True
    raise_exception = True

    def get_permission_object(self):
        return self.get_project()


class ProjectCreateWithInlinesView(ProjectMixin, VulnmanAuthCreateWithInlinesView):
    # TODO: do permission checks
    def form_valid(self, form):
        form.instance.project = self.get_project()
        form.instance.creator = self.request.user
        return super().form_valid(form)

    def forms_valid(self, form, inlines):
        response = self.form_valid(form)
        for formset in inlines:
            instances = formset.save(commit=False)
            for instance in instances:
                instance.project = self.get_project()
                instance.save()
        return response


class ProjectTemplateView(ObjectPermissionRequiredMixin, ProjectMixin, VulnmanAuthTemplateView):
    # TODO: legacy?
    pass


class ProjectFormView(ObjectPermissionRequiredMixin, ProjectMixin, VulnmanAuthFormView):
    def form_valid(self, form):
        return super().form_valid(form)


class ProjectRedirectView(ProjectMixin, VulnmanAuthRedirectView):
    pass

from django.core.exceptions import ImproperlyConfigured
from vulnman.core.mixins import ObjectPermissionRequiredMixin, ProjectMixin
from vulnman.core.views.generics.vulnman import (
    VulnmanAuthDetailView, VulnmanAuthListView, VulnmanAuthCreateView, VulnmanAuthUpdateView, VulnmanAuthDeleteView,
    VulnmanAuthFormView,
    VulnmanAuthRedirectView
)


class ProjectCreateView(ObjectPermissionRequiredMixin, ProjectMixin, VulnmanAuthCreateView):
    """
    Create an object with relation to a project
    """
    permission_required = ["projects.change_project"]
    return_403 = True
    raise_exception = True
    page_title = "Create"
    breadcrumbs = []

    def get_breadcrumbs(self):
        return self.breadcrumbs.copy()

    def get_context_data(self, **kwargs):
        kwargs["page_title"] = self.page_title
        kwargs["breadcrumbs"] = self.get_breadcrumbs()
        return super().get_context_data(**kwargs)

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
    page_title = "Update"
    breadcrumbs = []

    def get_breadcrumbs(self):
        return self.breadcrumbs.copy()

    def get_permission_object(self):
        return self.get_project()

    def get_context_data(self, **kwargs):
        kwargs["page_title"] = self.page_title
        kwargs["breadcrumbs"] = self.get_breadcrumbs()
        return super().get_context_data(**kwargs)


class ProjectFormView(ObjectPermissionRequiredMixin, ProjectMixin, VulnmanAuthFormView):
    def form_valid(self, form):
        return super().form_valid(form)


class ProjectRedirectView(ProjectMixin, VulnmanAuthRedirectView):
    pass

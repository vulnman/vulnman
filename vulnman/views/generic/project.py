from django.db.models import QuerySet
from django.core.exceptions import ImproperlyConfigured
from apps.projects.mixins import ProjectMixin
from vulnman.views.generic.vulnman import (
    VulnmanAuthDetailView, VulnmanAuthListView, VulnmanAuthCreateView, VulnmanAuthUpdateView, VulnmanAuthDeleteView,
    VulnmanAuthCreateWithInlinesView, VulnmanAuthUpdateWithInlinesView, VulnmanAuthTemplateView, VulnmanAuthFormView
)


class ProjectCreateView(ProjectMixin, VulnmanAuthCreateView):
    """
    Create an object with relation to a project
    """
    def form_valid(self, form):
        form.instance.creator = self.request.user
        form.instance.project = self.get_project()
        return super().form_valid(form)


class ProjectDetailView(ProjectMixin, VulnmanAuthDetailView):
    """
    DetailView for an object that belongs to a project of mine
    """
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


class ProjectListView(ProjectMixin, VulnmanAuthListView):
    """
    ListView for objects related to a project of mine
    """
    paginate_by = 25

    def get_queryset(self):
        if self.queryset is not None:
            queryset = self.queryset
            if isinstance(queryset, QuerySet):
                queryset = queryset.filter(project=self.get_project())
        elif self.model is not None:
            queryset = self.model._default_manager.filter(project=self.get_project())
        else:
            raise ImproperlyConfigured(
                "%(cls)s is missing a QuerySet. Define "
                "%(cls)s.model, %(cls)s.queryset, or override "
                "%(cls)s.get_queryset()." % {
                    'cls': self.__class__.__name__
                }
            )
        ordering = self.get_ordering()
        if ordering:
            if isinstance(ordering, str):
                ordering = (ordering,)
            queryset = queryset.order_by(*ordering)
        return queryset


class ProjectDeleteView(ProjectMixin, VulnmanAuthDeleteView):
    pass


class ProjectUpdateView(ProjectMixin, VulnmanAuthUpdateView):
    pass


class ProjectCreateWithInlinesView(ProjectMixin, VulnmanAuthCreateWithInlinesView):
    def form_valid(self, form):
        form.instance.project = self.get_project()
        form.instance.creator = self.request.user
        return super().form_valid(form)


class ProjectUpdateWithInlinesView(ProjectMixin, VulnmanAuthUpdateWithInlinesView):
    pass


class ProjectTemplateView(ProjectMixin, VulnmanAuthTemplateView):
    pass


class ProjectFormView(ProjectMixin, VulnmanAuthFormView):
    def form_valid(self, form):
        return super().form_valid(form)

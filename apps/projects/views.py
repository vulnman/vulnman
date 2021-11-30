from django.http import Http404
from django.utils.translation import gettext as _
from django.urls import reverse_lazy
from django.conf import settings
from django.utils import timezone
from django.db.models import Count
from apps.projects import models
from apps.projects import forms
from vulnman.views import generic


class ProjectList(generic.VulnmanAuthListView):
    template_name = "projects/project_list.html"
    context_object_name = "projects"

    def get_queryset(self):
        return models.Project.objects.filter(creator=self.request.user)

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        allow_empty = self.get_allow_empty()
        if not allow_empty:
            # When pagination is enabled and object_list is a queryset,
            # it's better to do a cheap query than to load the unpaginated
            # queryset in memory.
            if self.get_paginate_by(self.object_list) is not None and hasattr(self.object_list, 'exists'):
                is_empty = not self.object_list.exists()
            else:
                is_empty = not self.object_list
            if is_empty:
                raise Http404(_('Empty list and “%(class_name)s.allow_empty” is False.') % {
                    'class_name': self.__class__.__name__,
                })
        if self.request.session.get('project_pk'):
            del self.request.session['project_pk']
        context = self.get_context_data()
        return self.render_to_response(context)


class ProjectCreate(generic.VulnmanAuthCreateWithInlinesView):
    template_name = "projects/project_create.html"
    form_class = forms.ProjectForm
    model = models.Project
    inlines = [forms.ScopeInline, forms.ProjectContactInline]
    success_url = reverse_lazy("projects:project-list")


class ProjectDetail(generic.VulnmanAuthDetailView):
    template_name = "projects/project_detail.html"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        if self.object:
            self.request.session['project_pk'] = str(self.get_object().pk)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        # this one is ugly. use API!!!
        context = super().get_context_data(**kwargs)
        context['severity_vulns_count'] = [
            self.get_object().vulnerability_set.filter(cvss_base_score__gte=9.0, cvss_base_score__lte=10.0).count(),
            self.get_object().vulnerability_set.filter(cvss_base_score__gte=7.0, cvss_base_score__lte=8.9).count(),
            self.get_object().vulnerability_set.filter(cvss_base_score__gte=4.0, cvss_base_score__lte=6.9).count(),
            self.get_object().vulnerability_set.filter(cvss_base_score__gte=0.1, cvss_base_score__lte=3.9).count(),
            self.get_object().vulnerability_set.filter(cvss_base_score=0.0).count()
        ]
        context['severity_labels'] = list(settings.SEVERITY_COLORS.keys())
        context['severity_background_colors'] = []
        context['severity_border_colors'] = []
        for key, value in settings.SEVERITY_COLORS.items():
            context['severity_background_colors'].append(value.get('chart'))
            context['severity_border_colors'].append(value.get('chart_border'))
        context['hosts_list'] = list(self.get_object().host_set.annotate(
            service_count=Count('service')).order_by('-service_count').values_list('ip', flat=True))[:5]
        context['hosts_service_count'] = list(self.get_object().host_set.annotate(
            service_count=Count('service')).order_by('-service_count').values_list('service_count', flat=True))[:5]
        context['latest_days'] = []
        context['vulns_per_day'] = []
        for i in range(10):
            context['latest_days'].append(str(timezone.now().date() - timezone.timedelta(days=i)))
            context['vulns_per_day'].append(self.get_object().vulnerability_set.filter(
                date_created__date=timezone.now().date() - timezone.timedelta(days=i)).count())
        context['latest_days'].reverse()
        context['vulns_per_day'].reverse()
        return context

    def get_queryset(self):
        return models.Project.objects.filter(creator=self.request.user)


class ProjectUpdate(generic.VulnmanAuthUpdateWithInlinesView):
    template_name = "projects/project_update.html"
    form_class = forms.ProjectForm
    inlines = [forms.ScopeInline, forms.ProjectContactInline]
    model = models.Project

    def get_success_url(self):
        return reverse_lazy('projects:project-detail', kwargs={'pk': self.kwargs.get('pk')})

    def get_queryset(self):
        return models.Project.objects.filter(creator=self.request.user)



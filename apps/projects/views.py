from django.urls import reverse_lazy
from django.conf import settings
from django.utils import timezone
from django.db.models import Count
from guardian.shortcuts import get_objects_for_user, assign_perm
from apps.projects import models
from apps.projects import forms
from vulnman.views import generic
from vulnman.mixins.permission import NonObjectPermissionRequiredMixin


class ProjectList(generic.VulnmanAuthListView):
    template_name = "projects/project_list.html"
    context_object_name = "projects"

    def get_queryset(self):
        qs = get_objects_for_user(self.request.user, "view_project", models.Project, use_groups=True)
        if not self.request.GET.get('archived'):
            qs = qs.filter(is_archived=False)
        else:
            qs = qs.filter(is_archived=True)
        return qs

    def get(self, request, *args, **kwargs):
        if self.request.session.get('project_pk'):
            del self.request.session['project_pk']
        return super().get(request, *args, **kwargs)


class ProjectCreate(NonObjectPermissionRequiredMixin, generic.VulnmanAuthCreateWithInlinesView):
    template_name = "projects/project_create.html"
    form_class = forms.ProjectForm
    model = models.Project
    inlines = [forms.ScopeInline]
    success_url = reverse_lazy("projects:project-list")
    extra_context = {"TEMPLATE_HIDE_BREADCRUMBS": True}
    permission_required = "projects.add_project"

    def form_valid(self, form):
        instance = form.save()
        for pentester in form.cleaned_data.get('pentesters'):
            assign_perm("projects.pentest_project", pentester, instance)
            assign_perm("projects.view_project", pentester, instance)
        return super().form_valid(form)


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
            self.get_object().vulnerability_set.filter(cvss_score__gte=9.0, cvss_score__lte=10.0).count(),
            self.get_object().vulnerability_set.filter(cvss_score__gte=7.0, cvss_score__lte=8.9).count(),
            self.get_object().vulnerability_set.filter(cvss_score__gte=4.0, cvss_score__lte=6.9).count(),
            self.get_object().vulnerability_set.filter(cvss_score__gte=0.1, cvss_score__lte=3.9).count(),
            self.get_object().vulnerability_set.filter(cvss_score=0.0).count()
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
        return get_objects_for_user(self.request.user, "view_project",
                                    models.Project.objects.filter(pk=self.kwargs.get('pk')))


class ProjectUpdate(NonObjectPermissionRequiredMixin, generic.VulnmanAuthUpdateWithInlinesView):
    template_name = "projects/project_create.html"
    form_class = forms.ProjectForm
    inlines = [forms.ScopeInline]
    model = models.Project
    permission_required = ["projects.change_project"]

    def get_success_url(self):
        return reverse_lazy('projects:project-detail', kwargs={'pk': self.kwargs.get('pk')})

    def get_queryset(self):
        return get_objects_for_user(self.request.user, "change_project",
                                    models.Project.objects.filter(pk=self.kwargs.get('pk')))

    def form_valid(self, form):
        instance = form.save()
        for pentester in form.cleaned_data.get('pentesters'):
            assign_perm("projects.pentest_project", pentester, instance)
            assign_perm("projects.view_project", pentester, instance)
        return super().form_valid(form)

    def get_initial(self):
        from guardian.shortcuts import get_users_with_perms
        initial = super().get_initial()
        initial["pentesters"] = get_users_with_perms(self.get_object(), with_group_users=False)
        return initial


class ClientList(NonObjectPermissionRequiredMixin, generic.VulnmanAuthListView):
    template_name = "projects/client_list.html"
    context_object_name = "clients"
    model = models.Client
    permission_required = ["projects.view_client"]


class ClientDetail(NonObjectPermissionRequiredMixin, generic.VulnmanAuthDetailView):
    template_name = "projects/client_detail.html"
    context_object_name = "client"
    model = models.Client
    permission_required = ["projects.view_client"]


class ClientCreate(NonObjectPermissionRequiredMixin, generic.VulnmanAuthCreateWithInlinesView):
    template_name = "projects/client_create.html"
    model = models.Client
    permission_required = ["projects.add_client"]
    form_class = forms.ClientForm
    inlines = [forms.ClientContactInline]

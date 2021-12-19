from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone
from django.db.models import Count, Q
from apps.projects import models
from apps.projects import forms
from vulnman.views import generic


class ProjectList(generic.VulnmanAuthListView):
    template_name = "projects/project_list.html"
    context_object_name = "projects"

    def get_queryset(self):
        qs = models.Project.objects.filter(Q(creator=self.request.user) | Q(projectmember__user=self.request.user))
        if not self.request.GET.get('archived'):
            qs = qs.filter(is_archived=False)
        else:
            qs = qs.filter(is_archived=True)
        return qs

    def get(self, request, *args, **kwargs):
        if self.request.session.get('project_pk'):
            del self.request.session['project_pk']
        return super().get(request, *args, **kwargs)


class ProjectCreate(generic.VulnmanAuthCreateWithInlinesView):
    template_name = "projects/project_create.html"
    form_class = forms.ProjectForm
    model = models.Project
    inlines = [forms.ScopeInline]
    success_url = reverse_lazy("projects:project-list")
    extra_context = {"TEMPLATE_HIDE_BREADCRUMBS": True}


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
        return models.Project.objects.filter(Q(creator=self.request.user) | Q(projectmember__user=self.request.user))


class ProjectUpdate(generic.VulnmanAuthUpdateWithInlinesView):
    template_name = "projects/project_update.html"
    form_class = forms.ProjectForm
    inlines = [forms.ScopeInline]
    model = models.Project

    def get_success_url(self):
        return reverse_lazy('projects:project-detail', kwargs={'pk': self.kwargs.get('pk')})

    def get_queryset(self):
        return models.Project.objects.filter(creator=self.request.user)


class ProjectMemberCreate(generic.ProjectCreateView):
    template_name = "projects/project_add_member.html"
    form_class = forms.ProjectAddMemberForm

    def get_success_url(self):
        return reverse_lazy('projects:project-detail', kwargs={'pk': self.get_project().pk})

    def form_valid(self, form):
        if User.objects.filter(email=form.cleaned_data.get('email')).exists():
            user = User.objects.get(email=form.cleaned_data.get('email'))
            form.instance.user = user
            form.instance.project = self.get_project()
            return super().form_valid(form)
        return self.form_invalid(form)


class ProjectMemberList(generic.ProjectListView):
    template_name = "projects/project_member_list.html"
    model = models.ProjectMember
    context_object_name = "project_members"


class ProjectMemberDelete(generic.ProjectDeleteView):
    http_method_names = ["post"]
    model = models.ProjectMember
    success_url = reverse_lazy("projects:project-member-list")

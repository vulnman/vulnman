from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from dal import autocomplete
from vulnman.views import generic
from vulns import forms
from vulns import models
from vulns.utils import cvsslib


class HostList(generic.ProjectListView):
    template_name = "vulns/host_list.html"
    context_object_name = "hosts"
    model = models.Host


class HostCreate(generic.ProjectCreateWithInlinesView):
    template_name = "vulns/host_create.html"
    form_class = forms.HostForm
    model = models.Host
    inlines = [forms.HostnameInline]


class HostDetail(generic.ProjectDetailView):
    template_name = "vulns/host_detail.html"
    context_object_name = "host"
    model = models.Host


class VulnCreate(generic.ProjectCreateWithInlinesView):
    model = models.Vulnerability
    inlines = [forms.ProofOfConceptInline]
    form_class = forms.VulnerabilityForm
    template_name = "vulns/vuln_create.html"

    def form_valid(self, form):
        if form.instance.cvss_string:
            form.instance.cvss_base_score = cvsslib.get_scores_by_vector(form.instance.cvss_string)[0]
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['project'] = self.get_project()
        return kwargs


class VulnUpdate(generic.ProjectUpdateWithInlinesView):
    model = models.Vulnerability
    inlines = [forms.ProofOfConceptInline]
    form_class = forms.VulnerabilityForm
    template_name = "vulns/vuln_create.html"

    def form_valid(self, form):
        if form.instance.cvss_string:
            form.instance.cvss_base_score = cvsslib.get_scores_by_vector(form.instance.cvss_string)[0]
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['project'] = self.get_project()
        return kwargs


class VulnList(generic.ProjectListView):
    template_name = "vulns/vuln_list.html"
    context_object_name = "vulns"
    model = models.Vulnerability


class VulnDetail(generic.ProjectDetailView):
    template_name = "vulns/vuln_detail.html"
    context_object_name = "vuln"
    model = models.Vulnerability


class VulnDelete(generic.ProjectDeleteView):
    model = models.Vulnerability
    http_method_names = ["post"]

    def get_success_url(self):
        return reverse_lazy('projects:vulns:vuln-list')

    def get_queryset(self):
        return models.Vulnerability.objects.filter(project=self.get_project())


class VulnerabilityTemplateList(generic.VulnmanListView):
    model = models.VulnerabilityTemplate
    paginate_by = 20
    template_name = "vulns/vulnerability_template_list.html"
    context_object_name = "vuln_templates"


class VulnerabilityTemplateCreate(generic.VulnmanCreateView):
    model = models.VulnerabilityTemplate
    form_class = forms.VulnerabilityTemplateForm
    template_name = "vulns/vulnerability_template_create.html"

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class VulnerabilityTemplateDetail(generic.VulnmanDetailView):
    model = models.VulnerabilityTemplate
    template_name = "vulns/vulnerability_template_detail.html"
    context_object_name = "vuln_template"


class VulnerabilityTemplateAutocomplete(LoginRequiredMixin, autocomplete.Select2QuerySetView):
    def get_queryset(self):
        queryset = models.VulnerabilityTemplate.objects.all()
        if self.q:
            queryset = queryset.filter(Q(name__contains=self.q) | Q(description__contains=self.q))
        return queryset


class WebApplicationUrlPathAddWebApp(generic.ProjectUpdateView):
    model = models.WebApplicationUrlPath
    form_class = forms.WebApplicationUrlPathForm
    template_name = "vulns/webapp_url_add_webapp.html"

    def get_success_url(self):
        return reverse_lazy('projects:vulns:host-detail', kwargs={'pk': self.get_object().hostname.host.pk})


class HostEdit(generic.ProjectUpdateWithInlinesView):
    template_name = "vulns/host_create.html"
    form_class = forms.HostForm
    model = models.Host
    inlines = [forms.HostnameInline]


class HostDelete(generic.ProjectDeleteView):
    http_method_names = ["post"]
    model = models.Host

    def get_success_url(self):
        return reverse_lazy('projects:vulns:host-list')

from django.urls import reverse_lazy

from vulnman.views import generic
from vulns import forms
from vulns import models
from vulns.utils import cvsslib


class VulnCreate(generic.ProjectCreateWithInlinesView):
    model = models.Vulnerability
    inlines = [forms.ProofOfConceptInline]
    form_class = forms.VulnerabilityForm
    template_name = "vulns/vuln_create.html"
    allowed_project_roles = ["pentester"]

    def form_valid(self, form):
        if form.instance.cvss_string:
            form.instance.cvss_base_score = cvsslib.get_scores_by_vector(form.instance.cvss_string)[0]
        if form.instance.service:
            form.instance.host = form.instance.service.host
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
    allowed_project_roles = ["pentester"]

    def form_valid(self, form):
        if form.instance.cvss_string:
            form.instance.cvss_base_score = cvsslib.get_scores_by_vector(form.instance.cvss_string)[0]
        if form.instance.service:
            form.instance.host = form.instance.service.host
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['project'] = self.get_project()
        return kwargs


class VulnList(generic.ProjectListView):
    template_name = "vulns/vuln_list.html"
    context_object_name = "vulns"
    model = models.Vulnerability
    allowed_project_roles = ["pentester", "read-only"]


class VulnDetail(generic.ProjectDetailView):
    template_name = "findings/vuln_detail.html"
    context_object_name = "vuln"
    model = models.Vulnerability
    allowed_project_roles = ["pentester", "read-only"]


class VulnDelete(generic.ProjectDeleteView):
    model = models.Vulnerability
    http_method_names = ["post"]
    allowed_project_roles = ["pentester"]

    def get_success_url(self):
        return reverse_lazy('projects:vulns:vuln-list')

    def get_queryset(self):
        return models.Vulnerability.objects.filter(project=self.get_project())


class WebApplicationUrlPathAddWebApp(generic.ProjectUpdateView):
    model = models.WebApplicationUrlPath
    form_class = forms.WebApplicationUrlPathForm
    template_name = "vulns/webapp_url_add_webapp.html"
    allowed_project_roles = ["pentester"]

    def get_success_url(self):
        return reverse_lazy('projects:vulns:host-detail', kwargs={'pk': self.get_object().hostname.host.pk})

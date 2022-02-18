from django.db.models import Q
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from dal import autocomplete
from vulnman.views import generic
from apps.findings import models
from apps.findings import forms
from apps.findings.utils import cvss
from apps.assets.models import WebApplication


class TemplateCreate(generic.VulnmanAuthCreateWithInlinesView):
    model = models.Template
    form_class = forms.TemplateForm
    inlines = [forms.ReferenceInline]
    template_name = "findings/template_create.html"

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class TemplateList(generic.VulnmanAuthListView):
    model = models.Template
    paginate_by = 20
    template_name = "findings/template_list.html"
    context_object_name = "vuln_templates"


class TemplateDetail(generic.VulnmanAuthDetailView):
    model = models.Template
    template_name = "findings/template_detail.html"
    context_object_name = "vuln_template"


class TemplateUpdate(generic.VulnmanAuthUpdateView):
    model = models.Template
    form_class = forms.TemplateForm
    template_name = "findings/template_create.html"

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class VulnerabilityTemplateAutocomplete(LoginRequiredMixin,
                                        autocomplete.Select2QuerySetView):
    def get_queryset(self):
        queryset = models.Template.objects.all()
        if self.q:
            queryset = queryset.filter(
                Q(name__contains=self.q) | Q(description__contains=self.q))
        return queryset


class VulnList(generic.ProjectListView):
    template_name = "findings/vulnerability_list.html"
    context_object_name = "vulns"
    model = models.Vulnerability
    allowed_project_roles = ["pentester", "read-only"]


class VulnCreate(generic.ProjectCreateWithInlinesView):
    model = models.Vulnerability
    inlines = []
    form_class = forms.VulnerabilityForm
    template_name = "findings/vulnerability_create.html"
    allowed_project_roles = ["pentester"]

    def form_valid(self, form):
        if form.instance.cvss_vector:
            form.instance.cvss_score = cvss.get_scores_by_vector(
                form.instance.cvss_vector)[0]
        if form.cleaned_data["asset_type"] == "webapp":
            form.instance.asset_webapp = WebApplication.objects.get(project=self.get_project(), pk=form.cleaned_data["f_asset"])
        else:
            form.add_errors("asset_type", "invalid asset type")
            return super().form_invalid(form)
        return super().form_valid(form)

    def forms_valid(self, form, inlines):
        response = self.form_valid(form)
        for formset in inlines:
            instances = formset.save(commit=False)
            for instance in instances:
                instance.project = self.get_project()
                instance.save()
        return response

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['project'] = self.get_project()
        return kwargs


class AddTextProof(generic.ProjectCreateView):
    http_method_names = ["post"]
    model = models.TextProof
    form_class = forms.TextProofForm

    def form_valid(self, form):
        vuln = self.get_project().vulnerability_set.filter(pk=self.kwargs.get('pk'))
        if not vuln.exists():
            self.form.add_errors("name", "Vulnerability does not exist!")
            return super().form_invalid(form)
        form.instance.vulnerability = vuln.get()
        form.instance.project = self.get_project()
        self.success_url = vuln.get().get_absolute_url()
        return super().form_valid(form)


class AddImageProof(generic.ProjectCreateView):
    http_method_names = ["post"]
    model = models.ImageProof
    form_class = forms.ImageProofForm

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)


    def form_valid(self, form):
        vuln = self.get_project().vulnerability_set.filter(pk=self.kwargs.get('pk'))
        if not vuln.exists():
            self.form.add_errors("name", "Vulnerability does not exist!")
            return super().form_invalid(form)
        form.instance.vulnerability = vuln.get()
        form.instance.project = self.get_project()
        self.success_url = vuln.get().get_absolute_url()
        return super().form_valid(form)


class VulnDetail(generic.ProjectDetailView):
    template_name = "findings/vuln_detail.html"
    context_object_name = "vuln"
    model = models.Vulnerability

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["text_proof_form"] = forms.TextProofForm()
        context["image_proof_form"] = forms.ImageProofForm()
        return context
    

class VulnUpdate(generic.ProjectUpdateWithInlinesView):
    model = models.Vulnerability
    inlines = []
    form_class = forms.VulnerabilityForm
    template_name = "findings/vulnerability_create.html"

    def form_valid(self, form):
        if form.instance.cvss_vector:
            form.instance.cvss_score = cvss.get_scores_by_vector(
                form.instance.cvss_vector)[0]
        if form.instance.service:
            form.instance.host = form.instance.service.host
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['project'] = self.get_project()
        return kwargs

    def forms_valid(self, form, inlines):
        response = self.form_valid(form)
        for formset in inlines:
            instances = formset.save(commit=False)
            for instance in instances:
                instance.project = self.get_project()
                instance.save()
        return response

class VulnDelete(generic.ProjectDeleteView):
    model = models.Vulnerability
    http_method_names = ["post"]
    allowed_project_roles = ["pentester"]

    def get_success_url(self):
        return reverse_lazy('projects:findings:vulnerability-list')

    def get_queryset(self):
        return models.Vulnerability.objects.filter(project=self.get_project())


class TextProofDelete(generic.ProjectDeleteView):
    model = models.TextProof
    http_method_names = ["post"]

    def get_success_url(self):
        return reverse_lazy('projects:findings:vulnerability-list')

    def get_queryset(self):
        return models.TextProof.objects.filter(project=self.get_project())

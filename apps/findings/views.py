from django.db.models import Q
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from vulnman.views import generic
from apps.findings import models
from apps.findings import forms
from apps.findings.utils import cvss
from apps.assets.models import WebApplication, WebRequest


class TemplateList(generic.VulnmanAuthListView):
    model = models.Template
    paginate_by = 20
    template_name = "findings/template_list.html"
    context_object_name = "templates"


class VulnList(generic.ProjectListView):
    template_name = "findings/vulnerability_list.html"
    context_object_name = "vulns"
    model = models.Vulnerability
    allowed_project_roles = ["pentester", "read-only"]


class VulnCreate(generic.ProjectCreateView):
    model = models.Vulnerability
    form_class = forms.VulnerabilityForm
    template_name = "findings/vulnerability_create.html"
    allowed_project_roles = ["pentester"]

    def form_valid(self, form):
        if not models.Template.objects.filter(vulnerability_id=form.cleaned_data["template_id"]).exists():
            form.add_error("template_id", "Template does not exist!")
            return super().form_invalid(form)
        form.instance.template = models.Template.objects.get(vulnerability_id=form.cleaned_data["template_id"])
        if form.instance.cvss_vector:
            form.instance.cvss_score = cvss.get_scores_by_vector(
                form.instance.cvss_vector)[0]
        if form.cleaned_data["asset_type"] == "webapplication":
            form.instance.asset_webapp = WebApplication.objects.get(project=self.get_project(), pk=form.cleaned_data["f_asset"])
        elif form.cleaned_data["asset_type"] == "webrequest":
            form.instance.asset_webrequest = WebRequest.objects.get(project=self.get_project(), pk=form.cleaned_data["f_asset"])
        else:
            form.add_error("asset_type", "invalid asset type")
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
        return super().form_valid(form)

    def get_initial(self):
        initial = super().get_initial()
        initial["template_id"] = self.get_object().template.vulnerability_id
        return initial

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


class ProofSetOrder(generic.ProjectFormView):
    http_method_names = ["post"]

    def form_valid(self, form):
        if models.TextProof.objects.filter(project=self.get_project(), pk=form.cleaned_data["pk"]).exists():
            proof = models.TextProof.objects.get(pk=form.cleaned_data["pk"])
        elif models.ImageProof.objects.filter(project=self.get_project(), pk=form.cleaned_data["pk"]).exists():
            proof = models.ImageProof.objects.get(pk=form.cleaned_data["pk"])
        proof.order = form.cleaned_data["pk"]
        proof.save()
        return super().form_valid(form)


class UserAccountList(generic.ProjectListView):
    model = models.UserAccount
    context_object_name = "user_accounts"
    template_name = "findings/user_account_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["account_create_form"] = forms.UserAccountForm() 
        return context
    

class UserAccountCreate(generic.ProjectCreateView):
    http_method_names = ["post"]
    model = models.UserAccount
    form_class = forms.UserAccountForm
    success_url = reverse_lazy("projects:findings:user-account-list")

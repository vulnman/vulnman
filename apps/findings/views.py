import django_filters.views
from django.conf import settings
from django.http import HttpResponse, Http404
from django.urls import reverse_lazy
from vulnman.core.views import generics
from apps.findings import models
from apps.findings import forms
from apps.reporting.tasks import export_single_vulnerability
from apps.findings import filters


class TemplateList(generics.VulnmanAuthListView):
    model = models.Template
    paginate_by = 20
    template_name = "findings/template_list.html"
    context_object_name = "templates"


class TemplateDetail(generics.VulnmanAuthDetailView):
    model = models.Template
    template_name = "findings/template_detail.html"
    context_object_name = "template"


class VulnList(django_filters.views.FilterMixin, generics.ProjectListView):
    template_name = "findings/vulnerabilities/list.html"
    context_object_name = "vulnerabilities"
    filterset_class = filters.VulnerabilityFilter

    def get_queryset(self):
        qs = models.Vulnerability.objects.for_project(self.get_project())
        if not self.request.GET.get("status"):
            qs = qs.open()
        filterset = self.filterset_class(self.request.GET, queryset=qs)
        return filterset.qs

    def get_context_data(self, **kwargs):
        if not self.request.session.get("vulns_filters"):
            self.request.session["vulns_filters"] = dict(self.request.GET)
        if not self.request.GET:
            self.request.session["vulns_filters"] = {}
        for key, value in self.request.GET.items():
            self.request.session["vulns_filters"][key] = value
        qs = models.Vulnerability.objects.for_project(self.get_project())
        qs_filters = self.request.GET.copy()
        if qs_filters.get("status"):
            del qs_filters["status"]
        filterset = self.filterset_class(qs_filters, queryset=qs)
        qs = filterset.qs
        kwargs["open_vulns_count"] = qs.open().count()
        kwargs["closed_vulns_count"] = qs.fixed().count()
        return super().get_context_data(**kwargs)


class VulnCreate(generics.ProjectCreateView):
    model = models.Vulnerability
    form_class = forms.VulnerabilityForm
    template_name = "findings/vulnerability_create.html"

    def form_valid(self, form):
        if not models.Template.objects.filter(vulnerability_id=form.cleaned_data["template_id"]).exists():
            form.add_error("template_id", "Template does not exist!")
            return super().form_invalid(form)
        form.instance.template = models.Template.objects.get(vulnerability_id=form.cleaned_data["template_id"])
        if form.cleaned_data.get("severity") is None:
            form.instance.severity = form.instance.template.severity
        form.instance.object_id = form.cleaned_data["f_asset"]
        form.instance.content_type = models.Vulnerability.objects.get_asset_content_type(
            form.cleaned_data["f_asset"])
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['project'] = self.get_project()
        return kwargs


class TextProofCreate(generics.ProjectCreateView):
    form_class = forms.TextProofForm
    template_name = "findings/text_proof_create_or_update.html"

    def get_success_url(self):
        return reverse_lazy('projects:findings:vulnerability-proofs', kwargs={"pk": self.kwargs.get("pk")})

    def get_context_data(self, **kwargs):
        try:
            obj = self.get_project().vulnerability_set.get(pk=self.kwargs.get("pk"))
        except models.Vulnerability.DoesNotExist:
            raise Http404()
        kwargs["vuln"] = obj
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        vuln = self.get_context_data()["vuln"]
        form.instance.vulnerability = vuln
        form.instance.project = self.get_project()
        return super().form_valid(form)


class TextProofUpdate(generics.ProjectUpdateView):
    template_name = "findings/proof_update.html"
    form_class = forms.TextProofForm

    def get_queryset(self):
        return models.TextProof.objects.filter(vulnerability__project=self.get_project())

    def get_success_url(self):
        return self.get_object().vulnerability.get_absolute_url()


class ImageProofUpdate(generics.ProjectUpdateView):
    template_name = "findings/image_proof_create_or_update.html"
    form_class = forms.ImageProofForm

    def get_queryset(self):
        return models.ImageProof.objects.filter(vulnerability__project=self.get_project())

    def get_success_url(self):
        return self.get_object().vulnerability.get_absolute_url()


class AddImageProof(generics.ProjectCreateView):
    model = models.ImageProof
    form_class = forms.ImageProofForm
    template_name = "findings/image_proof_create_or_update.html"

    def get_success_url(self):
        return reverse_lazy('projects:findings:vulnerability-proofs', kwargs={"pk": self.kwargs.get("pk")})

    def get_context_data(self, **kwargs):
        try:
            obj = self.get_project().vulnerability_set.get(pk=self.kwargs.get("pk"))
        except models.Vulnerability.DoesNotExist:
            raise Http404()
        kwargs["vuln"] = obj
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        vuln = self.get_context_data()["vuln"]
        form.instance.vulnerability = vuln
        form.instance.project = self.get_project()
        return super().form_valid(form)


class VulnDetail(generics.ProjectDetailView):
    template_name = "findings/vuln_detail.html"
    context_object_name = "vuln"
    model = models.Vulnerability

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["export_vuln_form"] = forms.VulnerabilityExportForm(initial={"template": "default"})
        context["change_cvss_form"] = forms.VulnerabilityCVSSBaseForm(initial={
            "cvss_av": context["vuln"].cvss_av, "cvss_ac": context["vuln"].cvss_ac,
            "cvss_s": context["vuln"].cvss_s, "cvss_c": context["vuln"].cvss_c,
            "cvss_i": context["vuln"].cvss_i, "cvss_a": context["vuln"].cvss_a,
            "cvss_pr": context["vuln"].cvss_pr, "cvss_ui": context["vuln"].cvss_ui
        })
        return context


class VulnerabilityProofs(generics.ProjectDetailView):
    # TODO: write tests
    template_name = "findings/vulnerability_proofs.html"
    context_object_name = "vuln"
    model = models.Vulnerability


class VulnerabilityExport(generics.ProjectDetailView):
    model = models.Vulnerability

    def render_to_response(self, context, **response_kwargs):
        template = self.request.GET.get("template", "default")
        if not settings.REPORT_TEMPLATES.get(template, None):
            template = "default"
        result = export_single_vulnerability(self.get_object(), template)
        response = HttpResponse(result, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="report.pdf"'
        return response


class VulnUpdate(generics.ProjectUpdateView):
    form_class = forms.VulnerabilityForm
    template_name = "findings/vulnerability_create.html"

    def get_queryset(self):
        return models.Vulnerability.objects.filter(project=self.get_project())

    def form_valid(self, form):
        if not models.Template.objects.filter(vulnerability_id=form.cleaned_data["template_id"]).exists():
            form.add_error("template_id", "Template does not exist!")
            return super().form_invalid(form)
        form.instance.template = models.Template.objects.get(vulnerability_id=form.cleaned_data["template_id"])
        if form.cleaned_data.get("severity") is None:
            form.instance.severity = form.instance.template.severity
        form.instance.content_type = models.Vulnerability.objects.get_asset_content_type(form.cleaned_data["f_asset"])
        form.instance.object_id = form.cleaned_data["f_asset"]
        return super().form_valid(form)

    def get_initial(self):
        initial = super().get_initial()
        initial["template_id"] = self.get_object().template.vulnerability_id
        initial["f_asset"] = (self.get_object().asset.pk, self.get_object().name)
        return initial

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['project'] = self.get_project()
        return kwargs


class VulnDelete(generics.ProjectDeleteView):
    http_method_names = ["post"]
    allowed_project_roles = ["pentester"]

    def get_success_url(self):
        return reverse_lazy('projects:findings:vulnerability-list')

    def get_queryset(self):
        return models.Vulnerability.objects.filter(project=self.get_project())


class TextProofDelete(generics.ProjectDeleteView):
    http_method_names = ["post"]
    permission_required = ["projects.change_project"]

    def get_success_url(self):
        return self.get_object().vulnerability.get_absolute_url()

    def get_queryset(self):
        return models.TextProof.objects.filter(vulnerability__project=self.get_project())


class UserAccountList(generics.ProjectListView):
    # TODO: write tests
    context_object_name = "user_accounts"
    template_name = "findings/user_account_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["account_create_form"] = forms.UserAccountForm()
        context["account_update_forms"] = []
        for qs in self.get_queryset():
            context["account_update_forms"].append(forms.UserAccountUpdateForm(instance=qs))
        return context

    def get_queryset(self):
        return models.UserAccount.objects.filter(project=self.get_project())


class UserAccountCreate(generics.ProjectCreateView):
    # TODO: write tests
    http_method_names = ["post"]
    model = models.UserAccount
    form_class = forms.UserAccountForm
    success_url = reverse_lazy("projects:findings:user-account-list")


class UserAccountUpdate(generics.ProjectUpdateView):
    # TODO: write tests
    http_method_names = ["post"]
    form_class = forms.UserAccountUpdateForm
    success_url = reverse_lazy("projects:findings:user-account-list")

    def get_queryset(self):
        return models.UserAccount.objects.filter(project=self.get_project())


class UserAccountDelete(generics.ProjectDeleteView):
    # TODO: write tests
    http_method_names = ["post"]
    permission_required = ["projects.change_project"]

    def get_success_url(self):
        return reverse_lazy('projects:findings:user-account-list')

    def get_queryset(self):
        return models.UserAccount.objects.filter(project=self.get_project())


class VulnerabilityCVSSUpdate(generics.ProjectUpdateView):
    form_class = forms.VulnerabilityCVSSBaseForm
    template_name = "findings/vuln_cvss_update.html"

    def get_queryset(self):
        return models.Vulnerability.objects.filter(project=self.get_project())


class ImageProofDelete(generics.ProjectDeleteView):
    http_method_names = ["post"]

    def get_success_url(self):
        return self.get_object().vulnerability.get_absolute_url()

    def get_queryset(self):
        return models.ImageProof.objects.filter(vulnerability__project=self.get_project())

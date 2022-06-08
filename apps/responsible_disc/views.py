from django.urls import reverse_lazy
from django.http import HttpResponse
from vulnman.views import generic
from apps.findings.models import Template
from apps.responsible_disc import models
from apps.responsible_disc import forms
from apps.responsible_disc import tasks


class VulnerabilityList(generic.VulnmanAuthListView):
    template_name = "responsible_disc/vulnerability_list.html"
    context_object_name = "vulnerabilities"

    def get_queryset(self):
        return models.Vulnerability.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["create_form"] = forms.VulnerabilityForm()
        return context


class VulnerabilityCreate(generic.VulnmanAuthCreateView):
    form_class = forms.VulnerabilityForm
    template_name = "responsible_disc/vulnerability_create.html"

    def form_valid(self, form):
        if not Template.objects.filter(vulnerability_id=form.cleaned_data["template_id"]).exists():
            form.add_error("template_id", "Template does not exist!")
            return super().form_invalid(form)
        form.instance.template = Template.objects.get(vulnerability_id=form.cleaned_data["template_id"])
        if not form.cleaned_data.get('severity'):
            form.instance.severity = form.instance.template.severity
        form.instance.user = self.request.user
        return super().form_valid(form)


class VulnerabilityDetail(generic.VulnmanAuthDetailView):
    template_name = "responsible_disc/vulnerability_detail.html"
    context_object_name = "vuln"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["text_proof_form"] = forms.TextProofForm()
        context["image_proof_form"] = forms.ImageProofForm()
        return context

    def get_queryset(self):
        return models.Vulnerability.objects.filter(user=self.request.user)


class AddImageProof(generic.VulnmanAuthCreateView):
    http_method_names = ["post"]
    model = models.ImageProof
    form_class = forms.ImageProofForm

    def form_valid(self, form):
        vuln = models.Vulnerability.objects.filter(pk=self.kwargs.get('pk'), user=self.request.user)
        if not vuln.exists():
            form.add_error("name", "Vulnerability does not exist!")
            return super().form_invalid(form)
        form.instance.vulnerability = vuln.get()
        form.instance.user = self.request.user
        self.success_url = vuln.get().get_absolute_url()
        return super().form_valid(form)


class AddTextProof(generic.VulnmanAuthCreateView):
    http_method_names = ["post"]
    model = models.TextProof
    form_class = forms.TextProofForm

    def form_valid(self, form):
        vuln = models.Vulnerability.objects.filter(pk=self.kwargs.get('pk'), user=self.request.user)
        if not vuln.exists():
            form.add_error("name", "Vulnerability does not exist!")
            return super().form_invalid(form)
        form.instance.vulnerability = vuln.get()
        form.instance.user = self.request.user
        self.success_url = vuln.get().get_absolute_url()
        return super().form_valid(form)


class TextProofDelete(generic.VulnmanAuthDeleteView):
    model = models.TextProof
    http_method_names = ["post"]

    def get_success_url(self):
        return reverse_lazy('responsible_disc:vulnerability-detail', kwargs={"pk": self.get_object().vulnerability.pk})

    def get_queryset(self):
        return models.TextProof.objects.filter(vulnerability__user=self.request.user)


class ImageProofDelete(generic.VulnmanAuthDeleteView):
    model = models.ImageProof
    http_method_names = ["post"]

    def get_success_url(self):
        return reverse_lazy('responsible_disc:vulnerability-detail', kwargs={"pk": self.get_object().vulnerability.pk})

    def get_queryset(self):
        return models.ImageProof.objects.filter(vulnerability__user=self.request.user)


class VulnerabilityExport(generic.VulnmanAuthDetailView):

    def get_queryset(self):
        return models.Vulnerability.objects.filter(user=self.request.user)

    def render_to_response(self, context, **response_kwargs):
        result = tasks.export_single_vulnerability(self.get_object())
        response = HttpResponse(result, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="report.pdf"'
        return response


class VulnerabilityNotifyVendor(generic.VulnmanAuthUpdateView):
    form_class = forms.VulnerabilityNotificationForm
    http_method_names = ["post"]

    def get_queryset(self):
        return models.Vulnerability.objects.filter(user=self.request.user)

    def form_valid(self, form):
        if not form.instance.vendor_email:
            form.add_error("empty", "No vendor email set")
            return super().form_invalid(form)
        tasks.notify_vendor.delay(str(form.instance.pk))
        form.instance.status = models.Vulnerability.STATUS_VENDOR_NOTIFIED
        return super().form_valid(form)


class VulnUpdate(generic.VulnmanAuthUpdateView):
    model = models.Vulnerability
    form_class = forms.VulnerabilityForm
    template_name = "responsible_disc/vulnerability_create.html"

    def get_queryset(self):
        return models.Vulnerability.objects.filter(user=self.request.user)

    def form_valid(self, form):
        if not Template.objects.filter(vulnerability_id=form.cleaned_data["template_id"]).exists():
            form.add_error("template_id", "Template does not exist!")
            return super().form_invalid(form)
        form.instance.template = Template.objects.get(vulnerability_id=form.cleaned_data["template_id"])
        if not form.cleaned_data.get('severity'):
            form.instance.severity = form.instance.template.severity
        return super().form_valid(form)


class VulnDelete(generic.VulnmanAuthDeleteView):
    http_method_names = ["post"]
    success_url = reverse_lazy('responsible_disc:vulnerability-list')

    def get_queryset(self):
        return models.Vulnerability.objects.filter(user=self.request.user)


class VulnerabilityAdvisoryExport(generic.VulnmanAuthDetailView):

    def get_queryset(self):
        return models.Vulnerability.objects.filter(user=self.request.user)

    def render_to_response(self, context, **response_kwargs):
        result = tasks.export_advisory(self.get_object())
        response = HttpResponse(result, content_type='plain/text')
        response['Content-Disposition'] = 'attachment; filename="advisory.md"'
        return response

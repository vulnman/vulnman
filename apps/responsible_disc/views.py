import django_filters.views
from django.urls import reverse_lazy
from django.http import HttpResponse
from vulnman.core.views import generics
from apps.findings.models import Template
from apps.responsible_disc import models
from apps.responsible_disc import forms
from apps.responsible_disc import tasks
from apps.responsible_disc import filters


class VulnerabilityList(django_filters.views.FilterMixin, generics.VulnmanAuthListView):
    template_name = "responsible_disc/vulnerability_list.html"
    context_object_name = "vulnerabilities"
    filterset_class = filters.VulnerabilityFilter
    model = models.Vulnerability

    def get_queryset(self):
        qs = super().get_queryset().filter(
            user=self.request.user)
        filterset = self.filterset_class(self.request.GET, queryset=qs)
        return filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["create_form"] = forms.VulnerabilityForm()
        return context


class VulnerabilityCreate(generics.VulnmanAuthCreateView):
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


class VulnerabilityDetail(generics.VulnmanAuthDetailView):
    template_name = "responsible_disc/vulnerability_detail.html"
    context_object_name = "vuln"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["text_proof_form"] = forms.TextProofForm()
        context["image_proof_form"] = forms.ImageProofForm()
        context["log_form"] = forms.VulnerabilityLogForm()
        return context

    def get_queryset(self):
        return models.Vulnerability.objects.filter(user=self.request.user)


class AddImageProof(generics.VulnmanAuthCreateView):
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


class VulnerabilityLogCreate(generics.VulnmanAuthCreateView):
    http_method_names = ["post"]
    form_class = forms.VulnerabilityLogForm

    def get_queryset(self):
        return models.VulnerabilityLog.objects.filter(user=self.request.user)

    def form_valid(self, form):
        vulnerability = models.Vulnerability.objects.filter(pk=self.kwargs.get('pk'), user=self.request.user)
        if not vulnerability.exists():
            form.add_error("action", "Vulnerability does not exist!")
            return super().form_invalid(form)
        form.instance.vulnerability = vulnerability.get()
        self.success_url = vulnerability.get().get_absolute_url()
        return super().form_valid(form)


class AddTextProof(generics.VulnmanAuthCreateView):
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


class TextProofDelete(generics.VulnmanAuthDeleteView):
    model = models.TextProof
    http_method_names = ["post"]

    def get_success_url(self):
        return reverse_lazy('responsible_disc:vulnerability-detail', kwargs={"pk": self.get_object().vulnerability.pk})

    def get_queryset(self):
        return models.TextProof.objects.filter(vulnerability__user=self.request.user)


class ImageProofDelete(generics.VulnmanAuthDeleteView):
    model = models.ImageProof
    http_method_names = ["post"]

    def get_success_url(self):
        return reverse_lazy('responsible_disc:vulnerability-detail', kwargs={"pk": self.get_object().vulnerability.pk})

    def get_queryset(self):
        return models.ImageProof.objects.filter(vulnerability__user=self.request.user)


class VulnerabilityExport(generics.VulnmanAuthDetailView):

    def get_queryset(self):
        return models.Vulnerability.objects.filter(user=self.request.user)

    def render_to_response(self, context, **response_kwargs):
        result = tasks.export_single_vulnerability(self.get_object())
        response = HttpResponse(result, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="report.pdf"'
        return response


class VulnerabilityNotifyVendor(generics.VulnmanAuthUpdateView):
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


class VulnUpdate(generics.VulnmanAuthUpdateView):
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


class VulnDelete(generics.VulnmanAuthDeleteView):
    http_method_names = ["post"]
    success_url = reverse_lazy('responsible_disc:vulnerability-list')

    def get_queryset(self):
        return models.Vulnerability.objects.filter(user=self.request.user)


class VulnerabilityAdvisoryExport(generics.VulnmanAuthDetailView):

    def get_queryset(self):
        return models.Vulnerability.objects.filter(user=self.request.user)

    def render_to_response(self, context, **response_kwargs):
        result = tasks.export_advisory(self.get_object())
        response = HttpResponse(result, content_type='plain/text')
        response['Content-Disposition'] = 'attachment; filename="advisory.md"'
        return response


class TextProofUpdate(generics.VulnmanAuthUpdateView):
    template_name = "findings/proof_update.html"
    form_class = forms.TextProofForm

    def get_queryset(self):
        return models.TextProof.objects.filter(vulnerability__user=self.request.user)

    def get_success_url(self):
        return reverse_lazy("responsible_disc:vulnerability-detail", kwargs={"pk": self.get_object().vulnerability.pk})


class ImageProofUpdate(generics.VulnmanAuthUpdateView):
    template_name = "findings/proof_update.html"
    form_class = forms.ImageProofForm

    def get_queryset(self):
        return models.ImageProof.objects.filter(vulnerability__user=self.request.user)

    def get_success_url(self):
        return reverse_lazy("responsible_disc:vulnerability-detail", kwargs={"pk": self.get_object().vulnerability.pk})

from django.urls import reverse_lazy
from vulnman.views import generic
from apps.findings.models import Template
from apps.responsible_disc import models
from apps.responsible_disc import forms


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
        return reverse_lazy('responsible_disc:vulnerability-list')

    def get_queryset(self):
        return models.TextProof.objects.filter(vulnerability__user=self.request.user)


class ImageProofDelete(generic.VulnmanAuthDeleteView):
    model = models.ImageProof
    http_method_names = ["post"]

    def get_success_url(self):
        return reverse_lazy('responsible_disc:vulnerability-list')

    def get_queryset(self):
        return models.ImageProof.objects.filter(vulnerability__user=self.request.user)

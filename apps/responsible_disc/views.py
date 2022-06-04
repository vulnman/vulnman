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
        form.instance.user = self.request.user
        return super().form_valid(form)

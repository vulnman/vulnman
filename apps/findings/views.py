from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from dal import autocomplete
from vulnman.views import generic
from apps.findings import models
from apps.findings import forms


class TemplateCreate(generic.VulnmanCreateView):
    model = models.Template
    form_class = forms.TemplateForm
    template_name = "findings/template_create.html"

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class TemplateList(generic.VulnmanListView):
    model = models.Template
    paginate_by = 20
    template_name = "findings/template_list.html"
    context_object_name = "vuln_templates"


class TemplateDetail(generic.VulnmanDetailView):
    model = models.Template
    template_name = "findings/template_detail.html"
    context_object_name = "vuln_template"


class TemplateUpdate(generic.VulnmanUpdateView):
    model = models.Template
    form_class = forms.TemplateForm
    template_name = "findings/template_create.html"

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class VulnerabilityTemplateAutocomplete(LoginRequiredMixin, autocomplete.Select2QuerySetView):
    def get_queryset(self):
        queryset = models.Template.objects.all()
        if self.q:
            queryset = queryset.filter(Q(name__contains=self.q) | Q(description__contains=self.q))
        return queryset

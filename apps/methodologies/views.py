from django.urls import reverse_lazy
from vulnman.views import generic
from apps.methodologies import forms
from apps.methodologies import models


class MethodologyList(generic.VulnmanAuthListView):
    template_name = "methodologies/methodology_list.html"
    model = models.Methodology
    context_object_name = "methodologies"


class MethodologyDetail(generic.VulnmanAuthDetailView):
    template_name = "methodologies/methodology_detail.html"
    model = models.Methodology
    context_object_name = "methodology"


class MethodologyUpdate(generic.VulnmanAuthUpdateWithInlinesView):
    template_name = "methodologies/methodology_create.html"
    model = models.Methodology
    inlines = [forms.SuggestedCommandInline]
    form_class = forms.MethodologyForm


class MethodologyDelete(generic.VulnmanAuthDeleteView):
    http_method_names = ["post"]
    model = models.Methodology
    success_url = reverse_lazy('methodology:methodology-list')


class MethodologyCreate(generic.VulnmanAuthCreateWithInlinesView):
    template_name = "methodologies/methodology_create.html"
    form_class = forms.MethodologyForm
    inlines = [forms.SuggestedCommandInline]
    model = models.Methodology


class SuggestedCommandUpdate(generic.VulnmanAuthUpdateView):
    template_name = "methodologies/suggested_command_update.html"
    form_class = forms.SuggestedCommandForm
    model = models.SuggestedCommand

    def get_success_url(self):
        return reverse_lazy('methodology:methodology-detail', kwargs={'pk': self.get_object().methodology.pk})

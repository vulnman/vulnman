from django import forms
from apps.findings import models
from dal import autocomplete
from vulnman.forms import NamedInlineFormSetFactory
from apps.networking.models import Service


class TemplateForm(forms.ModelForm):
    class Meta:
        model = models.Template
        exclude = ["uuid", "creator"]


class VulnerabilityForm(forms.ModelForm):
    template = forms.ModelChoiceField(queryset=models.Template.objects.all(), required=False,
                                      widget=autocomplete.ModelSelect2(url="findings:template-autocomplete"))

    class Meta:
        model = models.Vulnerability
        exclude = ["uuid", "creator", "project", "cvss_score", "command_created"]

    field_order = ["template"]

    def __init__(self, project, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['host'].queryset = project.host_set.all()
        self.fields['service'].queryset = Service.objects.filter(host__project=project)
        self.fields['template'].widget.attrs = {'data-theme': 'bootstrap5'}

    class Media:
        css = {"all": ['/static/css/codemirror.min.css']}
        js = ["/static/js/codemirror/codemirror.min.js", "/static/js/codemirror/markdown.min.js"]


class ProofOfConceptInline(NamedInlineFormSetFactory):
    model = models.ProofOfConcept
    exclude = ["uuid", "vulnerability", "creator", "command_created", "project"]
    factory_kwargs = {'extra': 1, 'can_delete': True, 'max_num': 4}


class VulnerabilitydetailInline(NamedInlineFormSetFactory):
    model = models.VulnerabilityDetails
    exclude = ["uuid", "vulnerability", "creator", "command_created", "project", "template"]
    factory_kwargs = {"extra": 1, "can_delete": False, "max_num": 1}

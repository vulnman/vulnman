from django import forms
from dal import autocomplete
from vulnman.forms import NamedInlineFormSetFactory
from vulns import models


class VulnerabilityForm(forms.ModelForm):
    class Meta:
        model = models.Vulnerability
        exclude = ["uuid", "creator", "project", "cvss_base_score"]
        widgets = {
            'vulnerability_template': autocomplete.ModelSelect2(url='vulns:vuln-template-autocomplete'),

        }

    def __init__(self, project, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['host'].queryset = project.host_set.all()
        self.fields['vulnerability_template'].widget.attrs = {'data-theme': 'bootstrap5'}


class HostForm(forms.ModelForm):
    class Meta:
        model = models.Host
        exclude = ["uuid", "project", "creator"]


class VulnerabilityTemplateForm(forms.ModelForm):
    class Meta:
        model = models.VulnerabilityTemplate
        exclude = ["uuid", "creator"]


class HostnameInline(NamedInlineFormSetFactory):
    model = models.Hostname
    exclude = ["uuid", "host"]
    factory_kwargs = {'extra': 1, 'can_delete': True, 'max_num': 4}


class ProofOfConceptInline(NamedInlineFormSetFactory):
    model = models.ProofOfConcept
    exclude = ["uuid", "vuln", "creator"]
    factory_kwargs = {'extra': 1, 'can_delete': True, 'max_num': 4}


class WebApplicationUrlPathForm(forms.ModelForm):
    class Meta:
        model = models.WebApplicationUrlPath
        fields = ["web_application"]

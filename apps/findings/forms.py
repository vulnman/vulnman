from django import forms
from apps.findings import models
from dal import autocomplete
from crispy_forms.helper import FormHelper
from crispy_forms import layout
from crispy_bootstrap5 import bootstrap5
from crispy_forms.bootstrap import FormActions
from vulnman.forms import NamedInlineFormSetFactory
from apps.networking.models import Service


class TemplateForm(forms.ModelForm):
    class Meta:
        model = models.Template
        fields = ["name", "description", "resolution", "ease_of_resolution", "cve_id"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = layout.Layout(
            layout.Row(
                layout.Div(
                    bootstrap5.FloatingField("name"), css_class="col-sm-12 col-md-6"
                ),
                layout.Div(
                    bootstrap5.FloatingField("ease_of_resolution"), css_class="col-sm-12 col-md-6"
                ),
                layout.Div(
                    bootstrap5.FloatingField("cve_id"), css_class="col-sm-12 col-md-12"
                ),
                layout.Div(
                    bootstrap5.FloatingField("description"), css_class="col-sm-12 col-md-12"
                ),
                layout.Div(
                    bootstrap5.FloatingField("resolution"), css_class="col-sm-12 col-md-12"
                ),
            ),
            layout.Row(
                FormActions(
                    layout.Submit('submit', 'Submit', css_class="btn-primary w-100"),
                    wrapper_class="col-sm-12 col-md-6"
                )
            )
        )


class VulnerabilityForm(forms.ModelForm):
    template = forms.ModelChoiceField(queryset=models.Template.objects.all(), required=True,
                                      widget=autocomplete.ModelSelect2(url="findings:template-autocomplete"))

    class Meta:
        model = models.Vulnerability
        fields = ["template", "service", "host", "details", "cvss_vector", "request", "response", "method",
                  "parameter", "parameters", "path", "query_parameters", "site", "is_fixed", "exclude_from_report"]

    def __init__(self, project, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['host'].queryset = project.host_set.all()
        self.fields['service'].queryset = Service.objects.filter(host__project=project)
        self.fields['template'].widget.attrs = {'data-theme': 'bootstrap5'}
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = layout.Layout(
            layout.Row(
                bootstrap5.FloatingField("template", wrapper_class="col-sm-12")
            ),
            layout.Row(
                layout.Div(
                    bootstrap5.FloatingField("service"), css_class="col-sm-12 col-md-6",
                ),
                layout.Div(
                    bootstrap5.FloatingField("host"), css_class="col-sm-12 col-md-6",
                ),
            ),
            layout.Row(
                layout.Div(
                    bootstrap5.FloatingField("method"), css_class="col-sm-12 col-md-3",
                ),
                layout.Div(
                    bootstrap5.FloatingField("parameter"), css_class="col-sm-12 col-md-3",
                ),
                layout.Div(
                    bootstrap5.FloatingField("path"), css_class="col-sm-12 col-md-3",
                ),
                layout.Div(
                    bootstrap5.FloatingField("site"), css_class="col-sm-12 col-md-3",
                ),
            ),
            layout.Row(
                layout.Div(
                    bootstrap5.FloatingField("query_parameters"), css_class="col-sm-12 col-md-6",
                ),
                layout.Div(bootstrap5.Field("is_fixed"),
                           css_class="col-sm-12 col-md-3 form-check-form-check-inline form-switch"),
                layout.Div(bootstrap5.Field("exclude_from_report"),
                           css_class="col-sm-12 col-md-3 form-check-form-check-inline form-switch"),
            ),
            layout.Row(
                layout.Div(
                    bootstrap5.FloatingField("cvss_vector", css_class="mb-2"), css_class="col-sm-12 col-md-6 h-100",
                ),
                layout.Div(
                    bootstrap5.FloatingField("details", css_class="mb-2 h-100"), css_class="col-sm-12 col-md-6 h-100",
                ),
            ),
            layout.Row(
                bootstrap5.Field("request", wrapper_class="col-sm-12 col-md-6"),
                bootstrap5.Field("response", wrapper_class="col-sm-12 col-md-6"), css_class="mt-2"
            )
        )


class ProofOfConceptInline(NamedInlineFormSetFactory):
    model = models.ProofOfConcept
    fields = ["name", "description", "image", "is_code"]
    factory_kwargs = {'extra': 1, 'can_delete': True, 'max_num': 4}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def construct_formset(self):
        formset = super().construct_formset()
        formset.helper = FormHelper()
        formset.helper.form_tag = False
        formset.helper.disable_csrf = True
        formset.helper.render_unmentioned_fields = True
        formset.helper.layout = layout.Layout(
            layout.Row(
                layout.Div(
                    bootstrap5.FloatingField("name"),
                    css_class="col-sm-12 col-md-6"
                ),
                layout.Div(
                    bootstrap5.FloatingField("image"), css_class="col-sm-12 col-md-4"
                ),
                layout.Div(bootstrap5.Field("is_code"),
                           css_class="col-sm-12 col-md-2 form-check-form-check-inline form-switch"),
            ),
            layout.Row(
                layout.Div(
                    bootstrap5.FloatingField("description"),
                    css_class="col-sm-12"
                )
            )
        )
        for form in formset.forms:
            form.fields["image"].label = ""
        return formset

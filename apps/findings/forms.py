from django import forms
from apps.findings import models
from dal import autocomplete
from crispy_forms.helper import FormHelper
from crispy_forms import layout
from crispy_forms.bootstrap import FormActions
from crispy_bootstrap5 import bootstrap5
from vulnman.forms import NamedInlineFormSetFactory, CodeMirrorWidget
from apps.networking.models import Service


ASSET_TYPE_CHOICES = [
    ("webapp", "Web Application"),
    ("webrequest", "Web Request"),
    ("host", "Host"),
    ("service", "Service")
]


class TemplateForm(forms.ModelForm):
    class Meta:
        model = models.Template
        fields = ["name", "description", "recommendation"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = layout.Layout(
            layout.Row(
                layout.Div(
                    bootstrap5.FloatingField("name"), css_class="col-sm-12 col-md-6"
                ),
                layout.Div(
                    bootstrap5.FloatingField("cve_id"), css_class="col-sm-12 col-md-12"
                ),
                layout.Div(
                    bootstrap5.Field("description"), css_class="col-sm-12 col-md-12"
                ),
                layout.Div(
                    bootstrap5.Field("recommendation"), css_class="col-sm-12 col-md-12"
                ),
            )
        )



class TextProofForm(forms.ModelForm):
    class Meta:
        model = models.TextProof
        fields = ["name", "description", "text"]
        widgets = {
            "text": CodeMirrorWidget()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = layout.Layout(
            layout.Row(
                bootstrap5.FloatingField("name", wrapper_class="col-sm-12"),
                bootstrap5.Field("description", wrapper_class="col-sm-12"),
                bootstrap5.Field("text", wrapper_class="col-sm-12")
            )
        )


class ImageProofForm(forms.ModelForm):
    class Meta:
        model = models.ImageProof
        fields = ["name", "description", "image"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = layout.Layout(
            layout.Row(
                bootstrap5.FloatingField("name", wrapper_class="col-sm-12"),
                bootstrap5.Field("description", wrapper_class="col-sm-12"),
                bootstrap5.Field("image", wrapper_class="col-sm-12")
            )
        )


class ProofOrderingForm(forms.Form):
    pk = forms.UUIDField()
    order = forms.IntegerField(min_value=0)

    class Meta:
        fields = ["order", "pk"]


class VulnerabilityForm(forms.ModelForm):
    template = forms.ModelChoiceField(queryset=models.Template.objects.all(), required=True,
                                      widget=autocomplete.ModelSelect2(url="findings:template-autocomplete"))
    asset_type = forms.ChoiceField(choices=ASSET_TYPE_CHOICES)
    f_asset = forms.ChoiceField(choices=[], label="Asset")

    class Meta:
        model = models.Vulnerability
        fields = ["template", "cvss_vector", "name", "asset_type", "f_asset", "is_fixed", "verified", "cve_id"]

    def get_asset_choices(self, project):
        choices = [("---", "---")]
        for i in project.webapplication_set.all():
            d_name = "%s (%s)" % (i.name, "Web Application")
            choices.append((str(i.pk), d_name))
        for i in project.webrequest_set.all():
            d_name = "%s (%s)" % (i.name, "Web Request")
            choices.append((str(i.pk), d_name))
        return choices

    def __init__(self, project, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["f_asset"].choices = self.get_asset_choices(project)
        self.fields['template'].widget.attrs = {'data-theme': 'bootstrap5'}
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = layout.Layout(
            layout.Row(
                bootstrap5.Field("template", wrapper_class="col-sm-12")
            ),
            layout.Row(
                layout.Div(
                    bootstrap5.FloatingField("name"), css_class="col-sm-12",
                ),
            ),
            layout.Row(
                layout.Div(
                    bootstrap5.FloatingField('asset_type'), css_class="col-sm-12 col-md-6"
                ),
                layout.Div(
                    bootstrap5.FloatingField('f_asset'), css_class="col-sm-12 col-md-6"
                )
            ),
            layout.Row(
                layout.Div(
                    bootstrap5.FloatingField("cve_id"), css_class="col-sm-12 col-md-6",
                ),
                layout.Div(bootstrap5.Field("is_fixed"),
                           css_class="col-sm-12 col-md-2 form-check-form-check-inline form-switch"),
                layout.Div(bootstrap5.Field("verified"),
                           css_class="col-sm-12 col-md-2 form-check-form-check-inline form-switch"),
            ),
            layout.Row(
                layout.Div(
                    bootstrap5.FloatingField("cvss_vector", css_class="mb-2"), css_class="col-sm-12 h-100",
                )
            )
        )


class ReferenceInline(NamedInlineFormSetFactory):
    model = models.Reference
    fields = ["name"]
    factory_kwargs = {'extra': 1, 'can_delete': True, 'max_num': 4}

    def construct_formset(self):
        formset = super().construct_formset()
        formset.helper = FormHelper()
        formset.helper.form_tag = False
        formset.helper.disable_csrf = True
        formset.helper.render_unmentioned_fields = True
        formset.helper.layout = layout.Layout(
            layout.Row(
                layout.Div(bootstrap5.FloatingField("name"), css_class="col-sm-12 col-md-12")
            )
        )
        return formset


class UserAccountForm(forms.ModelForm):
    class Meta:
        model = models.UserAccount
        fields = ["username", "password", "role", "account_compromised"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_action = "projects:findings:user-account-create"
        self.helper.layout = layout.Layout(
            layout.Row(
                bootstrap5.FloatingField("username", wrapper_class="col-sm-12"),
                bootstrap5.FloatingField("password", wrapper_class="col-sm-12"),
                bootstrap5.FloatingField("role", wrapper_class="col-sm-12"),
                bootstrap5.Field("account_compromised", wrapper_class="col-sm-12")

            ),
            layout.Row(
                FormActions(layout.Submit("submit", "Submit", css_class="btn btn-primary w-100"),
                            wrapper_class="col-sm-12 col-md-6")
            )
        )

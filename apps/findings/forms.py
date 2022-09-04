from django import forms
from django.conf import settings
from apps.findings import models
from crispy_forms.helper import FormHelper
from crispy_forms import layout
from crispy_forms.bootstrap import FormActions
from crispy_bootstrap5 import bootstrap5
from vulnman.core.forms import CodeMirrorWidget, FileDropWidget


class TextProofForm(forms.ModelForm):
    class Meta:
        model = models.TextProof
        fields = ["name", "description", "text"]
        widgets = {
            "text": CodeMirrorWidget(),
            "description": CodeMirrorWidget()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = layout.Layout(
            layout.Row(
                bootstrap5.FloatingField("name", wrapper_class="col-sm-12"),
                bootstrap5.Field("description", wrapper_class="col-sm-12"),
                bootstrap5.Field("text", wrapper_class="col-sm-12"),
                css_class="g-2"
            ),
            layout.Row(
                FormActions(layout.Submit("submit", "Submit", css_class="btn btn-primary w-100"),
                            wrapper_class="col-sm-12 col-md-6")
            )
        )


class ImageProofForm(forms.ModelForm):
    class Meta:
        model = models.ImageProof
        fields = ["name", "description", "image", "caption"]
        widgets = {
            'image': FileDropWidget(),
            'description': CodeMirrorWidget()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = layout.Layout(
            layout.Row(
                bootstrap5.FloatingField("name", wrapper_class="col-sm-12"),
                bootstrap5.FloatingField("caption", wrapper_class="col-sm-12"),
                bootstrap5.Field("description", wrapper_class="col-sm-12"),
                bootstrap5.Field("image", wrapper_class="col-sm-12"),
                css_class="g-2"
            ),
            layout.Row(
                FormActions(layout.Submit("submit", "Submit", css_class="btn btn-primary w-100"),
                            wrapper_class="col-sm-12 col-md-6")
            )
        )


class VulnerabilityCVSSBaseForm(forms.ModelForm):
    class Meta:
        model = models.Vulnerability
        fields = ["cvss_av", "cvss_ac", "cvss_pr", "cvss_ui", "cvss_s", "cvss_c", "cvss_i", "cvss_a"]
        labels = {
            "cvss_av": "Attack Vector", "cvss_ac": "Attack Complexity",
            "cvss_pr": "Privileges Required", "cvss_ui": "User Interaction",
            "cvss_s": "Scope", "cvss_c": "Confidentiality", "cvss_i": "Integrity", "cvss_a": "Availability"
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = layout.Layout(
            layout.Row(
                bootstrap5.FloatingField("cvss_av", wrapper_class="col-sm-12 col-md-6"),
                bootstrap5.FloatingField("cvss_ac", wrapper_class="col-sm-12 col-md-6"),
                css_class="g-2"
            ),
            layout.Row(
                bootstrap5.FloatingField("cvss_pr", wrapper_class="col-sm-12 col-md-6"),
                bootstrap5.FloatingField("cvss_ui", wrapper_class="col-sm-12 col-md-6"),
                css_class="g-2"
            ),
            layout.Row(
                bootstrap5.FloatingField("cvss_s", wrapper_class="col-sm-12 col-md-6"),
                bootstrap5.FloatingField("cvss_c", wrapper_class="col-sm-12 col-md-6"),
                css_class="g-2"
            ),
            layout.Row(
                bootstrap5.FloatingField("cvss_i", wrapper_class="col-sm-12 col-md-6"),
                bootstrap5.FloatingField("cvss_a", wrapper_class="col-sm-12 col-md-6"),
                css_class="g-2"
            ),
            layout.Row(
                FormActions(layout.Submit("submit", "Submit", css_class="btn btn-primary w-100"),
                            wrapper_class="col-sm-12 col-md-6")
            )
        )


class ProofOrderingForm(forms.Form):
    pk = forms.UUIDField()
    order = forms.IntegerField(min_value=0)

    class Meta:
        fields = ["order", "pk"]


class VulnerabilityForm(forms.ModelForm):
    template_id = forms.CharField(label="Template", widget=forms.Select())
    f_asset = forms.ChoiceField(choices=[], label="Asset")

    class Meta:
        model = models.Vulnerability
        fields = ["template_id", "name", "asset_type", "f_asset", "status", "cve_id", "severity",
                  "auth_required", "user_account"]

    def get_asset_choices(self, project):
        choices = []
        for asset in project.get_assets():
            choices.append((asset.pk, asset.name))
        return choices

    def __init__(self, project, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["f_asset"].choices = self.get_asset_choices(project)
        self.fields["user_account"].queryset = project.useraccount_set.all()
        self.helper = FormHelper()
        self.helper.layout = layout.Layout(
            layout.Row(
                layout.Div(
                    bootstrap5.FloatingField("template_id"), css_class="col-sm-12",
                ),
            ),
            layout.Row(
                layout.Div(
                    bootstrap5.FloatingField("name"), css_class="col-sm-12",
                ),
            ),
            layout.Row(
                layout.Div(
                    bootstrap5.FloatingField("severity"), css_class="col-sm-12 col-md-6",
                ),
                layout.Div(
                    bootstrap5.FloatingField("user_account"), css_class="col-sm-12 col-md-6",
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
                layout.Div(bootstrap5.FloatingField("status"), css_class="col-sm-12 col-md-6"),
            ),
            layout.Row(
                FormActions(layout.Submit("submit", "Submit", css_class="btn btn-primary w-100"),
                            wrapper_class="col-sm-12 col-md-6")
            )
        )


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
                bootstrap5.Field("account_compromised", wrapper_class="col-sm-12"),
                css_class="g-2"
            ),
            layout.Row(
                FormActions(layout.Submit("submit", "Submit", css_class="btn btn-primary w-100"),
                            wrapper_class="col-sm-12 col-md-6")
            )
        )


class UserAccountUpdateForm(UserAccountForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.form_action = "projects:findings:user-account-update"


def get_template_choices():
    choices = []
    for item in settings.REPORT_TEMPLATES.keys():
        choices.append((item, item))
    return choices


class VulnerabilityExportForm(forms.Form):
    template = forms.ChoiceField(choices=get_template_choices())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = layout.Layout(
            layout.Row(
                bootstrap5.FloatingField("template", wrapper_class="col-sm-12"), css_class="g-2"
            ),
            layout.Row(
                FormActions(layout.Submit("submit", "Submit", css_class="btn btn-primary w-100"),
                            wrapper_class="col-sm-12 col-md-6")
            )
        )
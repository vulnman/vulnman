from django import forms
from crispy_forms import layout
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import FormActions
from crispy_bootstrap5 import bootstrap5
from apps.reporting import models
from vulnman.forms import DateInput


class ReportForm(forms.ModelForm):
    class Meta:
        model = models.Report
        fields = ["revision", "changes", "is_draft", "custom_title"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_action = "projects:reporting:report-create"
        self.helper.layout = layout.Layout(
            layout.Row(
                layout.Div(
                    bootstrap5.FloatingField("custom_title"), css_class="col-sm-12 col-md-6"
                )
            ),
            layout.Row(
                layout.Div(
                    bootstrap5.FloatingField("revision"), css_class="col-sm-12 col-md-6"
                ),
                layout.Div(
                    bootstrap5.Field("is_draft"), css_class="col-sm-12 col-md-3 form-switch"
                ),
                layout.Div(
                    bootstrap5.FloatingField("changes"), css_class="col-sm-12"
                ),
            ),
            layout.Row(
                FormActions(layout.Submit("submit", "Submit", css_class="btn btn-primary w-100"),
                            wrapper_class="col-sm-12 col-md-6")
            )
        )


class ReportUpdateForm(forms.ModelForm):
    class Meta:
        model = models.Report
        fields = ['raw_source']


class ReportShareTokenForm(forms.ModelForm):
    class Meta:
        model = models.ReportShareToken
        fields = ["date_expires"]
        widgets = {
            "date_expires": DateInput()
        }

from django import forms
from crispy_forms import layout
from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_bootstrap5 import bootstrap5
from apps.reporting import models
from vulnman.forms import DateInput
from vulnman.forms import CodeMirrorWidget


class PentestReportDraftForm(forms.ModelForm):
    empty = forms.CharField(required=False)

    class Meta:
        model = models.PentestReport
        fields = ["empty"]


class ReportShareTokenForm(forms.ModelForm):
    class Meta:
        model = models.ReportShareToken
        fields = ["date_expires"]
        widgets = {
            "date_expires": DateInput()
        }


class ReportManagementSummaryForm(forms.ModelForm):
    class Meta:
        model = models.ReportInformation
        fields = ["evaluation", "recommendation"]
        widgets = {
            "evaluation": CodeMirrorWidget(),
            "recommendation": CodeMirrorWidget()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = layout.Layout(
            layout.Row(
                bootstrap5.Field("evaluation", wrapper_class="col-sm-12"),
                bootstrap5.Field("recommendation", wrapper_class="col-sm-12"),
            )
        )


class PentestReportForm(forms.ModelForm):
    class Meta:
        model = models.PentestReport
        fields = ["name", "report_type"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_action = "projects:reporting:report-create"
        self.helper.layout = layout.Layout(
            layout.Row(
                bootstrap5.FloatingField("name", wrapper_class="col-sm-12"),
                bootstrap5.FloatingField(
                    "report_type", wrapper_class="col-sm-12")
            ),
            layout.Row(
                FormActions(layout.Submit("submit", "Submit", css_class="btn btn-primary w-100"),
                            wrapper_class="col-sm-12 col-md-6")
            )
        )

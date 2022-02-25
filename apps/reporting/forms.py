from django import forms
from crispy_forms import layout
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import FormActions
from crispy_bootstrap5 import bootstrap5
from apps.reporting import models
from vulnman.forms import DateInput
from vulnman.forms import CodeMirrorWidget


class PentestReportDraftForm(forms.ModelForm):
    empty = forms.CharField(required=False)

    class Meta:
        model = models.PentestReport
        fields = ["empty"]


class PentestReportCreateForm(forms.ModelForm):
    class Meta:
        model = models.PentestReport
        fields = ["author"]


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


class ReportManagementForm(forms.ModelForm):
    class Meta:
        model = models.PentestReport
        fields = ["mgmt_summary_evaluation", "mgmt_summary_recommendation"]
        widgets = {
            "mgmt_summary_evaluation": CodeMirrorWidget(),
            "mgmt_summary_recommendation": CodeMirrorWidget()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = layout.Layout(
            layout.Row(
                bootstrap5.FloatingField("mgmt_summary_evaluation", wrapper_class="col-sm-12"),
                bootstrap5.Field("mgmt_summary_recommendation", wrapper_class="col-sm-12"),
            )
        )

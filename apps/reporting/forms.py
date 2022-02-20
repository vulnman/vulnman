from django import forms
from crispy_forms import layout
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import FormActions
from crispy_bootstrap5 import bootstrap5
from apps.reporting import models
from vulnman.forms import DateInput


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

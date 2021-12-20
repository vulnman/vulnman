from django import forms
from apps.reporting import models
from vulnman.forms import DateInput


class ReportForm(forms.ModelForm):
    class Meta:
        model = models.Report
        exclude = ["uuid", "project", "creator", "raw_source"]


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

from django import forms
from apps.reporting import models


class ReportForm(forms.ModelForm):
    class Meta:
        model = models.Report
        exclude = ["uuid", "project", "creator", "raw_source"]


class ReportUpdateForm(forms.ModelForm):
    class Meta:
        model = models.Report
        fields = ['raw_source']

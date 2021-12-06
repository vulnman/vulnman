from django import forms
from apps.findings import models


class TemplateForm(forms.ModelForm):
    class Meta:
        model = models.Template
        exclude = ["uuid", "creator"]

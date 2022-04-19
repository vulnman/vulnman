from django import forms
from core import models


class ProjectTaskStatusUpdateForm(forms.ModelForm):
    class Meta:
        model = models.AssetTask
        fields = ["status"]

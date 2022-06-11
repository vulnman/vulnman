from django import forms
from apps.methodologies import models


class ProjectTaskStatusUpdateForm(forms.ModelForm):
    class Meta:
        model = models.AssetTask
        fields = ["status"]

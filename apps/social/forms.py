from django import forms
from apps.social import models
from apps.networking.models import Service


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = models.Employee
        exclude = ["uuid", "project", "creator", "command_created"]


class CredentialForm(forms.ModelForm):
    class Meta:
        model = models.Credential
        exclude = ["uuid", "project", "creator", "command_created"]

    def __init__(self, project, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['valid_services'].queryset = Service.objects.filter(host__project=project)

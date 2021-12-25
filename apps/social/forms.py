from crispy_forms.bootstrap import FormActions
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms import layout
from crispy_bootstrap5 import bootstrap5
from apps.social import models
from apps.networking.models import Service


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = models.Employee
        exclude = ["uuid", "project", "creator", "command_created"]


class CredentialForm(forms.ModelForm):
    class Meta:
        model = models.Credential
        fields = ["username", "valid_services", "location_found", "employee", "cleartext_password",
                  "hashed_password", "description"]

    def __init__(self, project, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['valid_services'].queryset = Service.objects.filter(host__project=project)
        self.helper = FormHelper()
        self.helper.layout = layout.Layout(
            layout.Row(
                layout.Div(bootstrap5.FloatingField("username"), css_class="col-sm-12 col-md-4"),
                layout.Div(bootstrap5.FloatingField("location_found"), css_class="col-sm-12 col-md-4"),
                layout.Div(bootstrap5.FloatingField("employee"), css_class="col-sm-12 col-md-4")
            ),
            layout.Row(
                layout.Div(bootstrap5.FloatingField("cleartext_password"), css_class="col-sm-12 col-md-6"),
                layout.Div(bootstrap5.FloatingField("hashed_password"), css_class="col-sm-12 col-md-6")
            ),
            layout.Row(
                layout.Div(bootstrap5.Field("description"), css_class="col-sm-12")
            ),
            layout.Row(
                FormActions(
                    layout.Submit('submit', 'Submit', css_class="btn-primary w-100"),
                    wrapper_class="col-sm-12 col-md-6")
            )
        )

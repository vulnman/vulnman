from crispy_forms.bootstrap import FormActions
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms import layout
from crispy_bootstrap5 import bootstrap5
from apps.account import models


class ProfileForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = models.Profile
        fields = ["pgp_fingerprint", "position", "hide_name_in_report", "email"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = layout.Layout(
            layout.Row(
                layout.Div(bootstrap5.FloatingField("pgp_fingerprint"), css_class="col-sm-12 col-md-8"),
                layout.Div(bootstrap5.Field("hide_name_in_report"),
                           css_class="col-sm-12 col-md-4 form-check-form-check-inline form-switch")
            ),
            layout.Row(
                layout.Div(bootstrap5.FloatingField("position"), css_class="col-sm-12 col-md-6"),
                layout.Div(bootstrap5.FloatingField("email"), css_class="col-sm-12 col-md-6")
            ),
            layout.Row(
                FormActions(
                    layout.Submit('submit', 'Submit', css_class="btn-primary w-100"),
                    wrapper_class="col-sm-12 col-md-6"
                )
            )
        )

from django import forms
from apps.assets import models
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import FormActions
from crispy_bootstrap5 import bootstrap5
from crispy_forms import layout


class WebApplicationForm(forms.ModelForm):
    class Meta:
        model = models.WebApplication
        fields = ["name", "base_url", "description"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_action = "projects:assets:webapp-create"
        self.helper.layout = layout.Layout(
            layout.Row(
                bootstrap5.FloatingField("name", wrapper_class="col-sm-12"),
                bootstrap5.FloatingField("base_url", wrapper_class="col-sm-12"),
                bootstrap5.Field("description", wrapper_class="col-sm-12"),
            ),
            layout.Row(
                FormActions(layout.Submit("submit", "Submit", css_class="btn btn-primary w-100"),
                            wrapper_class="col-sm-12 col-md-6")
            )
        )


class WebRequestCreateForm(forms.ModelForm):
    class Meta:
        model = models.WebRequest
        fields = ["web_app", "url", "parameter", "description"]

    def __init__(self, project, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["web_app"].queryset = project.webapplication_set.all()
        self.helper = FormHelper()
        self.helper.form_action = "projects:assets:webrequest-create"
        self.helper.layout = layout.Layout(
            layout.Row(
                bootstrap5.FloatingField("web_app", wrapper_class="col-sm-12"),
                bootstrap5.FloatingField("url", wrapper_class="col-sm-12"),
                bootstrap5.FloatingField("parameter", wrapper_class="col-sm-12"),
                bootstrap5.Field("description", wrapper_class="col-sm-12")
            ),
            layout.Row(
                FormActions(layout.Submit("submit", "Submit", css_class="btn btn-primary w-100"),
                            wrapper_class="col-sm-12 col-md-6")
            )
        )


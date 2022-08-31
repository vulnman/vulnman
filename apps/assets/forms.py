from django import forms
from django.urls import reverse_lazy
from apps.assets import models
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import FormActions
from crispy_bootstrap5 import bootstrap5
from crispy_forms import layout


class WebApplicationForm(forms.ModelForm):
    class Meta:
        model = models.WebApplication
        fields = ["name", "base_url", "description", "hide_from_report", "environment", "accessibility"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = layout.Layout(
            layout.Row(
                bootstrap5.FloatingField("name", wrapper_class="col-sm-12"),
                bootstrap5.FloatingField("base_url", wrapper_class="col-sm-12"),
                bootstrap5.FloatingField("environment", wrapper_class="col-sm-12"),
                bootstrap5.FloatingField("accessibility", wrapper_class="col-sm-12"),
                bootstrap5.Field("description", wrapper_class="col-sm-12"),
                bootstrap5.Field("hide_from_report", wrapper_class="col-sm-12"),
                css_class="g-2"
            ),
            layout.Row(
                FormActions(layout.Submit("submit", "Submit", css_class="btn btn-primary w-100"),
                            wrapper_class="col-sm-12 col-md-6")
            )
        )


class HostForm(forms.ModelForm):
    class Meta:
        model = models.Host
        fields = ["ip", "operating_system", "accessibility", "dns", "hide_from_report", "description", "environment"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = layout.Layout(
            layout.Row(
                bootstrap5.FloatingField("ip", wrapper_class="col-sm-12"),
                bootstrap5.FloatingField("operating_system", wrapper_class="col-sm-12"),
                css_class="g-2"
            ),
            layout.Row(
                bootstrap5.FloatingField("accessibility", wrapper_class="col-sm-12 col-md-6"),
                bootstrap5.FloatingField("dns", wrapper_class="col-sm-12 col-md-6"),
                css_class="g-2"
            ),
            bootstrap5.FloatingField("environment", wrapper_class="col-sm-12"),
            bootstrap5.Field("description", wrapper_class="col-sm-12"),
            bootstrap5.Field("hide_from_report", wrapper_class="col-sm-12"),
            layout.Row(
                FormActions(layout.Submit("submit", "Submit", css_class="btn btn-primary w-100"),
                            wrapper_class="col-sm-12 col-md-6")
            )
        )


class ServiceForm(forms.ModelForm):
    class Meta:
        model = models.Service
        fields = ["host", "port", "name", "protocol", "state", "banner", "hide_from_report"]

    def __init__(self, project, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields["host"].queryset = project.host_set.all()
        self.helper.layout = layout.Layout(
            layout.Row(
                bootstrap5.FloatingField("host", wrapper_class="col-sm-12 col-md-6"),
                bootstrap5.FloatingField("port", wrapper_class="col-sm-12 col-md-6"),
                css_class="g-2"
            ),
            layout.Row(
                bootstrap5.FloatingField("name", wrapper_class="col-sm-12 col-md-6"),
                bootstrap5.FloatingField("protocol", wrapper_class="col-sm-12 col-md-6"),
                css_class="g-2"
            ),
            layout.Row(
                bootstrap5.FloatingField("state", wrapper_class="col-sm-12 col-md-6"),
                bootstrap5.FloatingField("banner", wrapper_class="col-sm-12 col-md-6"),
                css_class="g-2"
            ),
            bootstrap5.Field("hide_from_report", wrapper_class="col-sm-12"),
            layout.Row(
                FormActions(layout.Submit("submit", "Submit", css_class="btn btn-primary w-100"),
                            wrapper_class="col-sm-12 col-md-6")
            )
        )


class ServiceUpdateForm(ServiceForm):

    def __init__(self, project, *args, **kwargs):
        super().__init__(project, *args, **kwargs)
        self.helper.form_action = reverse_lazy(
            "projects:assets:service-update", kwargs={"pk": self.instance.pk})

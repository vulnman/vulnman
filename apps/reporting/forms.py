from django import forms
from django.conf import settings
from crispy_forms import layout
from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_bootstrap5 import bootstrap5
from apps.reporting import models
from vulnman.forms import CodeMirrorWidget


def get_report_templates():
    choices = []
    for template in settings.REPORT_TEMPLATES.keys():
        choices.append((template, template))
    return choices


class PentestReportDraftForm(forms.ModelForm):
    empty = forms.CharField(required=False)

    class Meta:
        model = models.PentestReport
        fields = ["empty"]


class ReportManagementSummaryForm(forms.ModelForm):
    class Meta:
        model = models.ReportInformation
        fields = ["evaluation", "recommendation"]
        widgets = {
            "evaluation": CodeMirrorWidget(),
            "recommendation": CodeMirrorWidget()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = layout.Layout(
            layout.Row(
                bootstrap5.Field("evaluation", wrapper_class="col-sm-12"),
                bootstrap5.Field("recommendation", wrapper_class="col-sm-12"),
                css_class="g-2"
            )
        )


class PentestReportForm(forms.ModelForm):
    report_template = forms.ChoiceField(
        choices=get_report_templates())

    class Meta:
        model = models.PentestReport
        fields = ["name", "report_type", "report_template", "language"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_action = "projects:reporting:report-create"
        self.helper.form_tag = False
        self.helper.layout = layout.Layout(
            layout.Row(
                bootstrap5.FloatingField("name", wrapper_class="col-sm-12"),
                bootstrap5.FloatingField("language", wrapper_class="col-sm-12"),
                bootstrap5.FloatingField(
                    "report_type", wrapper_class="col-sm-12"),
                bootstrap5.FloatingField(
                    "report_template", wrapper_class="col-sm-12"),
                css_class="g-2"
            ),
            layout.Row(
                FormActions(layout.Submit("submit", "Submit", css_class="btn btn-primary w-100"),
                            wrapper_class="col-sm-12 col-md-6")
            )
        )

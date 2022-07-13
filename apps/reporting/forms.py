from django import forms
from django.conf import settings
from crispy_forms import layout
from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_bootstrap5 import bootstrap5
from apps.reporting import models
from apps.account.models import User
from vulnman.core.forms import CodeMirrorWidget, DateInput


def get_report_templates():
    choices = []
    for template in settings.REPORT_TEMPLATES.keys():
        choices.append((template, template))
    return choices


class ReportCreateForm(forms.ModelForm):
    class Meta:
        model = models.Report
        fields = ["author", "title", "language", "name", "template"]

    def __init__(self, project, *args, **kwargs):
        super().__init__(*args, **kwargs)
        available_author_pks = list(project.projectcontributor_set.values_list("user__pk", flat=True))
        available_author_pks.append(project.creator.pk)
        available_authors = User.objects.filter(pk__in=available_author_pks)
        self.fields["author"].queryset = available_authors
        self.helper = FormHelper()
        self.helper.layout = layout.Layout(
            layout.Row(
                layout.Div(
                    bootstrap5.FloatingField("name", wrapper_class="col-sm-12")
                ),
                layout.Div(
                    bootstrap5.FloatingField("author", wrapper_class="col-sm-12")
                ),
                layout.Div(
                    bootstrap5.FloatingField("title", wrapper_class="col-sm-12")
                ),
                layout.Div(
                    bootstrap5.FloatingField("language", wrapper_class="col-sm-12")
                ),
                layout.Div(
                    bootstrap5.FloatingField("template", wrapper_class="col-sm-12")
                )
            ),
            layout.Row(
                FormActions(layout.Submit("submit", "Submit", css_class="btn btn-primary w-100"),
                            wrapper_class="col-sm-12 col-md-6")
            )
        )


class ReportReleaseForm(forms.ModelForm):
    class Meta:
        model = models.ReportRelease
        fields = ["name", "release_type"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = layout.Layout(
            layout.Row(
                layout.Div(
                    bootstrap5.FloatingField("name", wrapper_class="col-sm-12")
                ),
                layout.Div(
                    bootstrap5.FloatingField("release_type", wrapper_class="col-sm-12")
                )
            ),
            layout.Row(
                FormActions(layout.Submit("submit", "Submit", css_class="btn btn-primary w-100"),
                            wrapper_class="col-sm-12 col-md-6")
            )
        )


class ReportReleaseWIPForm(forms.ModelForm):
    class Meta:
        model = models.ReportRelease
        fields = ["name"]
        widgets = {
            "name": forms.HiddenInput()
        }


class ReportReleaseUpdateForm(forms.ModelForm):
    class Meta:
        model = models.ReportRelease
        fields = ["name"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = layout.Layout(
            layout.Row(
                layout.Div(
                    bootstrap5.FloatingField("name", wrapper_class="col-sm-12")
                ),
            ),
            layout.Row(
                FormActions(layout.Submit("submit", "Submit", css_class="btn btn-primary w-100"),
                            wrapper_class="col-sm-12 col-md-6")
            )
        )


class ReportManagementSummaryForm(forms.ModelForm):
    class Meta:
        model = models.Report
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


class VersionForm(forms.ModelForm):
    class Meta:
        model = models.ReportVersion
        fields = ["change", "version", "date", "user"]
        widgets = {
            "date": DateInput()
        }

    def __init__(self, project, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        user_pks = list(project.projectcontributor_set.filter(
            user__is_pentester=True).values_list("user__pk", flat=True))
        user_pks.append(project.creator.pk)
        self.fields["user"].queryset = User.objects.filter(pk__in=user_pks)
        self.helper.layout = layout.Layout(
            layout.Row(
                layout.Div(
                    bootstrap5.FloatingField("change", wrapper_class="col-sm-12")
                ),
            ),
            layout.Row(
                layout.Div(
                    bootstrap5.FloatingField("version", wrapper_class="col-sm-12")
                )
            ),
            layout.Row(
              layout.Div(
                  bootstrap5.FloatingField("user", wrapper_class="col-sm-12")
              )
            ),
            layout.Row(
                layout.Div(
                    bootstrap5.FloatingField("date", wrapper_class="col-sm-12")
                )
            ),
            layout.Row(
                FormActions(layout.Submit("submit", "Submit", css_class="btn btn-primary w-100"),
                            wrapper_class="col-sm-12 col-md-6")
            )
        )

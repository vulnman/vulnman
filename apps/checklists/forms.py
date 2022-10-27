from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import FormActions
from crispy_bootstrap5 import bootstrap5
from crispy_forms import layout
from . import models


class ChecklistForm(forms.ModelForm):
    asset = forms.ChoiceField(choices=[], label="Asset")

    class Meta:
        model = models.ProjectTask
        fields = ["task_id", "name", "description", "status", "asset", "asset_type"]

    def __init__(self, project, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["asset"].choices = self.get_asset_choices(project)
        self.helper = FormHelper()
        self.helper.layout = layout.Layout(
            layout.Row(
                layout.Div(bootstrap5.FloatingField("task_id", wrapper_class="col-sm-12")),
                layout.Div(bootstrap5.FloatingField("name", wrapper_class="col-sm-12")),
                layout.Div(bootstrap5.FloatingField("status", wrapper_class="col-sm-12")),
            ),
            layout.Row(
                layout.Div(bootstrap5.FloatingField("asset_type", wrapper_class="col-sm-12 col-md-6")),
                layout.Div(bootstrap5.FloatingField("asset", wrapper_class="col-sm-12 col-md-6"))
            ),
            layout.Row(
                layout.Div(bootstrap5.Field("description", wrapper_class="col-sm-12"))
            ),
            layout.Row(
                FormActions(layout.Submit("submit", "Submit", css_class="btn btn-primary w-100"),
                            wrapper_class="col-sm-12 col-md-6")
            )
        )

    def get_asset_choices(self, project):
        choices = []
        for asset in project.get_assets():
            choices.append((asset.pk, asset.name))
        return choices

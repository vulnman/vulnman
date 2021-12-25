from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms import layout
from crispy_bootstrap5 import bootstrap5
from apps.projects import models
from vulnman.forms import DateInput
from extra_views import InlineFormSetFactory


class ProjectForm(forms.ModelForm):
    class Meta:
        model = models.Project
        exclude = ["uuid", "creator"]
        widgets = {
            'start_date': DateInput(),
            'end_date': DateInput()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = layout.Layout(
            layout.Row(
                layout.Div(bootstrap5.FloatingField("client"), css_class="col-sm-12"),
            ),
            layout.Row(
                layout.Div(bootstrap5.FloatingField("start_date"), css_class="col-sm-12 col-md-6"),
                layout.Div(bootstrap5.FloatingField("end_date"), css_class="col-sm-12 col-md-6")
            )
        )


class ScopeInline(InlineFormSetFactory):
    model = models.Scope
    fields = ["name"]
    factory_kwargs = {'extra': 1, 'can_delete': True, 'max_num': 10}

    def construct_formset(self):
        formset = super().construct_formset()
        formset.helper = FormHelper()
        formset.helper.form_tag = False
        formset.helper.disable_csrf = True
        formset.helper.render_unmentioned_fields = True
        formset.helper.layout = layout.Layout(
            layout.Row(
                layout.Div(bootstrap5.FloatingField("name"), css_class="col-sm-12")
            )
        )
        return formset

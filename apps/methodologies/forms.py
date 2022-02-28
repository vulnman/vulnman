from django import forms
from extra_views import InlineFormSetFactory
from crispy_forms import layout
from crispy_bootstrap5 import bootstrap5
from crispy_forms.helper import FormHelper
from apps.methodologies import models


class MethodologyForm(forms.ModelForm):
    class Meta:
        model = models.Methodology
        fields = ["name"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = layout.Layout(
            layout.Row(layout.Div(bootstrap5.FloatingField("name"), css_class="col-sm-12"))
        )


class TaskInline(InlineFormSetFactory):
    model = models.Task
    fields = ["name", "description"]
    factory_kwargs = {'extra': 1, 'can_delete': True, 'max_num': 50}

    def construct_formset(self):
        formset = super().construct_formset()
        formset.helper = FormHelper()
        formset.helper.form_tag = False
        formset.helper.disable_csrf = True
        formset.helper.render_unmentioned_fields = True
        formset.helper.layout = layout.Layout(
            layout.Row(
                layout.Div(bootstrap5.FloatingField("name"), css_class="col-sm-12 col-md-12"),
                layout.Div(bootstrap5.FloatingField("description"), css_class="col-sm-12 col-md-12")
            )
        )
        return formset


class ProjectMethodologyForm(forms.ModelForm):
    class Meta:
        model = models.ProjectMethodology
        fields = ["name"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = layout.Layout(
            layout.Row(layout.Div(bootstrap5.FloatingField("name"), css_class="col-sm-12"))
        )


class ProjectTaskInline(InlineFormSetFactory):
    model = models.ProjectTask
    fields = ["name", "description"]
    factory_kwargs = {'extra': 1, 'can_delete': True, 'max_num': 50}

    def construct_formset(self):
        formset = super().construct_formset()
        formset.helper = FormHelper()
        formset.helper.form_tag = False
        formset.helper.disable_csrf = True
        formset.helper.render_unmentioned_fields = True
        formset.helper.layout = layout.Layout(
            layout.Row(
                layout.Div(bootstrap5.FloatingField("name"), css_class="col-sm-12 col-md-12"),
                layout.Div(bootstrap5.FloatingField("description"), css_class="col-sm-12 col-md-12")
            )
        )
        return formset


class CreateProjectMethodologyFromTemplateForm(forms.Form):
    template = forms.ModelChoiceField(queryset=models.Methodology.objects.all())

    class Meta:
        fields = ["template"]

from django import forms
from projects import models
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


class ProjectContactForm(forms.ModelForm):
    class Meta:
        model = models.ProjectContact
        exclude = ["pk", "project"]


class ReportForm(forms.ModelForm):
    class Meta:
        model = models.Report
        exclude = ["uuid", "project", "creator", "latex_source"]


class ReportUpdateForm(forms.ModelForm):
    class Meta:
        model = models.Report
        fields = ['latex_source']


class ProjectClassificationInline(InlineFormSetFactory):
    model = models.ProjectClassification
    exclude = ["project"]
    factory_kwargs = {'extra': 1, 'can_delete': False, 'max_num': 1}


class ProjectContactInline(InlineFormSetFactory):
    model = models.ProjectContact
    exclude = ["project"]
    factory_kwargs = {'extra': 1, 'can_delete': True, 'max_num': 5}


class ScopeInline(InlineFormSetFactory):
    model = models.Scope
    exclude = ["uuid", "project", "creator"]
    factory_kwargs = {'extra': 1, 'can_delete': True, 'max_num': 10}

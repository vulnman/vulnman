from django import forms
from extra_views import InlineFormSetFactory
from apps.methodologies import models


class MethodologyForm(forms.ModelForm):
    class Meta:
        model = models.Methodology
        exclude = ["creator", "uuid"]


class TaskInline(InlineFormSetFactory):
    model = models.Task
    exclude = ["uuid", "creator"]
    factory_kwargs = {'extra': 1, 'can_delete': True, 'max_num': 50}

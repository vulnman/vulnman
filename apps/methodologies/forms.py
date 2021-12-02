from django import forms
from extra_views import InlineFormSetFactory
from apps.methodologies import models


class SuggestedCommandInline(InlineFormSetFactory):
    model = models.SuggestedCommand
    exclude = ["uuid", "creator"]
    factory_kwargs = {'extra': 1, 'can_delete': True, 'max_num': 15}


class MethodologyForm(forms.ModelForm):
    class Meta:
        model = models.Methodology
        exclude = ["creator", "uuid"]


class SuggestedCommandForm(forms.ModelForm):
    class Meta:
        model = models.SuggestedCommand
        exclude = ["creator", "uuid", "methodology"]

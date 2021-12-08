from django import forms
from apps.agents import models


class AgentForm(forms.ModelForm):
    class Meta:
        model = models.Agent
        fields = ["name"]

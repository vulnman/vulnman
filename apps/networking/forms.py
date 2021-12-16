from django import forms
from apps.networking import models
from vulnman.forms import NamedInlineFormSetFactory


class HostForm(forms.ModelForm):
    class Meta:
        model = models.Host
        exclude = ["uuid", "project", "creator", "command_created"]


class HostnameInline(NamedInlineFormSetFactory):
    model = models.Hostname
    exclude = ["uuid", "host", "project", "creator", "command_created"]
    factory_kwargs = {'extra': 1, 'can_delete': True, 'max_num': 4}

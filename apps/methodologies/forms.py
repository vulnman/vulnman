from django import forms
from extra_views import InlineFormSetFactory
from apps.methodologies import models
from apps.networking.models import Service, Host


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


class QueueCommandForm(forms.Form):
    command = forms.ModelChoiceField(queryset=models.SuggestedCommand.objects.all())
    hosts = forms.ModelMultipleChoiceField(queryset=Host.objects.all())
    services = forms.ModelMultipleChoiceField(queryset=Service.objects.all())
    threat_ip_as_domain = forms.BooleanField()
    overwrite_scheme = forms.CharField(max_length=12)

    class Meta:
        fields = '__all__'

    def __init__(self, project, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['hosts'].queryset = Host.objects.filter(project=project)
        self.fields['services'].queryset = Service.objects.filter(host__project=project)

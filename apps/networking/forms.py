from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms import layout
from crispy_bootstrap5 import bootstrap5
from apps.networking import models
from vulnman.forms import NamedInlineFormSetFactory


class HostForm(forms.ModelForm):
    class Meta:
        model = models.Host
        fields = ["is_online", "os", "ip"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = layout.Layout(
            layout.Row(
                layout.Div(bootstrap5.FloatingField("ip"), css_class="col-sm-12 col-md-6"),
                layout.Div(bootstrap5.FloatingField("os"), css_class="col-sm-12 col-md-6")
            )
        )


class HostnameInline(NamedInlineFormSetFactory):
    model = models.Hostname
    fields = ["name"]
    factory_kwargs = {'extra': 1, 'can_delete': True, 'max_num': 4}

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

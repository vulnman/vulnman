from django import forms
from django.contrib.auth.models import User, Group
from crispy_forms.helper import FormHelper
from crispy_forms import layout
from crispy_bootstrap5 import bootstrap5
from apps.projects import models
from vulnman.forms import DateInput
from extra_views import InlineFormSetFactory


class ProjectForm(forms.ModelForm):

    class Meta:
        model = models.Project
        fields = ["client", "start_date", "end_date", "name"]
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
                layout.Div(bootstrap5.FloatingField("name"), css_class="col-sm-12")
            ),
            layout.Row(
                layout.Div(bootstrap5.FloatingField("start_date"), css_class="col-sm-12 col-md-6"),
                layout.Div(bootstrap5.FloatingField("end_date"), css_class="col-sm-12 col-md-6")
            )
        )


class ClientForm(forms.ModelForm):

    class Meta:
        model = models.Client
        fields = ["name", "street", "city", "country", "zip"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = layout.Layout(
            layout.Row(
                layout.Div(bootstrap5.FloatingField("name"), css_class="col-sm-12 col-md-12"),
            ),
            layout.Row(
                layout.Div(bootstrap5.FloatingField("street"), css_class="col-sm-12 col-md-3"),
                layout.Div(bootstrap5.FloatingField("city"), css_class="col-sm-12 col-md-3"),
                layout.Div(bootstrap5.FloatingField("country"), css_class="col-sm-12 col-md-3"),
                layout.Div(bootstrap5.FloatingField("zip"), css_class="col-sm-12 col-md-3")
            ),
        )


class ClientContactInline(InlineFormSetFactory):
    model = models.ClientContact
    fields = ["first_name", "last_name", "phone", "position", "email", "pgp_key"]
    factory_kwargs = {'extra': 1, 'can_delete': True, 'max_num': 10}

    def construct_formset(self):
        formset = super().construct_formset()
        formset.helper = FormHelper()
        formset.helper.form_tag = False
        formset.helper.disable_csrf = True
        formset.helper.render_unmentioned_fields = True
        formset.helper.layout = layout.Layout(
            layout.Row(
                layout.Div(bootstrap5.FloatingField("first_name"), css_class="col-sm-12 col-md-6"),
                layout.Div(bootstrap5.FloatingField("last_name"), css_class="col-sm-12 col-md-6")
            ),
            layout.Row(
                layout.Div(bootstrap5.FloatingField("position"), css_class="col-sm-12 col-md-4"),
                layout.Div(bootstrap5.FloatingField("phone"), css_class="col-sm-12 col-md-4"),
                layout.Div(bootstrap5.FloatingField("email"), css_class="col-sm-12 col-md-4")
            )
        )
        return formset


class ContributorForm(forms.ModelForm):
    username = forms.CharField()
    class Meta:
        model = models.ProjectContributor
        fields = ["username", "role"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = layout.Layout(
            layout.Row(
                layout.Div(bootstrap5.FloatingField("username"), css_class="col-sm-12"),
            ),
            layout.Row(
                layout.Div(bootstrap5.FloatingField("role"), css_class="col-sm-12"),
            ),
        )
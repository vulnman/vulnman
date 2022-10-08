from django import forms
from django.urls import reverse_lazy
from crispy_forms.helper import FormHelper
from crispy_forms import layout
from crispy_bootstrap5 import bootstrap5
from phonenumber_field.formfields import PhoneNumberField
from apps.projects import models
from vulnman.core.forms import DateInput, FileDropWidget, CodeMirrorWidget
from crispy_forms.bootstrap import FormActions
from apps.account.models import User


class ProjectForm(forms.ModelForm):
    class Meta:
        model = models.Project
        fields = ["client", "start_date", "end_date", "name", "cvss_required", "pentest_method", "description"]
        widgets = {
            'start_date': DateInput(),
            'end_date': DateInput(),
            'description': CodeMirrorWidget()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = layout.Layout(
            layout.Row(
                layout.Div(bootstrap5.FloatingField("client"), css_class="col-sm-12"),
            ),
            layout.Row(
                layout.Div(bootstrap5.FloatingField("name"), css_class="col-sm-12")
            ),
            layout.Row(
                layout.Div(bootstrap5.FloatingField("pentest_method"), css_class="col-sm-12")
            ),
            layout.Row(
                layout.Div(bootstrap5.FloatingField("start_date"), css_class="col-sm-12 col-md-6"),
                layout.Div(bootstrap5.FloatingField("end_date"), css_class="col-sm-12 col-md-6")
            ),
            layout.Row(
                layout.Div(bootstrap5.Field("description"), css_class="col-sm-12")
            ),
            layout.Row(
                layout.Div(bootstrap5.Field("cvss_required"), css_class="col-sm-12 col-md-6"),
            ),
            layout.Row(
                FormActions(layout.Submit("submit", "Submit", css_class="btn btn-primary w-100"),
                            wrapper_class="col-sm-12 col-md-6")
            )
        )


class ClientForm(forms.ModelForm):

    class Meta:
        model = models.Client
        fields = ["name", "street", "city", "country", "zip", "homepage", "logo"]
        widgets = {
            "logo": FileDropWidget()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = layout.Layout(
            layout.Row(
                layout.Div(bootstrap5.FloatingField("name"), css_class="col-sm-12 col-md-12"),
            ),
            layout.Row(
                layout.Div(bootstrap5.FloatingField("street"), css_class="col-sm-12 col-md-6"),
                layout.Div(bootstrap5.FloatingField("city"), css_class="col-sm-12 col-md-6")
            ),
            layout.Row(
                layout.Div(bootstrap5.FloatingField("country"), css_class="col-sm-12 col-md-6"),
                layout.Div(bootstrap5.FloatingField("zip"), css_class="col-sm-12 col-md-6")
            ),
            layout.Row(
                layout.Div(bootstrap5.FloatingField("homepage"), css_class="col-sm-12")
            ),
            layout.Row(
                layout.Div(bootstrap5.Field("logo", wrapper_class="col-sm-12"))
            ),
            layout.Row(
                FormActions(layout.Submit("submit", "Submit", css_class="btn btn-primary w-100"),
                            wrapper_class="col-sm-12 col-md-6")
            )
        )


class ContactForm(forms.ModelForm):
    invite_user = forms.BooleanField(required=False)
    position = forms.CharField()
    phone = PhoneNumberField(required=False)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "position", "phone"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = layout.Layout(
            layout.Row(
                layout.Div(bootstrap5.FloatingField("first_name"), css_class="col-sm-12 col-md-12"),
            ),
            layout.Row(
                layout.Div(bootstrap5.FloatingField("last_name"), css_class="col-sm-12 col-md-12"),
            ),
            layout.Row(
                layout.Div(bootstrap5.FloatingField("email"), css_class="col-sm-12 col-md-12"),
            ),
            layout.Row(
                layout.Div(bootstrap5.FloatingField("position"), css_class="col-sm-12 col-md-6"),
                layout.Div(bootstrap5.FloatingField("phone"), css_class="col-sm-12 col-md-6")
            ),
            layout.Row(
                layout.Div(bootstrap5.Field("invite_user"), css_class="col-sm-12 col-md-6")
            ),
            layout.Row(
                FormActions(layout.Submit("submit", "Submit", css_class="btn btn-primary w-100"),
                            wrapper_class="col-sm-12 col-md-6")
            )
        )


class ContributorForm(forms.ModelForm):
    username = forms.CharField()

    class Meta:
        model = models.ProjectContributor
        fields = ["username", "role"]

    def __init__(self, project=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        if project:
            self.helper.form_action = reverse_lazy("projects:contributor-create", kwargs={"pk": project.pk})
        self.helper.layout = layout.Layout(
            layout.Row(
                layout.Div(bootstrap5.FloatingField("username"), css_class="col-sm-12"),
            ),
            layout.Row(
                layout.Div(bootstrap5.FloatingField("role"), css_class="col-sm-12"),
            ),
            layout.Row(
                FormActions(layout.Submit("submit", "Submit", css_class="btn btn-primary w-100"),
                            wrapper_class="col-sm-12 col-md-6")
            )
        )


class ProjectAPITokenForm(forms.ModelForm):
    class Meta:
        model = models.ProjectAPIToken
        fields = ["name", "date_valid"]
        widgets = {'date_valid': DateInput()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_action = "projects:token-create"
        self.helper.layout = layout.Layout(
            layout.Row(
                layout.Div(bootstrap5.FloatingField("name"), css_class="col-sm-12")
            ),
            layout.Row(
                layout.Div(bootstrap5.FloatingField("date_valid"), css_class="col-sm-12")
            ),
            layout.Row(
                FormActions(layout.Submit("submit", "Submit", css_class="btn btn-primary w-100"),
                            wrapper_class="col-sm-12 col-md-6")
            )
        )


class ProjectFileForm(forms.ModelForm):
    class Meta:
        model = models.ProjectFile
        fields = ["name", "file"]
        widgets = {
            'file': FileDropWidget()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = layout.Layout(
            layout.Row(
                layout.Div(bootstrap5.FloatingField("name"), css_class="col-sm-12"), css_class="g-2"
            ),
            layout.Row(
                layout.Div(bootstrap5.Field("file", wrapper_class="col-sm-12"))
            ),
            layout.Row(
                FormActions(layout.Submit("submit", "Submit", css_class="btn btn-primary w-100"),
                            wrapper_class="col-sm-12 col-md-6")
            )
        )

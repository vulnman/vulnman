from django.urls import reverse_lazy
from django import forms
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from crispy_forms.helper import FormHelper
from crispy_forms import layout
from crispy_forms.bootstrap import FormActions
from crispy_bootstrap5 import bootstrap5
from vulnman.core.forms import CodeMirrorWidget
from apps.account import models


class ChangePasswordForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_action = reverse_lazy("account:change-password")
        self.helper.layout = layout.Layout(
            layout.Row(
                layout.Div(
                    bootstrap5.FloatingField("old_password"),
                    css_class="col-sm-12"),
            ),
            layout.Row(
                layout.Div(
                    bootstrap5.FloatingField("new_password1"),
                    css_class="col-sm-12"),
                layout.Div(
                    bootstrap5.FloatingField("new_password2"),
                    css_class="col-sm-12")
            ),
            layout.Row(
                FormActions(
                    layout.Submit('submit', 'Submit',
                                  css_class="btn-primary w-100"),
                    wrapper_class="col-sm-12 col-md-6"
                )
            )
        )


class UpdatePentesterProfileForm(forms.ModelForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = models.PentesterProfile
        fields = [
            "is_public", "public_real_name", "public_email_address", "first_name", "last_name",
            "bio",
        ]
        widgets = {
            "bio": CodeMirrorWidget()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = layout.Layout(
            layout.Row(
              layout.Div(
                  bootstrap5.FloatingField("first_name"), css_class="col-sm-12"
              ),
            ),
            layout.Row(
                layout.Div(
                    bootstrap5.FloatingField("last_name"), css_class="col-sm-12"
                )
            ),
            layout.Row(
                layout.Div(
                    bootstrap5.Field("bio"), css_class="col-sm-12"
                )
            ),
            layout.Row(
                layout.Div(
                    bootstrap5.Field("is_public"),
                    css_class="col-sm-12 col-md-4"),
                layout.Div(
                    bootstrap5.Field("public_real_name"),
                    css_class="col-sm-12 col-md-4"),
                layout.Div(
                    bootstrap5.Field("public_email_address"),
                    css_class="col-sm-12 col-md-4")
            ),
            layout.Row(
                FormActions(
                    layout.Submit('submit', 'Submit',
                                  css_class="btn-primary w-100"),
                    wrapper_class="col-sm-12 col-md-6"
                )
            )
        )


class PasswordSetForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = layout.Layout(
            layout.Row(
                layout.Div(
                    bootstrap5.FloatingField("new_password1")
                )
            ),
            layout.Row(
                layout.Div(
                    bootstrap5.FloatingField("new_password2")
                )
            ),
            layout.Row(
                FormActions(
                    layout.Submit('submit', 'Activate',
                                  css_class="btn-primary justify-content-center w-100"),
                    wrapper_class="col-sm-12 col-md-6"
                )
            )
        )

    def save(self, *args, **kwargs):
        user = super().save(*args, **kwargs)
        user.is_active = True
        user.save()
        return user

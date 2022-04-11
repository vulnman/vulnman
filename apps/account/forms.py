from django.urls import reverse_lazy
from django.contrib.auth.forms import PasswordChangeForm
from crispy_forms.helper import FormHelper
from crispy_forms import layout
from crispy_forms.bootstrap import FormActions
from crispy_bootstrap5 import bootstrap5


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

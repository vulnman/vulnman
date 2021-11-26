from django import forms
from extra_views import InlineFormSetFactory
from crispy_forms.helper import FormHelper


class DateInput(forms.DateInput):
    input_type = 'date'


class NamedInlineFormSetFactory(InlineFormSetFactory):
    factory_kwargs = {'extra': 1, 'can_delete': True, 'max_num': 4}
    formset_name = "Named Formset"

    def get_formset_name(self):
        # TODO: make model verbose_plural_name the default here
        return self.formset_name


class CrispyModelForm(forms.ModelForm):
    # TODO: unused
    crispy_form_action = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_action = self.get_crispy_form_action()
        self.helper.form_tag = False
        self.helper.use_custom_control = True

    def get_crispy_form_action(self):
        return self.crispy_form_action

    def style_crispy_form(self):
        pass

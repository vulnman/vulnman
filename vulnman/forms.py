from django import forms
from extra_views import InlineFormSetFactory


class DateInput(forms.DateInput):
    input_type = 'date'


class NamedInlineFormSetFactory(InlineFormSetFactory):
    factory_kwargs = {'extra': 1, 'can_delete': True, 'max_num': 4}
    formset_name = "Named Formset"

    def get_formset_name(self):
        # TODO: make model verbose_plural_name the default here
        return self.formset_name

from django import forms
from django.conf import settings


def get_tools_choices():
	choices = []
	for tool in settings.EXTERNAL_TOOLS.keys():
		choices.append((tool, tool))
	return choices


class ToolReportImportForm(forms.Form):
	tool = forms.ChoiceField(choices=get_tools_choices())
	file = forms.FileField()

from django.conf import settings
from django.urls import reverse_lazy
from django.utils.module_loading import import_string
from vulnman.views import generic
from apps.external_tools import forms


class ToolImportReport(generic.ProjectFormView):
    form_class = forms.ToolReportImportForm
    template_name = "external_tools/tool_import_report.html"
    valid_report_content_types = ["application/json"]

    def form_valid(self, form):
        tool = form.cleaned_data['tool']
        tool_module = import_string(settings.EXTERNAL_TOOLS[tool])
        if "text/" in form.cleaned_data['file'].content_type:
            content = form.cleaned_data['file'].read().decode()
            tool_instance = tool_module()
            tool_instance.parse(content, self.get_project(), self.request.user)
        elif form.cleaned_data["file"].content_type in self.valid_report_content_types:
            content = form.cleaned_data['file'].read().decode()
            tool_instance = tool_module()
            tool_instance.parse(content, self.get_project(), self.request.user)
        else:
            print("TODO: handle invalid content type: %s" % form.cleaned_data['file'].content_type)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('projects:project-detail', kwargs={'pk': self.get_project().pk})

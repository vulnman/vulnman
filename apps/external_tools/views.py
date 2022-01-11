from django.conf import settings
from django.urls import reverse_lazy
from vulnman.views import generic
from apps.external_tools import forms
from apps.external_tools import tasks


class ToolImportReport(generic.ProjectFormView):
    form_class = forms.ToolReportImportForm
    template_name = "external_tools/tool_import_report.html"
    valid_report_content_types = ["application/json"]

    def form_valid(self, form):
        plugin_name = form.cleaned_data['tool']
        if "text/" in form.cleaned_data['file'].content_type:
            content = form.cleaned_data['file'].read().decode()
            task_id = tasks.do_import_report.delay(plugin_name, content, self.get_project().pk, self.request.user.pk)
        elif form.cleaned_data["file"].content_type in self.valid_report_content_types:
            content = form.cleaned_data['file'].read().decode()
            task_id = tasks.do_import_report.delay(plugin_name, content, self.get_project().pk, self.request.user.pk)
        else:
            print("TODO: handle invalid content type: %s" % form.cleaned_data['file'].content_type)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('projects:project-detail', kwargs={'pk': self.get_project().pk})

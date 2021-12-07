from django.urls import reverse_lazy
from vulnman.views import generic
from apps.social import models
from apps.social import forms


class EmployeeList(generic.ProjectListView):
    model = models.Employee
    template_name = "social/employee_list.html"
    context_object_name = "employees"
    allowed_project_roles = ["pentester", "read-only"]


class EmployeeDetail(generic.ProjectDetailView):
    model = models.Employee
    template_name = "social/employee_detail.html"
    context_object_name = "employee"
    allowed_project_roles = ["read-only", "pentester"]


class EmployeeCreate(generic.ProjectCreateView):
    template_name = "social/employee_create.html"
    form_class = forms.EmployeeForm
    model = models.Employee
    allowed_project_roles = ["pentester"]


class CredentialList(generic.ProjectListView):
    model = models.Credential
    template_name = "social/credential_list.html"
    context_object_name = "credentials"
    allowed_project_roles = ["pentester", "read-only"]


class CredentialCreate(generic.ProjectCreateView):
    template_name = "social/credential_create.html"
    allowed_project_roles = ["pentester"]
    form_class = forms.CredentialForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['project'] = self.get_project()
        return kwargs


class CredentialUpdate(generic.ProjectUpdateView):
    template_name = "social/credential_create.html"
    allowed_project_roles = ["pentester"]
    form_class = forms.CredentialForm
    model = models.Credential
    success_url = reverse_lazy("projects:social:credential-list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['project'] = self.get_project()
        return kwargs

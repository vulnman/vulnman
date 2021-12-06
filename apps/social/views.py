from vulnman.views import generic
from apps.social import models


class EmployeeList(generic.ProjectListView):
    model = models.Employee
    template_name = "social/employee_list.html"
    context_object_name = "employees"


class EmployeeDetail(generic.ProjectDetailView):
    model = models.Employee
    template_name = "social/employee_detail.html"
    context_object_name = "employee"

from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.conf import settings
from django.utils import timezone
from django.db.models import Count
from guardian.shortcuts import get_objects_for_user, assign_perm
from apps.projects import models
from apps.projects import forms
from apps.findings.models import get_severity_by_name
from vulnman.views import generic
from vulnman.mixins.permission import NonObjectPermissionRequiredMixin


class ProjectList(generic.VulnmanAuthListView):
    template_name = "projects/project_list.html"
    context_object_name = "projects"

    def get_queryset(self):
        qs = get_objects_for_user(self.request.user, "projects.view_project", models.Project, use_groups=False, accept_global_perms=False)
        if not self.request.GET.get('archived'):
            qs = qs.filter(is_archived=False)
        else:
            qs = qs.filter(is_archived=True)
        return qs

    def get(self, request, *args, **kwargs):
        if self.request.session.get('project_pk'):
            del self.request.session['project_pk']
        return super().get(request, *args, **kwargs)


class ProjectCreate(NonObjectPermissionRequiredMixin, generic.VulnmanAuthCreateWithInlinesView):
    template_name = "projects/project_create.html"
    form_class = forms.ProjectForm
    model = models.Project
    success_url = reverse_lazy("projects:project-list")
    extra_context = {"TEMPLATE_HIDE_BREADCRUMBS": True}
    permission_required = "projects.add_project"


class ProjectDetail(generic.VulnmanAuthDetailView):
    template_name = "projects/project_detail.html"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        if self.object:
            self.request.session['project_pk'] = str(self.get_object().pk)
        return self.render_to_response(context)

    def get_queryset(self):
        return get_objects_for_user(self.request.user, "projects.view_project",
                                    models.Project.objects.filter(pk=self.kwargs.get('pk')), use_groups=False, accept_global_perms=False)


class ProjectUpdate(NonObjectPermissionRequiredMixin, generic.VulnmanAuthUpdateWithInlinesView):
    template_name = "projects/project_create.html"
    form_class = forms.ProjectForm
    model = models.Project
    permission_required = ["projects.change_project"]

    def get_success_url(self):
        return reverse_lazy('projects:project-detail', kwargs={'pk': self.kwargs.get('pk')})

    def get_queryset(self):
        return get_objects_for_user(self.request.user, "change_project",
                                    models.Project.objects.filter(pk=self.kwargs.get('pk')))

    def form_valid(self, form):
        instance = form.save()
        for pentester in form.cleaned_data.get('pentesters'):
            assign_perm("projects.pentest_project", pentester, instance)
            assign_perm("projects.view_project", pentester, instance)
        return super().form_valid(form)

    def get_initial(self):
        from guardian.shortcuts import get_users_with_perms
        initial = super().get_initial()
        initial["pentesters"] = get_users_with_perms(self.get_object(), with_group_users=False)
        return initial


class ProjectUpdateClose(generic.ProjectRedirectView):
    http_method_names = ["post"]
    url = reverse_lazy("projects:project-list")

    def post(self, request, *args, **kwargs):
        obj = self.get_project()
        obj.is_archived = True
        obj.save()
        obj.archive_project()
        return super().post(request, *args, **kwargs)


class ClientList(NonObjectPermissionRequiredMixin, generic.VulnmanAuthListView):
    template_name = "projects/client_list.html"
    context_object_name = "clients"
    model = models.Client
    permission_required = ["projects.view_client"]


class ClientDetail(NonObjectPermissionRequiredMixin, generic.VulnmanAuthDetailView):
    template_name = "projects/client_detail.html"
    context_object_name = "client"
    model = models.Client
    permission_required = ["projects.view_client"]


class ClientCreate(NonObjectPermissionRequiredMixin, generic.VulnmanAuthCreateWithInlinesView):
    template_name = "projects/client_create.html"
    model = models.Client
    permission_required = ["projects.add_client"]
    form_class = forms.ClientForm
    inlines = [forms.ClientContactInline]


class ProjectContributorList(generic.ProjectListView):
    template_name = "projects/contributor_list.html"
    model = models.ProjectContributor
    permission_required = ["projects.view_project"]
    context_object_name = "contributors"

from django.urls import reverse_lazy
from django.db.models import Q
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.conf import settings
from guardian.shortcuts import get_objects_for_user
from guardian.mixins import PermissionRequiredMixin
from apps.projects import models
from apps.projects import forms
from core.tasks.send_mail import send_mail_task
from vulnman.views import generic
from vulnman.core.views import generics
from vulnman.mixins.permission import NonObjectPermissionRequiredMixin, ObjectPermissionRequiredMixin


class ProjectList(generics.VulnmanAuthListView):
    template_name = "projects/project_list.html"
    context_object_name = "projects"

    def get_queryset(self):
        qs = get_objects_for_user(self.request.user, "projects.view_project", models.Project,
                                  use_groups=False, accept_global_perms=False, with_superuser=False)
        if self.request.GET.get('archived'):
            qs = qs.filter(status=models.Project.PENTEST_STATUS_CLOSED)
        else:
            qs = qs.filter(~Q(status=models.Project.PENTEST_STATUS_CLOSED))
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["create_project_form"] = forms.ProjectForm(form_action="projects:project-create")
        if self.request.GET.get('archived'):
            context["show_archived"] = True
        return context

    def get(self, request, *args, **kwargs):
        if self.request.session.get('project_pk'):
            del self.request.session['project_pk']
        return super().get(request, *args, **kwargs)


class ProjectCreate(NonObjectPermissionRequiredMixin, generics.VulnmanCreateView):
    http_method_names = ["post"]
    form_class = forms.ProjectForm
    model = models.Project
    success_url = reverse_lazy("projects:project-list")
    permission_required = "projects.add_project"

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class ProjectDetail(PermissionRequiredMixin, generics.VulnmanAuthDetailView):
    template_name = "projects/project_detail.html"
    raise_exception = True
    return_403 = True
    permission_required = ["projects.view_project"]

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        if self.object:
            self.request.session['project_pk'] = str(self.get_object().pk)
        return self.render_to_response(context)

    def get_queryset(self):
        return get_objects_for_user(self.request.user, "projects.view_project",
                                    models.Project.objects.filter(pk=self.kwargs.get('pk')),
                                    use_groups=False, accept_global_perms=False, with_superuser=False)


class ProjectUpdate(PermissionRequiredMixin, generics.VulnmanAuthUpdateView):
    template_name = "projects/project_create.html"
    form_class = forms.ProjectForm
    model = models.Project
    permission_required = ["projects.change_project"]
    return_403 = True
    raise_exception = True

    def get_success_url(self):
        return reverse_lazy('projects:project-detail', kwargs={'pk': self.kwargs.get('pk')})

    def get_queryset(self):
        return get_objects_for_user(self.request.user, "change_project",
                                    models.Project.objects.filter(pk=self.kwargs.get('pk')))


class ProjectUpdateClose(PermissionRequiredMixin, generic.ProjectRedirectView):
    http_method_names = ["post"]
    url = reverse_lazy("projects:project-list")
    return_403 = True
    raise_exception = True
    permission_required = ["projects.change_project"]

    def get_permission_object(self):
        return self.get_project()

    def post(self, request, *args, **kwargs):
        obj = self.get_project()
        obj.status = models.Project.PENTEST_STATUS_CLOSED
        obj.save()
        obj.archive_project()
        return super().post(request, *args, **kwargs)


class ClientList(ObjectPermissionRequiredMixin, generics.VulnmanAuthListView):
    template_name = "projects/client_list.html"
    context_object_name = "clients"
    model = models.Client
    permission_required = ["projects.view_client"]
    raise_exception = True
    return_403 = True


class ClientDetail(NonObjectPermissionRequiredMixin, generics.VulnmanAuthDetailView):
    template_name = "projects/client_detail.html"
    context_object_name = "client"
    model = models.Client
    permission_required = ["projects.view_client"]


class ClientCreate(NonObjectPermissionRequiredMixin, generics.VulnmanAuthCreateWithInlinesView):
    # TODO: deprecate *inlinesview
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["create_form"] = forms.ContributorForm(project=self.get_project())
        return context


class ProjectContributorCreate(generic.ProjectCreateView):
    http_method_names = ["post"]
    permission_required = ["projects.add_contributor"]
    form_class = forms.ContributorForm

    def get_success_url(self):
        return reverse_lazy("projects:contributor-list", kwargs={"pk": self.get_project().pk})

    def form_valid(self, form):
        user = User.objects.filter(username=form.cleaned_data.get('username'))
        if not user.exists():
            form.add_error("username", "Username not found!")
            return super().form_invalid(form)
        form.instance.user = user.get()
        if settings.EMAIL_BACKEND:
            send_mail_task.delay(
                "vulnman - New Project %s" % self.get_project().name,
                render_to_string("emails/new_project_contributor.html", context={
                    "obj": form.instance, "request": self.request, "project": self.get_project()}),
                form.instance.user.email
            )
        return super().form_valid(form)


class ProjectContributorDelete(generic.ProjectDeleteView):
    http_method_names = ["post"]
    permission_required = ["projects.add_contributor"]
    model = models.ProjectContributor

    def get_success_url(self):
        return reverse_lazy("projects:contributor-list", kwargs={"pk": self.get_project().pk})


class ProjectTokenList(generic.ProjectListView):
    template_name = "projects/token_list.html"
    context_object_name = "tokens"
    permission_required = ["projects.view_project"]

    def get_queryset(self):
        return models.ProjectAPIToken.objects.filter(user=self.request.user, project=self.get_project())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["token_create_form"] = forms.ProjectAPITokenForm()
        return context


class ProjectTokenCreate(generic.ProjectCreateView):
    http_method_names = ["post"]
    form_class = forms.ProjectAPITokenForm
    success_url = reverse_lazy("projects:token-list")
    permission_required = ["projects.change_project"]

    def get_queryset(self):
        return models.ProjectAPIToken.objects.filter(project=self.get_project(), user=self.request.user)

    def form_valid(self, form):
        form.instance.project = self.get_project()
        form.instance.user = self.request.user
        return super().form_valid(form)


class ProjectTokenDelete(generic.ProjectDeleteView):
    http_method_names = ["post"]
    success_url = reverse_lazy("projects:token-list")

    def get_queryset(self):
        return models.ProjectAPIToken.objects.filter(
            project=self.get_project(), user=self.request.user)

from django.contrib.sites.shortcuts import get_current_site
from django.utils import timezone
from django.urls import reverse_lazy
from django.http import Http404, HttpResponse
from django.conf import settings
from django.utils.encoding import force_bytes
import django_filters.views
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django_q.tasks import async_task
from guardian.mixins import PermissionRequiredMixin
from apps.projects import models
from apps.projects import forms
from apps.projects import filters
from apps.account.models import User
from vulnman.core.views import generics
from vulnman.core.breadcrumbs import Breadcrumb
from vulnman.core.utils import send_mail, get_unique_username_from_email
from vulnman.core.mixins import VulnmanPermissionRequiredMixin, ObjectPermissionRequiredMixin


class ProjectList(django_filters.views.FilterMixin, generics.VulnmanAuthListView):
    template_name = "projects/project_list.html"
    context_object_name = "projects"
    filterset_class = filters.ProjectFilter

    def get_queryset(self):
        qs = models.Project.objects.for_user(self.request.user)
        if not self.request.GET.get("status"):
            qs = qs.filter(status=models.Project.PENTEST_STATUS_OPEN)
        filterset = self.filterset_class(self.request.GET, queryset=qs)
        return filterset.qs

    def get_context_data(self, **kwargs):
        if self.request.GET and not self.request.session.get("project_filters"):
            self.request.session["project_filters"] = dict(self.request.GET)
        if not self.request.GET:
            self.request.session["project_filters"] = {}
        for key, value in self.request.GET.items():
            self.request.session["project_filters"][key] = value
        qs = models.Project.objects.for_user(self.request.user)
        qs_filters = self.request.GET.copy()
        if qs_filters.get("status"):
            del qs_filters["status"]
        filterset = self.filterset_class(qs_filters, queryset=qs)
        qs = filterset.qs
        kwargs["open_status_count"] = qs.filter(
            status=models.Project.PENTEST_STATUS_OPEN).count()
        kwargs["closed_status_count"] = qs.filter(
            status=models.Project.PENTEST_STATUS_CLOSED).count()
        return super().get_context_data(**kwargs)

    def get(self, request, *args, **kwargs):
        if self.request.session.get('project_pk'):
            del self.request.session['project_pk']
        return super().get(request, *args, **kwargs)


class ProjectCreate(VulnmanPermissionRequiredMixin, generics.VulnmanCreateView):
    form_class = forms.ProjectForm
    model = models.Project
    success_url = reverse_lazy("projects:project-list")
    permission_required = "projects.add_project"
    template_name = "projects/project_create.html"

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class ProjectDetail(VulnmanPermissionRequiredMixin, generics.VulnmanAuthDetailView):
    template_name = "projects/project_detail.html"
    permission_required = ["projects.view_project"]

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        if self.object:
            self.request.session['project_pk'] = str(self.get_object().pk)
        return self.render_to_response(context)

    def get_queryset(self):
        qs = models.Project.objects.for_user(self.request.user)
        return qs.filter(pk=self.kwargs.get("pk"))


class ProjectUpdate(VulnmanPermissionRequiredMixin, generics.VulnmanAuthUpdateView):
    template_name = "projects/project_create.html"
    form_class = forms.ProjectForm
    permission_required = ["projects.change_project"]

    def get_success_url(self):
        return reverse_lazy('projects:project-detail', kwargs={'pk': self.kwargs.get('pk')})

    def get_queryset(self):
        qs = models.Project.objects.for_user(self.request.user, perms="projects.change_project")
        return qs.filter(pk=self.kwargs.get("pk"))


class ProjectUpdateClose(PermissionRequiredMixin, generics.ProjectRedirectView):
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
    template_name = "projects/clients/list.html"
    context_object_name = "clients"
    model = models.Client
    permission_required = ["projects.view_client"]
    raise_exception = True
    return_403 = True


class ClientDetail(VulnmanPermissionRequiredMixin, generics.VulnmanAuthDetailView):
    template_name = "projects/client_detail.html"
    context_object_name = "client"
    model = models.Client
    permission_required = ["projects.view_client"]


class ClientCreate(VulnmanPermissionRequiredMixin, generics.VulnmanAuthCreateView):
    template_name = "projects/clients/create_or_update.html"
    model = models.Client
    permission_required = ["projects.add_client"]
    form_class = forms.ClientForm


class ClientUpdate(VulnmanPermissionRequiredMixin, generics.VulnmanAuthUpdateView):
    template_name = "projects/clients/create_or_update.html"
    model = models.Client
    permission_required = ["projects.change_client"]
    form_class = forms.ClientForm


class ClientDelete(VulnmanPermissionRequiredMixin, generics.VulnmanAuthDeleteView):
    model = models.Client
    permission_required = ["projects.delete_client"]
    http_method_names = ["post"]
    success_url = reverse_lazy("clients:client-list")


class ClientContacts(VulnmanPermissionRequiredMixin, generics.VulnmanAuthDetailView):
    # TODO: write tests
    model = models.Client
    permission_required = ["projects.view_client"]
    template_name = "projects/clients/contacts_list.html"

    def get_context_data(self, **kwargs):
        kwargs["contacts"] = User.objects.filter(user_role=User.USER_ROLE_CUSTOMER,
                                                 customer_profile__customer=self.get_object())
        return super().get_context_data(**kwargs)


class ContactCreate(VulnmanPermissionRequiredMixin, generics.VulnmanAuthCreateView):
    # TODO: write tests
    model = User
    permission_required = ["projects.change_client"]
    form_class = forms.ContactForm
    template_name = "projects/clients/contact_create_or_update.html"
    invite_mail_subject = "vulnman / Invitation to vulnman"
    invite_mail_template_name = "emails/invite_customer.html"
    invite_mail_from_mail = settings.DEFAULT_FROM_EMAIL

    def get_success_url(self):
        return reverse_lazy("clients:client-contacts", kwargs={"pk": self.kwargs.get("pk")})

    def get_client(self):
        try:
            obj = models.Client.objects.get(pk=self.kwargs.get("pk"))
        except models.Client.DoesNotExist:
            return Http404()
        return obj

    def get_context_data(self, **kwargs):
        kwargs["client"] = self.get_client()
        return super().get_context_data(**kwargs)

    def send_invite_mail(self, user):
        current_site = get_current_site(self.request)
        site_name = current_site.name
        domain = current_site.domain
        context = {"email": user.email, "domain": domain, "site_name": site_name,
                   "uid": urlsafe_base64_encode(force_bytes(user.pk)), "user": user,
                   "token": PasswordResetTokenGenerator().make_token(user),
                   "protocol": self.request.scheme}
        async_task(send_mail, self.invite_mail_subject, self.invite_mail_template_name, context,
                   self.invite_mail_from_mail, user.email)

    def form_valid(self, form):
        form.instance.username = get_unique_username_from_email(form.cleaned_data["email"], prefix="cus")
        form.instance.user_role = User.USER_ROLE_CUSTOMER
        user = form.save()
        user.customer_profile.position = form.cleaned_data["position"]
        user.customer_profile.phone = form.cleaned_data.get("phone")
        user.customer_profile.customer = self.get_client()
        user.customer_profile.save()
        if form.cleaned_data["invite_user"]:
            self.send_invite_mail(form.instance)
        return super().form_valid(form)


class ContactDelete(VulnmanPermissionRequiredMixin, generics.VulnmanAuthDeleteView):
    # TODO: write tests
    # FIXME: new user model
    model = models.ClientContact
    permission_required = ["projects.change_client"]
    http_method_names = ["post"]

    def get_success_url(self):
        return reverse_lazy("clients:client-contacts", kwargs={"pk": self.get_object().client.pk})


class ProjectContributorList(generics.ProjectListView):
    template_name = "projects/contributor_list.html"
    model = models.ProjectContributor
    permission_required = ["projects.view_project"]
    context_object_name = "contributors"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["create_form"] = forms.ContributorForm(project=self.get_project())
        return context


class ProjectContributorCreate(generics.ProjectCreateView):
    template_name = "core/pages/create.html"
    permission_required = ["projects.add_contributor"]
    form_class = forms.ContributorForm
    page_title = "Add Project Contributor"
    success_url = reverse_lazy("projects:contributor-list")
    success_message = "Invite Mail was Sent!"

    def get_breadcrumbs(self):
        return [
            Breadcrumb(reverse_lazy("projects:contributor-list"), "Contributors")
        ]

    def is_customer_for_current_project(self, user):
        if self.get_project().client != user.customer_profile.customer:
            return False
        return True

    def is_send_mail_allowed(self, form):
        user_roles = [User.USER_ROLE_CUSTOMER, User.USER_ROLE_PENTESTER]
        user = User.objects.filter(email=form.cleaned_data["invite_email"], user_role__in=user_roles)
        if not user.exists():
            return False
        contrib_user = user.get()
        form.instance.user = contrib_user
        if contrib_user.user_role == User.USER_ROLE_CUSTOMER:
            if not self.is_customer_for_current_project(contrib_user):
                form.instance.user = None
                return False
        # check if we are already part of the project
        if models.ProjectContributor.objects.filter(user=contrib_user, project=self.get_project()).exists():
            return False
        return True

    def send_invite_mail(self, user):
        subject = "vulnman / New Project Invite"
        context = {"obj": user, "project": self.get_project(), "login_url": self.request.build_absolute_uri(
            reverse_lazy("account:login"))}
        async_task(send_mail, subject, "emails/new_project_contributor.html", context, settings.DEFAULT_FROM_EMAIL,
                   user.email)

    def form_valid(self, form):
        if self.is_send_mail_allowed(form):
            self.send_invite_mail(form.instance.user)
        return super().form_valid(form)


class ProjectContributorDelete(generics.ProjectDeleteView):
    http_method_names = ["post"]
    permission_required = ["projects.add_contributor"]

    def get_queryset(self):
        return models.ProjectContributor.objects.filter(pk=self.kwargs.get("pk"), project=self.get_project())

    def get_success_url(self):
        return reverse_lazy("projects:contributor-list")


class ProjectContributorConfirmList(generics.VulnmanAuthListView):
    # TODO: write tests
    template_name = "projects/contributor_confirm_list.html"

    def get_queryset(self):
        return models.ProjectContributor.objects.filter(user=self.request.user, confirmed=False)


class ProjectContributorConfirmDelete(generics.VulnmanAuthDeleteView):
    # TODO: write tests
    http_method_names = ["post"]
    success_url = reverse_lazy("projects:contributor-confirm-list")

    def get_queryset(self):
        return models.ProjectContributor.objects.filter(user=self.request.user, confirmed=False)


class ProjectContributorConfirmUpdate(generics.VulnmanAuthUpdateView):
    # TODO: write tests
    http_method_names = ["post"]
    success_url = reverse_lazy("projects:contributor-confirm-list")
    form_class = forms.ContributorConfirmForm

    def get_queryset(self):
        return models.ProjectContributor.objects.filter(user=self.request.user, confirmed=False)

    def form_valid(self, form):
        form.instance.confirmed = True
        form.instance.date_confirmed = timezone.now()
        return super().form_valid(form)


class ProjectTokenList(generics.ProjectListView):
    template_name = "projects/token_list.html"
    context_object_name = "tokens"
    permission_required = ["projects.view_project"]

    def get_queryset(self):
        return models.ProjectAPIToken.objects.filter(user=self.request.user, project=self.get_project())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["token_create_form"] = forms.ProjectAPITokenForm()
        return context


class ProjectTokenCreate(generics.ProjectCreateView):
    template_name = "core/pages/create.html"
    form_class = forms.ProjectAPITokenForm
    success_url = reverse_lazy("projects:token-list")
    permission_required = ["projects.change_project"]
    page_title = "Create API-Token"
    breadcrumbs = [
        Breadcrumb(reverse_lazy("projects:token-list"), "API-Tokens"),
    ]

    def get_queryset(self):
        return models.ProjectAPIToken.objects.filter(project=self.get_project(), user=self.request.user)

    def form_valid(self, form):
        form.instance.project = self.get_project()
        form.instance.user = self.request.user
        return super().form_valid(form)


class ProjectTokenDelete(generics.ProjectDeleteView):
    http_method_names = ["post"]
    success_url = reverse_lazy("projects:token-list")

    def get_queryset(self):
        return models.ProjectAPIToken.objects.filter(
            project=self.get_project(), user=self.request.user)


class ProjectFileList(generics.ProjectListView):
    template_name = "projects/files/list.html"

    def get_queryset(self):
        return models.ProjectFile.objects.filter(project=self.get_project())


class ProjectFileCreate(generics.ProjectCreateView):
    template_name = "core/pages/create.html"
    form_class = forms.ProjectFileForm
    success_url = reverse_lazy("projects:file-list")
    page_title = "Create New File"
    breadcrumbs = [
        Breadcrumb(reverse_lazy("projects:file-list"), "Files")
    ]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ProjectFileDetail(generics.ProjectDetailView):
    model = models.ProjectFile

    def render_to_response(self, context, **response_kwargs):
        obj = self.get_object()
        response = HttpResponse(self.get_object().file)
        response['Content-Disposition'] = 'attachment; filename="{filename}"'.format(filename=obj.filename)
        return response


class ProjectFileUpdate(generics.ProjectUpdateView):
    # TODO: write tests
    template_name = "core/pages/update.html"
    form_class = forms.ProjectFileForm
    page_title = "Update File"

    def get_breadcrumbs(self):
        return [
            Breadcrumb(reverse_lazy("projects:file-list"), "Files"),
        ]

    def get_queryset(self):
        return models.ProjectFile.objects.filter(project=self.get_project())


class ProjectFileDelete(generics.ProjectDeleteView):
    http_method_names = ["post"]
    success_url = reverse_lazy("projects:file-list")

    def get_queryset(self):
        return models.ProjectFile.objects.filter(project=self.get_project())

import django_filters.views
from django.urls import reverse_lazy
from django.db.models import Count
from django.http import HttpResponse, Http404
from guardian.shortcuts import get_objects_for_user, get_users_with_perms, get_user_perms, remove_perm
from vulnman.core.views import generics
from vulnman.mixins.permission import VulnmanPermissionRequiredMixin, ObjectPermissionRequiredMixin
from apps.findings.models import Template
from apps.account.models import User
from apps.responsible_disc import models
from apps.responsible_disc import forms
from apps.responsible_disc import tasks
from apps.responsible_disc import filters


class VulnerabilityList(django_filters.views.FilterMixin, generics.VulnmanAuthListView):
    template_name = "responsible_disc/vulnerability_list.html"
    context_object_name = "vulnerabilities"
    filterset_class = filters.VulnerabilityFilter
    model = models.Vulnerability

    def get_queryset(self, skip_status_filter=False):
        qs = get_objects_for_user(self.request.user, "responsible_disc.view_vulnerability", models.Vulnerability,
                                  use_groups=False, with_superuser=False, accept_global_perms=False)
        if not skip_status_filter:
            if not self.request.GET.get("status"):
                qs = qs.filter(status=models.Vulnerability.STATUS_OPEN)
        filterset = self.filterset_class(self.request.GET, queryset=qs)
        return filterset.qs

    def get_context_data(self, **kwargs):
        if not self.request.session.get("rd_vulns_filters"):
            self.request.session["rd_vulns_filters"] = dict(self.request.GET)
        for key, value in self.request.GET.items():
            self.request.session["rd_vulns_filters"][key] = value
        qs = get_objects_for_user(self.request.user, "responsible_disc.view_vulnerability", models.Vulnerability,
                                  use_groups=False, with_superuser=False, accept_global_perms=False)
        qs_filters = self.request.GET.copy()
        if qs_filters.get("status"):
            del qs_filters["status"]
        filterset = self.filterset_class(qs_filters, queryset=qs)
        qs = filterset.qs
        kwargs["open_vulns_count"] = qs.filter(
            status=models.Vulnerability.STATUS_OPEN).count()
        kwargs["closed_vulns_count"] = qs.filter(
            status=models.Vulnerability.STATUS_CLOSED).count()
        return super().get_context_data(**kwargs)


class VulnerabilityCreate(VulnmanPermissionRequiredMixin, generics.VulnmanAuthCreateView):
    form_class = forms.VulnerabilityForm
    template_name = "responsible_disc/vulnerability_create.html"
    permission_required = ["responsible_disc.add_vulnerability"]

    def form_valid(self, form):
        if not Template.objects.filter(vulnerability_id=form.cleaned_data["template_id"]).exists():
            form.add_error("template_id", "Template does not exist!")
            return super().form_invalid(form)
        form.instance.template = Template.objects.get(vulnerability_id=form.cleaned_data["template_id"])
        if not form.cleaned_data.get('severity'):
            form.instance.severity = form.instance.template.severity
        form.instance.user = self.request.user
        return super().form_valid(form)


class VulnerabilityDetail(ObjectPermissionRequiredMixin, generics.VulnmanAuthDetailView):
    template_name = "responsible_disc/vulnerability_detail.html"
    context_object_name = "vuln"
    permission_required = ["responsible_disc.view_vulnerability"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["text_proof_form"] = forms.TextProofForm()
        context["image_proof_form"] = forms.ImageProofForm()
        return context

    def get_queryset(self):
        return models.Vulnerability.objects.filter(pk=self.kwargs.get("pk"))


class VulnerabilityTimeline(ObjectPermissionRequiredMixin, generics.VulnmanAuthDetailView):
    template_name = "responsible_disc/vulnerability_timeline.html"
    context_object_name = "vuln"
    permission_required = ["responsible_disc.view_vulnerability"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["log_form"] = forms.VulnerabilityLogForm()
        return context

    def get_queryset(self):
        return models.Vulnerability.objects.filter(pk=self.kwargs.get("pk"))


class VulnerabilityLogCreate(generics.VulnmanAuthCreateView):
    http_method_names = ["post"]
    form_class = forms.VulnerabilityLogForm

    def get_queryset(self):
        return models.VulnerabilityLog.objects.filter(user=self.request.user)

    def form_valid(self, form):
        vulnerability = models.Vulnerability.objects.filter(pk=self.kwargs.get('pk'), user=self.request.user)
        if not vulnerability.exists():
            form.add_error("action", "Vulnerability does not exist!")
            return super().form_invalid(form)
        form.instance.vulnerability = vulnerability.get()
        if form.cleaned_data["action"] == models.VulnerabilityLog.ACTION_PUBLISHED:
            form.instance.vulnerability.status = models.Vulnerability.STATUS_CLOSED
            form.instance.vulnerability.save()
        self.success_url = form.instance.vulnerability.get_absolute_url()
        return super().form_valid(form)


class TextProofDelete(generics.VulnmanAuthDeleteView):
    model = models.TextProof
    http_method_names = ["post"]

    def get_success_url(self):
        return reverse_lazy('responsible_disc:vulnerability-detail', kwargs={"pk": self.get_object().vulnerability.pk})

    def get_queryset(self):
        return models.TextProof.objects.filter(vulnerability__user=self.request.user)


class ImageProofDelete(generics.VulnmanAuthDeleteView):
    model = models.ImageProof
    http_method_names = ["post"]

    def get_success_url(self):
        return reverse_lazy('responsible_disc:vulnerability-detail', kwargs={"pk": self.get_object().vulnerability.pk})

    def get_queryset(self):
        return models.ImageProof.objects.filter(vulnerability__user=self.request.user)


class VulnerabilityExport(ObjectPermissionRequiredMixin, generics.VulnmanAuthDetailView):
    permission_required = ["responsible_disc.view_vulnerability"]

    def get_queryset(self):
        return models.Vulnerability.objects.filter(pk=self.kwargs.get("pk"))

    def render_to_response(self, context, **response_kwargs):
        result = tasks.export_single_vulnerability(self.get_object())
        response = HttpResponse(result, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="report.pdf"'
        return response


class VulnerabilityNotifyVendor(generics.VulnmanAuthUpdateView):
    form_class = forms.VulnerabilityNotificationForm
    http_method_names = ["post"]

    def get_queryset(self):
        return models.Vulnerability.objects.filter(user=self.request.user)

    def form_valid(self, form):
        if not form.instance.vendor_email:
            form.add_error("empty", "No vendor email set")
            return super().form_invalid(form)
        tasks.notify_vendor.delay(str(form.instance.pk))
        return super().form_valid(form)


class VulnUpdate(ObjectPermissionRequiredMixin, generics.VulnmanAuthUpdateView):
    model = models.Vulnerability
    form_class = forms.VulnerabilityForm
    permission_required = ["responsible_disc.change_vulnerability"]
    template_name = "responsible_disc/vulnerability_create.html"

    def get_queryset(self):
        return models.Vulnerability.objects.filter(pk=self.kwargs.get("pk"))

    def form_valid(self, form):
        if not Template.objects.filter(vulnerability_id=form.cleaned_data["template_id"]).exists():
            form.add_error("template_id", "Template does not exist!")
            return super().form_invalid(form)
        form.instance.template = Template.objects.get(vulnerability_id=form.cleaned_data["template_id"])
        if not form.cleaned_data.get('severity'):
            form.instance.severity = form.instance.template.severity
        return super().form_valid(form)


class VulnDelete(generics.VulnmanAuthDeleteView):
    http_method_names = ["post"]
    success_url = reverse_lazy('responsible_disc:vulnerability-list')

    def get_queryset(self):
        return models.Vulnerability.objects.filter(user=self.request.user)


class VulnerabilityAdvisoryExport(ObjectPermissionRequiredMixin, generics.VulnmanAuthDetailView):
    permission_required = ["responsible_disc.view_vulnerability"]

    def get_queryset(self):
        return models.Vulnerability.objects.filter(pk=self.kwargs.get("pk"))

    def render_to_response(self, context, **response_kwargs):
        result = tasks.export_advisory(self.get_object())
        response = HttpResponse(result, content_type='plain/text')
        response['Content-Disposition'] = 'attachment; filename="advisory.md"'
        return response


class TextProofUpdate(ObjectPermissionRequiredMixin, generics.VulnmanAuthUpdateView):
    template_name = "responsible_disc/proof_update.html"
    form_class = forms.TextProofForm
    permission_required = ["responsible_disc.change_vulnerability"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["vuln"] = self.get_object().vulnerability
        return context

    def get_permission_object(self):
        try:
            obj = self.get_queryset().get().vulnerability
        except models.Vulnerability.DoesNotExist:
            return Http404("No such vulnerability found")
        return obj

    def get_queryset(self):
        return models.TextProof.objects.filter(pk=self.kwargs.get("pk"))

    def get_success_url(self):
        return reverse_lazy("responsible_disc:vulnerability-detail", kwargs={"pk": self.get_object().vulnerability.pk})


class ImageProofUpdate(generics.VulnmanAuthUpdateView):
    template_name = "responsible_disc/proof_update.html"
    form_class = forms.ImageProofForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["vuln"] = self.get_object().vulnerability
        return context

    def get_queryset(self):
        return models.ImageProof.objects.filter(vulnerability__user=self.request.user)

    def get_success_url(self):
        return reverse_lazy("responsible_disc:vulnerability-detail", kwargs={"pk": self.get_object().vulnerability.pk})


class TextProofCreate(ObjectPermissionRequiredMixin, generics.VulnmanAuthCreateView):
    template_name = "responsible_disc/proof_create.html"
    form_class = forms.TextProofForm
    permission_required = ["responsible_disc.change_vulnerability"]

    def get_queryset(self):
        return models.Vulnerability.objects.filter(pk=self.kwargs.get('pk'))

    def get_success_url(self):
        return reverse_lazy("responsible_disc:vulnerability-detail", kwargs={"pk": self.get_object().pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["vuln"] = self.get_object()
        return context

    def form_valid(self, form):
        form.instance.vulnerability = self.get_object()
        return super().form_valid(form)


class ImageProofCreate(ObjectPermissionRequiredMixin, generics.VulnmanAuthCreateView):
    template_name = "responsible_disc/proof_create.html"
    form_class = forms.ImageProofForm
    permission_required = ["responsible_disc.change_vulnerability"]

    def get_queryset(self):
        return models.Vulnerability.objects.filter(pk=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["vuln"] = self.get_object()
        return context

    def get_success_url(self):
        return reverse_lazy("responsible_disc:vulnerability-detail", kwargs={"pk": self.get_object().pk})

    def form_valid(self, form):
        form.instance.vulnerability = self.get_object()
        form.instance.user = self.request.user
        return super().form_valid(form)


class CommentList(ObjectPermissionRequiredMixin, generics.VulnmanAuthListView):
    template_name = "responsible_disc/comment_list.html"
    permission_required = ["responsible_disc.view_vulnerability"]
    context_object_name = "comments"
    paginate_by = 200

    def get_permission_object(self):
        qs = models.Vulnerability.objects.filter(pk=self.kwargs.get('pk'))
        try:
            obj = qs.get()
        except models.Vulnerability.DoesNotExist:
            return Http404("No such vulnerability found!")
        return obj

    def get_queryset(self):
        return models.VulnerabilityComment.objects.filter(vulnerability__pk=self.kwargs.get("pk"))

    def get_context_data(self, **kwargs):
        kwargs["vuln"] = models.Vulnerability.objects.get(pk=self.kwargs.get("pk"))
        kwargs["new_comment_form"] = forms.NewCommentForm(kwargs["vuln"])
        return super().get_context_data(**kwargs)


class CommentCreate(ObjectPermissionRequiredMixin, generics.VulnmanAuthCreateView):
    permission_required = ["responsible_disc.add_comment"]
    http_method_names = ["post"]
    form_class = forms.NewCommentForm

    def get_success_url(self):
        return reverse_lazy("responsible_disc:comment-list", kwargs={"pk": self.kwargs.get("pk")})

    def get_permission_object(self):
        qs = models.Vulnerability.objects.filter(pk=self.kwargs.get('pk'))
        try:
            obj = qs.get()
        except models.Vulnerability.DoesNotExist:
            return Http404("No such vulnerability found!")
        return obj

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["vuln"] = self.get_permission_object()
        return kwargs

    def form_valid(self, form):
        form.instance.vulnerability = self.get_permission_object()
        form.instance.creator = self.request.user
        return super().form_valid(form)


class ManageAccessList(ObjectPermissionRequiredMixin, generics.VulnmanAuthListView):
    template_name = "responsible_disc/vulnerability_manage_access.html"
    context_object_name = "users"
    permission_required = ["responsible_disc.view_vulnerability"]

    def get_queryset(self):
        obj = self.get_permission_object()
        return get_users_with_perms(obj, with_group_users=False, with_superusers=False)

    def get_permission_object(self):
        try:
            obj = models.Vulnerability.objects.get(pk=self.kwargs.get("pk"))
        except models.Vulnerability.DoesNotExist:
            return Http404("No such vulnerability found!")
        return obj

    def get_context_data(self, **kwargs):
        kwargs["vuln"] = self.get_permission_object()
        return super().get_context_data(**kwargs)


class UnshareVulnerabilityFromUser(ObjectPermissionRequiredMixin, generics.VulnmanAuthFormView):
    http_method_names = ["post"]
    permission_required = ["responsible_disc.invite_vendor"]
    form_class = forms.UnshareVulnerability

    def get_success_url(self):
        return self.get_permission_object().get_absolute_url()

    def get_permission_object(self):
        try:
            obj = models.Vulnerability.objects.get(pk=self.kwargs.get('pk'))
        except models.Vulnerability.DoesNotExist:
            return Http404("No such vulnerability found!")
        return obj

    def form_valid(self, form):
        obj = self.get_permission_object()
        try:
            qs = get_users_with_perms(obj)
            user = qs.get(email=form.cleaned_data["email"])
        except User.DoesNotExist:
            form.add_error("email", "User not found!")
            return super().form_invalid(form)
        if user == obj.user:
            form.add_error("email", "Cannot remove creator!")
            return super().form_invalid(form)
        perms = get_user_perms(user, obj)
        for perm in perms:
            remove_perm(perm, user_or_group=user, obj=obj)
        return super().form_valid(form)


from apps.responsible_disc.views.vendor import InviteVendor

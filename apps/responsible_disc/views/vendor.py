import uuid
from django.http import Http404, HttpResponseRedirect
from django.conf import settings
from guardian.shortcuts import assign_perm
from vulnman.core.mixins import ObjectPermissionRequiredMixin
from apps.account.models import User
from apps.account.token import account_activation_token
from apps.responsible_disc import forms
from apps.responsible_disc import models
from django.contrib.auth.views import PasswordResetView


class InviteVendor(ObjectPermissionRequiredMixin, PasswordResetView):
    # TODO: write tests
    template_name = "responsible_disc/vendor/invite_vendor.html"
    permission_required = ["responsible_disc.invite_vendor"]
    form_class = forms.InviteVendorForm
    extra_email_context = {}
    token_generator = account_activation_token
    from_email = settings.RESPONSIBLE_DISCLOSURE_MAIL_FROM
    # html_email_template_name = "responsible_disc/emails/vendor_invite.html"
    email_template_name = "responsible_disc/emails/vendor_invite.html"
    subject_template_name = "responsible_disc/emails/vendor_invite_subject.html"

    def get_success_url(self):
        return models.Vulnerability.objects.get(pk=self.kwargs.get("pk")).get_absolute_url()

    def get_permission_object(self):
        try:
            obj = models.Vulnerability.objects.get(pk=self.kwargs.get("pk"))
        except models.Vulnerability.DoesNotExist:
            return Http404("No such vulnerability found!")
        return obj

    def get_context_data(self, **kwargs):
        kwargs["vuln"] = self.get_permission_object()
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        # FIXME: this view is ugly!
        qs = User.objects.filter(email=form.cleaned_data.get('email'))
        perms = ["responsible_disc.view_vulnerability", "responsible_disc.add_comment"]
        if qs.filter(is_active=True).exists():
            user = qs.get()
            for perm in perms:
                assign_perm(perm, user_or_group=user, obj=self.get_permission_object())
            # TODO: send notification mail to user that a new vulnerability was shared with him
            return HttpResponseRedirect(self.get_success_url())
        if not qs.exists():
            user = User.objects.create(
                username="vendor-%s" % uuid.uuid4(), email=form.cleaned_data["email"], is_vendor=True, is_active=False)
            self.extra_email_context["new_user"] = user
        else:
            user = User.objects.get(email=form.cleaned_data["email"])
            self.extra_email_context["new_user"] = user
        for perm in perms:
            assign_perm(perm, user_or_group=user, obj=self.get_permission_object())
        return super().form_valid(form)

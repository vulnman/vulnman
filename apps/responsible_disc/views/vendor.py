from django.http import Http404, HttpResponseRedirect
from django.conf import settings
from django.contrib.auth.views import PasswordResetView
from django.core.exceptions import ImproperlyConfigured
from guardian.shortcuts import assign_perm
from django_q.tasks import async_task
from vulnman.core.mixins import ObjectPermissionRequiredMixin
from vulnman.core import utils
from apps.account.models import User
from apps.account.token import account_activation_token
from apps.responsible_disc import forms
from apps.responsible_disc import models


class ShareWithMailMixin:
    share_email_template_name = None
    share_email_subject = None
    share_from_email = None
    share_email_context = None
    share_html_email_template_name = None

    def get_share_email_template_name(self):
        if not self.share_email_template_name:
            raise ImproperlyConfigured("Require `self.share_email_template_name`")
        return self.share_email_template_name

    def get_share_email_subject(self):
        if not self.share_email_subject:
            raise ImproperlyConfigured("Require `share_email_subject`")
        return self.share_email_subject

    def get_share_email_context(self):
        if not self.share_email_context:
            raise ImproperlyConfigured("Require `share_email_context`")
        return self.share_email_context

    def get_share_from_email(self):
        if not self.share_from_email:
            raise ImproperlyConfigured("Require `share_from_email`")
        return self.share_from_email

    def get_share_html_email_template_name(self):
        return self.share_html_email_template_name

    def send_shared_notification_mail(self, to_email):
        task_id = async_task(utils.send_mail, self.get_share_email_subject(), self.get_share_email_template_name(),
                             self.get_share_email_context(), self.get_share_from_email(), to_email,
                             html_email_template_name=self.get_share_html_email_template_name())
        return task_id


class InviteVendor(ObjectPermissionRequiredMixin, ShareWithMailMixin, PasswordResetView):
    template_name = "responsible_disc/vendor/invite_vendor.html"
    permission_required = ["responsible_disc.invite_vendor"]
    form_class = forms.InviteVendorForm
    extra_email_context = {}
    from_email = settings.RESPONSIBLE_DISCLOSURE_MAIL_FROM
    email_template_name = "responsible_disc/emails/vendor_invite.html"
    subject_template_name = "responsible_disc/emails/vendor_invite_subject.html"
    share_from_email = settings.RESPONSIBLE_DISCLOSURE_MAIL_FROM
    share_email_template_name = "responsible_disc/emails/new_vulnerability_shared.html"
    share_email_subject = "New Vulnerability Shared on vulnman"

    def get_share_email_context(self):
        context = {"user": self.request.user,
                   "link": self.request.build_absolute_uri(self.get_permission_object().get_absolute_url())}
        return context

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

    def create_new_vendor(self, email):
        user = User.objects.create(username=email, email=email, user_role=User.USER_ROLE_VENDOR, is_active=True)
        return user

    def form_valid(self, form):
        # FIXME: this view is ugly!
        qs = User.objects.filter(email=form.cleaned_data.get('email'))
        perms = ["responsible_disc.view_vulnerability", "responsible_disc.add_comment"]
        if qs.filter(is_active=True).exists():
            user = qs.get()
            for perm in perms:
                assign_perm(perm, user_or_group=user, obj=self.get_permission_object())
            self.send_shared_notification_mail(user.email)
            return HttpResponseRedirect(self.get_success_url())
        if not qs.exists():
            user = self.create_new_vendor(form.cleaned_data["email"])
            self.extra_email_context["new_user"] = user
        else:
            user = User.objects.get(email=form.cleaned_data["email"])
            self.extra_email_context["new_user"] = user
        for perm in perms:
            assign_perm(perm, user_or_group=user, obj=self.get_permission_object())
        return super().form_valid(form)

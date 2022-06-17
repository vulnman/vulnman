import uuid
from django.contrib.auth import views
from django.urls import reverse_lazy
from apps.account import forms
from apps.account import models
from vulnman.core.views.mixins import ThemeMixin, VulnmanContextMixin
from vulnman.mixins.permission import DJPermissionRequiredMixin
from vulnman.core.views import generics


class Login(ThemeMixin, views.LoginView):
    template_name = "account/login.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['TEMPLATE_HIDE_BREADCRUMBS'] = True
        context['hide_navbar'] = True
        return context


class Logout(views.LogoutView):
    pass


class Profile(generics.VulnmanDetailView):
    template_name = "account/profile.html"
    context_object_name = "user"
    slug_field = "username"

    def get_queryset(self):
        return models.User.objects.filter(is_pentester=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["change_password_form"] = forms.ChangePasswordForm(self.request.user)
        return context


class ChangePassword(VulnmanContextMixin, views.PasswordChangeView):
    form_class = forms.ChangePasswordForm
    template_name = "account/change_password.html"

    def get_success_url(self):
        return reverse_lazy('account:user-profile', kwargs={'slug': self.request.user.username})


"""
# Not yet used
class InviteVendor(DJPermissionRequiredMixin, generics.VulnmanAuthCreateView):
    template_name = "account/invite_vendor.html"
    form_class = forms.InviteVendorForm
    success_url = reverse_lazy("responsible_disc:vulnerability-list")
    permission_required = ["account.invite_vendor"]

    def form_valid(self, form):
        form.instance.token = models.InviteCode.generate_token()
        form.instance.user_created = self.request.user
        # generate unique username to not disclose vendor data with vulnerability disclosure
        models.User.objects.create(
            username="vendor-%s" % uuid.uuid4(), email=form.instance.email, is_vendor=True, is_active=False)
        # TODO: send mail to vendor
        return super().form_valid(form)
"""
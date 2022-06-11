from django.contrib.auth import views
from django.urls import reverse_lazy
from apps.account import forms
from vulnman.core.views.mixins import ThemeMixin
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


class Profile(generics.VulnmanAuthTemplateView):
    template_name = "account/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["change_password_form"] = forms.ChangePasswordForm(self.request.user)
        return context


class ChangePassword(ThemeMixin, views.PasswordChangeView):
    form_class = forms.ChangePasswordForm
    http_method_names = ["post"]
    success_url = reverse_lazy("account:profile-edit")

from django.contrib.auth import views
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from apps.account import forms
from vulnman.mixins import ThemeMixin
from vulnman.views import generic


class Login(ThemeMixin, views.LoginView):
    template_name = "account/login.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['TEMPLATE_HIDE_BREADCRUMBS'] = True
        return context


class Logout(views.LogoutView):
    pass


class ProfileEdit(generic.VulnmanAuthUpdateView):
    form_class = forms.ProfileForm
    template_name = "account/profile_edit.html"
    success_url = reverse_lazy('projects:project-list')

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_initial(self):
        initial = super().get_initial()
        initial["email"] = self.request.user.email
        return initial

    def form_valid(self, form):
        if not User.objects.filter(email=form.cleaned_data["email"]).exists():
            self.request.user.email = form.cleaned_data["email"]
            self.request.user.save()
        return super().form_valid(form)


class Profile(generic.VulnmanAuthTemplateView):
    template_name = "account/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["change_password_form"] = forms.ChangePasswordForm(self.request.user)
        return context


class ChangePassword(ThemeMixin, views.PasswordChangeView):
    form_class = forms.ChangePasswordForm
    http_method_names = ["post"]
    success_url = reverse_lazy("account:profile-edit")
